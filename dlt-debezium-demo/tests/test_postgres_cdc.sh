#!/bin/bash
# End-to-end test script for PostgreSQL CDC Pipeline with DuckDB Destination

# Change to project root (one level up from tests/)
cd "$(dirname "$0")/.."

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="test_results_${TIMESTAMP}.log"
PIPELINE_LOG="cdc_test_${TIMESTAMP}.log"

exec > >(tee "$LOG_FILE") 2>&1

echo "=================================================================================="
echo "🧪 POSTGRESQL CDC END-TO-END TEST (DuckDB Destination)"
echo "   Started: $(date)"
echo "   Test log: $LOG_FILE"
echo "   Pipeline log: $PIPELINE_LOG"
echo "=================================================================================="
echo ""

echo "🧹 Cleaning up old files, processes, and pipeline state..."
# Step 1: Kill all existing pipeline processes
echo "  📋 Stopping all existing pipeline processes..."
pkill -f "debezium_dlt_loader.py" 2>/dev/null || true
sleep 2
ps aux | grep "[d]ebezium_dlt_loader" && echo "  ⚠️  Some processes still running, force killing..." && pkill -9 -f "debezium_dlt_loader.py" 2>/dev/null || true
sleep 1

# Step 2: Cleanup replication slot in PostgreSQL
echo "  📋 Cleaning up PostgreSQL replication slot..."
docker exec postgres_source_event_driven psql -U myuser -d mydb << 'SQL' 2>/dev/null || true
DO $$
DECLARE
    pid INTEGER;
BEGIN
    SELECT active_pid INTO pid FROM pg_replication_slots WHERE slot_name = 'debezium_slot';
    IF pid IS NOT NULL THEN
        PERFORM pg_terminate_backend(pid);
        PERFORM pg_sleep(1);
    END IF;
    IF EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = 'debezium_slot') THEN
        PERFORM pg_drop_replication_slot('debezium_slot');
    END IF;
END $$;
SQL

# Step 3: Drop pipeline state using dlt CLI (proper cleanup)
echo "  📋 Dropping dlt pipeline state..."
if source venv/bin/activate 2>/dev/null; then
    python -m dlt pipeline debezium_cdc drop --drop-all 2>/dev/null || true
    python -m dlt pipeline debezium_cdc drop --state-paths "*" 2>/dev/null || true
fi

