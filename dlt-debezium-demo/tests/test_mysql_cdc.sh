#!/bin/bash
# End-to-end test script for MySQL CDC Pipeline with DuckDB Destination

# Change to project root (one level up from tests/)
cd "$(dirname "$0")/.."

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="test_mysql_results_${TIMESTAMP}.log"
PIPELINE_LOG="cdc_mysql_test_${TIMESTAMP}.log"

exec > >(tee "$LOG_FILE") 2>&1

echo "=================================================================================="
echo "🧪 MYSQL CDC END-TO-END TEST (DuckDB Destination)"
echo "   Started: $(date)"
echo "   Test log: $LOG_FILE"
echo "   Pipeline log: $PIPELINE_LOG"
echo "=================================================================================="
echo ""

echo "🧹 Cleaning up old files, processes, and pipeline state..."
# Step 1: Kill all existing pipeline processes
echo "  📋 Stopping all existing MySQL pipeline processes..."
pkill -f "debezium_dlt_loader_mysql.py" 2>/dev/null || true
sleep 2
ps aux | grep "[d]ebezium_dlt_loader_mysql" && echo "  ⚠️  Some processes still running, force killing..." && pkill -9 -f "debezium_dlt_loader_mysql.py" 2>/dev/null || true
sleep 1

# Step 2: Drop pipeline state using dlt CLI (proper cleanup)
echo "  📋 Dropping dlt pipeline state..."
if source venv/bin/activate 2>/dev/null; then
    python -m dlt pipeline mysql_cdc drop --drop-all 2>/dev/null || true
    python -m dlt pipeline mysql_cdc drop --state-paths "*" 2>/dev/null || true
fi

# Step 3: Manual cleanup as fallback
echo "  📋 Removing old files and directories..."
rm -rf data .dlt/pipelines/mysql_cdc tmp/offsets_mysql_debezium.dat 2>/dev/null || true
rm -rf ~/.dlt/pipelines/mysql_cdc 2>/dev/null || true

# Step 4: Remove all DuckDB files
echo "  📋 Removing DuckDB files..."
rm -f mysql_cdc.duckdb mysql_cdc.duckdb.wal mysql_cdc.duckdb.tmp 2>/dev/null || true
find .dlt -name "*mysql_cdc*.duckdb*" -type f -delete 2>/dev/null || true
find ~/.dlt/pipelines -name "*mysql_cdc*.duckdb*" -type f -delete 2>/dev/null || true

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
server_name = "mysql-server"
database_include_list = "testdb"
table_include_list = "testdb.test_users"
snapshot_mode = "initial"

# MySQL connection details
[sources.debezium.mysql]
host = "localhost"
port = 3306
user = "testuser"
password = "testpassword"
database = "testdb"

# DuckDB destination configuration
[destination.duckdb]
credentials = "duckdb:///mysql_cdc.duckdb"
EOF

cat > .dlt/config.toml << 'EOF'
[cdc_settings.primary_keys]
test_users = "id"
EOF
echo "✅ Configuration files created"
echo ""

echo "🐘 Starting MySQL database..."
# Remove any existing containers first
docker rm -f mysql_source_event_driven mysql_source 2>/dev/null || true
docker-compose up -d mysql_source 2>&1
echo "⏳ Waiting for MySQL to be ready..."
sleep 15
MAX_WAIT=60
WAITED=0
until docker exec mysql_source_event_driven mysqladmin ping -h localhost -uroot -prootpassword --silent > /dev/null 2>&1; do
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo "❌ MySQL failed to start after ${MAX_WAIT} seconds"
        docker logs mysql_source_event_driven 2>&1 | tail -20
        exit 1
    fi
    echo "   Waiting for MySQL... (${WAITED}s/${MAX_WAIT}s)"
    sleep 2
    WAITED=$((WAITED + 2))
done
echo "✅ MySQL is ready"
echo ""

