# MySQL CDC Setup Guide

This guide provides MySQL-specific instructions for setting up Change Data Capture (CDC) with Debezium and dlt.

## Setup Guide

### 1. Environment Requirements

- **Python:** 3.8+
- **Java:** 17+ (Required for the Debezium engine)
- **Docker:** For running local test databases

### 2. Installation & Configuration

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure credentials by copying the template:

```bash
cp .dlt/example.secrets.toml .dlt/secrets.toml
```

Edit `.dlt/secrets.toml` with your MySQL database connection details. See `.dlt/example.secrets.toml` for full configuration options.

Note on strategy: Merge requires primary keys (set in `.dlt/config.toml` or on the dlt resource). If primary keys are missing, the pipeline automatically uses Append mode.

### 3. MySQL Database Setup

**Start MySQL database:**

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

**Grant required privileges for Debezium:**

```bash
docker exec -i mysql_source mysql -u root -prootpassword << 'EOF'
GRANT REPLICATION CLIENT, REPLICATION SLAVE, RELOAD, FLUSH_TABLES ON *.* TO 'myuser'@'%';
FLUSH PRIVILEGES;
EOF
```

Required privileges:
- `REPLICATION CLIENT` / `REPLICATION SLAVE`: Required for binlog streaming
- `RELOAD` / `FLUSH_TABLES`: Required for snapshot phase (table locking)

## Architecture: MERGE vs. APPEND

The pipeline implements `dlt` write dispositions based on the presence of primary keys. For a deep dive into how these modes handle schema evolution and data deduplication, refer to the [dlt destinations documentation](https://dlthub.com/docs/destinations).

### Loading Strategies

| Disposition | Requirement | Behavior on Delete |
| --- | --- | --- |
| **MERGE** | Primary Key defined | Row updated with `deleted=True` |
| **APPEND** | No Primary Key | New audit record with `__op='delete'` |

## Executing the Demo

### Manual Real-Time Stream

Start the CDC pipeline:

```bash
python debezium_dlt_loader_mysql.py
```

The pipeline will perform an initial snapshot and begin streaming changes. Terminate with `Ctrl+C`.

### Database Preparation

Connect to MySQL to prepare the test environment:

```bash
docker exec -it mysql_source mysql -u myuser -pmypassword mydb
```

```sql
-- Create a test table
CREATE TABLE IF NOT EXISTS test_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

### Verification

Perform database operations in the MySQL terminal to see them replicated in DuckDB (local storage: `.dlt/pipelines/mysql_cdc/`):

```sql
-- 1. Insert records
INSERT INTO test_users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO test_users (name, email) VALUES ('Bob', 'bob@example.com');

-- 2. Update a record (Changes the email for Alice)
UPDATE test_users SET email = 'alice.updated@example.com' WHERE name = 'Alice';

-- 3. Delete a record (Triggers soft-delete in MERGE or audit-row in APPEND)
DELETE FROM test_users WHERE name = 'Bob';
```

> **Tip:** You can query the destination DuckDB file using the `dlt` CLI or any DuckDB-compatible tool to verify that the rows reflect these changes in near real-time.

### Automated Testing

For automated end-to-end testing, run the test script:

```bash
./tests/test_mysql_cdc.sh
```

This script automatically sets up the database, runs the pipeline, executes test operations, and verifies results.

## Troubleshooting & Reference

### Essential MySQL Commands

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

**Drop replication state (for fresh start):**
```bash
python -m dlt pipeline mysql_cdc drop --drop-all
rm -f tmp/offsets_mysql_debezium.dat
```

## Technical Notes

* **Full row data in DELETE events:** MySQL includes full row data in DELETE events by default, so no additional configuration is needed beyond privileges (unlike PostgreSQL which requires `REPLICA IDENTITY FULL`).
* **Binary logging:** MySQL binary logging must be enabled (it is by default in MySQL 8.0+). The binlog format should be `ROW` for CDC to work correctly.
* **Dataset naming:** The dataset name for MySQL is `mysql_cdc_data`. In DuckDB, datasets correspond to schemas, so tables are accessed as `dataset_name.table_name`.
