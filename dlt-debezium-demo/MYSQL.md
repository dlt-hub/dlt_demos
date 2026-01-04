# MySQL CDC Setup Guide

This guide provides MySQL-specific instructions for setting up Change Data Capture (CDC) with Debezium and dlt.

## Prerequisites

Same as main README: Python 3.8+, Java 17+, and Docker Desktop.

## MySQL Setup

1. **Start MySQL database:**

   ```bash
   docker run -d --name mysql_source \
     -e MYSQL_ROOT_PASSWORD=rootpassword \
     -e MYSQL_DATABASE=mydb \
     -e MYSQL_USER=myuser \
     -e MYSQL_PASSWORD=mypassword \
     -p 3306:3306 \
     mysql:8.0
   ```

   Wait for MySQL to be ready:
   ```bash
   docker exec mysql_source mysqladmin ping -h localhost -uroot -prootpassword --silent
   ```

2. **Grant required privileges for Debezium:**

   ```bash
   docker exec -i mysql_source mysql -u root -prootpassword << 'EOF'
   GRANT REPLICATION CLIENT, REPLICATION SLAVE, RELOAD, FLUSH_TABLES ON *.* TO 'myuser'@'%';
   FLUSH PRIVILEGES;
   EOF
   ```

   **Why these privileges are needed:**
   - `REPLICATION CLIENT` / `REPLICATION SLAVE`: Required for binlog streaming
   - `RELOAD` / `FLUSH_TABLES`: Required for snapshot phase (table locking)

3. **Configure database connection:**

   Copy and edit `.dlt/secrets.toml`:

   ```bash
   cp .dlt/example.secrets.toml .dlt/secrets.toml
   ```

   Configure MySQL connection in `.dlt/secrets.toml`:

   ```toml
   # MySQL connection details
   [sources.debezium.mysql]
   host = "localhost"
   port = 3306
   user = "myuser"
   password = "mypassword"
   database = "mydb"

   # General Debezium settings
   [sources.debezium]
   database_include_list = "mydb"
   table_include_list = "mydb.test_users"
   snapshot_mode = "initial"
   ```

   Setup primary keys in `.dlt/config.toml` as shown in `.dlt/example.config.toml` to use merge write disposition.

4. **Set up test table:**

   ```bash
   docker exec -i mysql_source mysql -uroot -prootpassword << 'SQL'
   CREATE DATABASE IF NOT EXISTS testdb;
   USE testdb;
   CREATE TABLE test_users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(100),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   SQL
   ```

## Running the Pipeline

**Start MySQL CDC Pipeline:**

```bash
python debezium_dlt_loader_mysql.py
```

This uses the `mysql_cdc` pipeline name and creates data in the `mysql_cdc_data` dataset.

## MySQL Setup Commands

**Connect to MySQL:**
```bash
docker exec -it mysql_source mysql -u myuser -pmypassword mydb
```

**Check binary logging:**
```sql
SHOW VARIABLES LIKE 'log_bin';
SHOW VARIABLES LIKE 'binlog_format';
-- Should show 'ROW' for binlog_format
```

**Create test table:**
```sql
CREATE TABLE IF NOT EXISTS test_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

**Test INSERT operation:**
```sql
INSERT INTO test_users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO test_users (name, email) VALUES ('Bob', 'bob@example.com');
```

**Test UPDATE operation:**
```sql
UPDATE test_users SET email = 'alice.updated@example.com' WHERE name = 'Alice';
```

**Test DELETE operation:**
```sql
DELETE FROM test_users WHERE name = 'Bob';
```

## Viewing Your Data

Query the DuckDB database:

```python
import duckdb
from pathlib import Path

# Find DuckDB file in pipeline state
pipeline_dir = Path(".dlt/pipelines/mysql_cdc")
db_file = list(pipeline_dir.rglob("*.duckdb"))[0]

con = duckdb.connect(str(db_file), read_only=True)

# Show all tables
tables = con.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

# Query data from mysql_cdc_data dataset
records = con.execute("SELECT * FROM mysql_cdc_data.test_users ORDER BY id").fetchall()
for r in records:
    print(r)

con.close()
```

> Note: The dataset name for MySQL is `mysql_cdc_data`. In DuckDB, datasets correspond to schemas, so tables are accessed as `dataset_name.table_name`.

## Automated Testing

Run the MySQL end-to-end test script:

```bash
./tests/test_mysql_cdc.sh
```

This script automatically sets up the database, runs the pipeline, executes test operations, and verifies results.

## MySQL-Specific Notes

- **Full row data in DELETE events:** MySQL includes full row data in DELETE events by default, so no additional configuration is needed beyond privileges (unlike PostgreSQL which requires `REPLICA IDENTITY FULL`).

- **Binary logging:** MySQL binary logging must be enabled (it is by default in MySQL 8.0+). The binlog format should be `ROW` for CDC to work correctly.

- **Pipeline cleanup:** When restarting, clean up MySQL pipeline state:
  ```bash
  python -m dlt pipeline mysql_cdc drop --drop-all
  rm -f tmp/offsets_mysql_debezium.dat
  ```