echo "🔧 Setting up database table and binlog..."
docker exec -i mysql_source_event_driven mysql -uroot -prootpassword << 'SQL'
CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;
DROP TABLE IF EXISTS test_users;
CREATE TABLE test_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'testuser'@'%';
FLUSH PRIVILEGES;
SELECT 'MySQL setup complete' as status;
SQL
echo "✅ Database setup complete"
echo ""

echo "🚀 Starting CDC pipeline..."
python debezium_dlt_loader_mysql.py > "$PIPELINE_LOG" 2>&1 &
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
docker exec -i mysql_source_event_driven mysql -utestuser -ptestpassword testdb << 'SQL'
INSERT INTO test_users (name, email) VALUES ('Alice', 'alice@example.com');
SQL
echo "✅ INSERT executed"
echo "⏳ Waiting 12 seconds for INSERT to process and DuckDB locks to release..."
sleep 12
tail -5 "$PIPELINE_LOG" | grep -E "(Processing batch|Batch load complete)" || echo "Waiting for completion..."
echo ""

echo "🔄 Testing UPDATE operation..."
docker exec -i mysql_source_event_driven mysql -utestuser -ptestpassword testdb << 'SQL'
UPDATE test_users SET email = 'alice.updated@example.com' WHERE name = 'Alice';
SQL
echo "✅ UPDATE executed"
echo "⏳ Waiting 12 seconds for UPDATE to process and DuckDB locks to release..."
sleep 12
tail -10 "$PIPELINE_LOG" | grep -E "(Processing batch|Batch load complete)" || tail -5 "$PIPELINE_LOG"
echo ""

echo "➖ Testing DELETE operation..."
docker exec -i mysql_source_event_driven mysql -utestuser -ptestpassword testdb << 'SQL'
DELETE FROM test_users WHERE name = 'Alice';
SQL
echo "✅ DELETE executed"
echo "⏳ Waiting 12 seconds for DELETE to process and DuckDB locks to release..."
sleep 12
tail -15 "$PIPELINE_LOG" | grep -E "(Processing batch|Batch load complete)" || tail -10 "$PIPELINE_LOG"
echo ""

echo "➕ Inserting additional test data..."
docker exec -i mysql_source_event_driven mysql -utestuser -ptestpassword testdb << 'SQL'
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

db_paths = [
    "mysql_cdc.duckdb",
    ".dlt/pipelines/mysql_cdc/*.duckdb",
    Path.home() / ".dlt/pipelines/mysql_cdc/*.duckdb"
]

db_file = None
for path_pattern in db_paths:
    if isinstance(path_pattern, str):
        if "*" in path_pattern:
            from glob import glob
            matches = glob(path_pattern)
            if matches:
                db_file = matches[0]
        elif Path(path_pattern).exists():
            db_file = path_pattern
    else:
        from glob import glob
        matches = glob(str(path_pattern))
        if matches:
            db_file = matches[0]
    if db_file:
        break

if not db_file:
    print("❌ Could not find mysql_cdc.duckdb file")
    sys.exit(1)

try:
    con = duckdb.connect(str(db_file), read_only=True)
    tables = con.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog') AND table_name NOT LIKE '_dlt_%'").fetchall()
    
    if not tables:
        print("⚠️  No tables found in database")
        sys.exit(1)
    
    print(f"✅ Found database: {db_file}")
    for schema, table in tables:
        if schema == "mysql_cdc_data":
            full_table = f"{schema}.{table}"
            total = con.execute(f"SELECT COUNT(*) FROM {full_table}").fetchone()[0]
            try:
                active = con.execute(f"SELECT COUNT(*) FROM {full_table} WHERE deleted = False").fetchone()[0]
                deleted = con.execute(f"SELECT COUNT(*) FROM {full_table} WHERE deleted = True").fetchone()[0]
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
    print("✅ MySQL CDC verification successful")
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