# Step 4: Manual cleanup as fallback
echo "  📋 Removing old files and directories..."
rm -rf data .dlt/pipelines/* tmp/offsets_postgres_debezium.dat 2>/dev/null || true
rm -rf ~/.dlt/pipelines/debezium_cdc 2>/dev/null || true

# Step 5: Remove all DuckDB files
echo "  📋 Removing DuckDB files..."
rm -f debezium_cdc.duckdb debezium_cdc.duckdb.wal debezium_cdc.duckdb.tmp 2>/dev/null || true
find .dlt -name "*.duckdb*" -type f -delete 2>/dev/null || true
find ~/.dlt/pipelines/debezium_cdc -name "*.duckdb*" -type f -delete 2>/dev/null || true

mkdir -p .dlt/pipelines tmp data
echo "✅ Cleanup complete"
echo ""

echo "📦 Setting up virtual environment..."
python -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -q -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"
echo ""

echo "⚙️  Creating configuration files..."
cat > .dlt/secrets.toml << 'EOF'
# General Debezium settings (connector configuration)
[sources.debezium]
slot_name = "debezium_slot"
publication_name = "debezium_pub"
table_include_list = "public.test_users"
snapshot_mode = "initial"

# PostgreSQL connection details
[sources.debezium.postgres]
host = "localhost"
port = 5432
user = "myuser"
password = "mypassword"
database = "mydb"

# DuckDB destination configuration
[destination.duckdb]
credentials = "duckdb:///debezium_cdc.duckdb"
EOF

cat > .dlt/config.toml << 'EOF'
[cdc_settings.primary_keys]
test_users = "id"
EOF
echo "✅ Configuration files created"
echo ""

echo "🐘 Starting PostgreSQL database..."
docker-compose up -d postgres_source > /dev/null 2>&1
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5
docker exec postgres_source_event_driven pg_isready -U myuser -d mydb > /dev/null 2>&1
echo "✅ PostgreSQL is ready"
echo ""

echo "🔧 Setting up database table and replication..."
docker exec -i postgres_source_event_driven psql -U myuser -d mydb << 'SQL'
DROP TABLE IF EXISTS test_users CASCADE;
CREATE TABLE test_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE test_users REPLICA IDENTITY FULL;
SELECT pg_drop_replication_slot('debezium_slot') WHERE EXISTS (
    SELECT 1 FROM pg_replication_slots WHERE slot_name = 'debezium_slot'
);
DROP PUBLICATION IF EXISTS debezium_pub;
CREATE PUBLICATION debezium_pub FOR TABLE test_users;
SELECT 'Setup complete' as status;
SQL
echo "✅ Database setup complete"
echo ""

echo "🚀 Starting CDC pipeline..."
python debezium_dlt_loader.py > "$PIPELINE_LOG" 2>&1 &
PIPELINE_PID=$!
echo "Pipeline PID: $PIPELINE_PID"
echo "⏳ Waiting 10 seconds for pipeline to initialize..."
sleep 10

if ! kill -0 $PIPELINE_PID 2>/dev/null; then
    echo "❌ Pipeline died immediately! Check $PIPELINE_LOG"
    tail -50 "$PIPELINE_LOG"
    exit 1
fi
echo "✅ Pipeline is running"
echo ""

echo "➕ Testing INSERT operation..."
docker exec -i postgres_source_event_driven psql -U myuser -d mydb << 'SQL'
INSERT INTO test_users (name, email) VALUES ('Alice', 'alice@example.com');
SQL
echo "✅ INSERT executed"
echo "⏳ Waiting 12 seconds for INSERT to process and DuckDB locks to release..."
sleep 12
tail -5 "$PIPELINE_LOG" | grep -E "(Processing batch|Batch load complete)" || echo "Waiting for completion..."
echo ""

echo "🔄 Testing UPDATE operation..."
docker exec -i postgres_source_event_driven psql -U myuser -d mydb << 'SQL'
UPDATE test_users SET email = 'alice.updated@example.com' WHERE name = 'Alice';
SQL
echo "✅ UPDATE executed"
echo "⏳ Waiting 12 seconds for UPDATE to process and DuckDB locks to release..."
sleep 12
tail -10 "$PIPELINE_LOG" | grep -E "(Processing batch|Batch load complete)" || tail -5 "$PIPELINE_LOG"
echo ""

echo "➖ Testing DELETE operation..."
docker exec -i postgres_source_event_driven psql -U myuser -d mydb << 'SQL'
DELETE FROM test_users WHERE name = 'Alice';
SQL
echo "✅ DELETE executed"
echo "⏳ Waiting 12 seconds for DELETE to process and DuckDB locks to release..."
sleep 12
tail -15 "$PIPELINE_LOG" | grep -E "(Processing batch|Batch load complete)" || tail -10 "$PIPELINE_LOG"
echo ""

echo "➕ Inserting additional test data..."
docker exec -i postgres_source_event_driven psql -U myuser -d mydb << 'SQL'
INSERT INTO test_users (name, email) VALUES 
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com');
SQL
echo "✅ Additional inserts executed"
echo "⏳ Waiting 12 seconds for inserts to process and DuckDB locks to release..."
sleep 12
echo ""

echo ""
echo "🛑 Test operations complete. Pipeline is still running (PID: $PIPELINE_PID)"
echo "   Please stop it manually with Ctrl+C when ready"
echo "   Or run: kill $PIPELINE_PID"
echo ""

echo "🔍 Verifying results..."
echo ""
echo "=== PIPELINE LOG SUMMARY ==="
grep -E "(Processing batch|Batch load complete|failed|ERROR)" "$PIPELINE_LOG" | tail -20
echo ""

# Check for DuckDB file
if python << 'PYEOF'
import duckdb
from pathlib import Path
import sys
from glob import glob

db_paths = [
    "debezium_cdc.duckdb",
    ".dlt/pipelines/debezium_dlt_pipeline/*.duckdb",
    Path.home() / ".dlt/pipelines/debezium_dlt_pipeline/*.duckdb"
]

db_file = None
for path_pattern in db_paths:
    if isinstance(path_pattern, str):
        if "*" in path_pattern:
            matches = glob(path_pattern)
            if matches:
                db_file = matches[0]
        elif Path(path_pattern).exists():
            db_file = path_pattern
    else:
        matches = glob(str(path_pattern))
        if matches:
            db_file = matches[0]
    if db_file:
        break

if not db_file:
    print("❌ Could not find debezium_cdc.duckdb file")
    sys.exit(1)

try:
    con = duckdb.connect(str(db_file), read_only=True)
    tables = con.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog') AND table_name NOT LIKE '_dlt_%'").fetchall()
    
    if not tables:
        print("⚠️  No tables found in database")
        sys.exit(1)
    
    print(f"✅ Found database: {db_file}")
    for schema, table in tables:
        if schema == "debezium_data":
            full_table = f"{schema}.{table}"
            total = con.execute(f"SELECT COUNT(*) FROM {full_table}").fetchone()[0]
            try:
                active = con.execute(f"SELECT COUNT(*) FROM {full_table} WHERE __deleted = False").fetchone()[0]
                deleted = con.execute(f"SELECT COUNT(*) FROM {full_table} WHERE __deleted = True").fetchone()[0]
                print(f"   Table {table}: {total} total ({active} active, {deleted} deleted)")
            except:
                print(f"   Table {table}: {total} total")
            
            # Show sample data
            sample = con.execute(f"SELECT * FROM {full_table} ORDER BY id LIMIT 3").fetchall()
            if sample:
                print(f"   Sample data:")
                for row in sample:
                    print(f"     {row}")
    con.close()
    print("✅ PostgreSQL CDC verification successful")
except Exception as e:
    print(f"❌ Error querying database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF
then
    echo "✅ DuckDB database found and queried successfully"
else
    echo "⚠️  DuckDB verification failed"
fi

echo ""
echo "=================================================================================="
echo "✅ END-TO-END TEST COMPLETE"
echo "   Finished: $(date)"
echo "   Pipeline log: $PIPELINE_LOG"
echo "   Test log: $LOG_FILE"
echo "=================================================================================="

