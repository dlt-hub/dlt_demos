# Change Data Capture with Debezium and dlt

## Overview

This project demonstrates **Universal Change Data Capture (CDC)** using the Embedded Debezium Engine combined with `dlt`. While this demo focuses on PostgreSQL, the architecture seamlessly supports MySQL, Oracle, SQL Server, MongoDB, DB2, and Cassandra.

By utilizing an Embedded Debezium Engine running directly in Python, this solution eliminates the need for complex infrastructure like Kafka or Zookeeper, providing a lightweight, "infrastructure-free" deployment.

### The Data Flow

1. **Source:** PostgreSQL Database
2. **Capture:** Debezium Engine (Embedded in Python)
3. **Format:** JSON Change Events
4. **Processing:** `DltChangeHandler` (Custom logic)
5. **Loading:** `dlt` Pipeline
6. **Destination:** DuckDB (or any supported `dlt` destination)

## Setup Guide

### 1. Environment Requirements

- **Python:** 3.8+
- **Java:** 17+ (Required for the Debezium engine)
- **Docker Desktop:** For running local test databases

### 2. Installation & Configuration

Install the core dependencies:

```bash
pip install -r requirements.txt
```

Configure your credentials by copying the template and editing your connection details:

```bash
cp .dlt/example.secrets.toml .dlt/secrets.toml
```

Edit `.dlt/secrets.toml` with your PostgreSQL database connection details. See `.dlt/example.secrets.toml` for full configuration options.

> **Note on Strategy:** Configure primary keys in `.dlt/config.toml` to enable the **Merge** write disposition. Without primary keys, the pipeline defaults to **Append** mode.

### 3. Initialization

Spin up the source database:

```bash
docker-compose up -d
```

## Architecture: MERGE vs. APPEND

The pipeline automatically selects a loading strategy based on your primary key configuration:

| Feature | MERGE Mode  | APPEND Mode |
| --- | --- | --- |
| **Trigger** | Primary keys defined in `.dlt/config.toml` or resource | No primary keys provided (Default) |
| **Updates** | Overwrites existing records | Creates a new record (Full history) |
| **Deletes** | Soft delete (`deleted=True`) | Audit record (`__op='delete'`) |


## Executing the Demo

### Manual Real-Time Stream

Start the CDC pipeline to begin monitoring PostgreSQL for changes:

```bash
python debezium_dlt_loader.py
```

The pipeline will connect to your PostgreSQL database, perform an initial snapshot, and begin streaming changes in real-time. Keep it running until you press `Ctrl+C`.

### Database Preparation

Connect to PostgreSQL to create a test environment:

```bash
docker exec -it postgres_source_event_driven psql -U myuser -d mydb
```

```sql
-- 1. Create a test table
CREATE TABLE IF NOT EXISTS test_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- 2. Enable CDC via Publication
DROP PUBLICATION IF EXISTS debezium_pub;
CREATE PUBLICATION debezium_pub FOR TABLE test_users;

-- 3. Capture full row state for deletes
ALTER TABLE test_users REPLICA IDENTITY FULL;
```

### Verification

As you perform `INSERT`, `UPDATE`, or `DELETE` operations in PostgreSQL, the changes will replicate instantly to DuckDB (located in `.dlt/pipelines/debezium_cdc/`).

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

### Automated Testing

For automated end-to-end testing, run the test script:

```bash
./tests/test_postgres_cdc.sh
```

This script automatically sets up the database, runs the pipeline, executes test operations, and verifies results.

## Troubleshooting & Reference

### Essential PostgreSQL Commands

**Check replication slots:**
```sql
SELECT * FROM pg_replication_slots WHERE slot_name = 'debezium_slot';
```

**Check REPLICA IDENTITY setting:**
```sql
SELECT relreplident, relname 
FROM pg_class 
WHERE relname = 'test_users';
-- 'f' = full (what we want), 'd' = default (primary key only)
```

**Drop replication slot (for fresh start):**
```sql
SELECT pg_drop_replication_slot('debezium_slot');
```

**Clean pipeline state:**
```bash
python -m dlt pipeline debezium_cdc drop --drop-all
rm -f tmp/offsets_postgres_debezium.dat
```

> **Note:** If you see the error "offset is no longer available on the server", delete the offset file and restart. This happens when PostgreSQL has purged old WAL segments that the offset file references.

> **⚠️ Critical Requirement:** Always set `REPLICA IDENTITY FULL` on PostgreSQL tables. Without this, `DELETE` events will only contain the Primary Key, causing `NULL` values for all other columns in your destination.

> **Note:** For PostgreSQL-only CDC use cases, consider dlt's native `pg_replication` source for a simpler setup (no Java or Debezium engine required).

> **Project Structure:**
> 
> ```
> dlt-debezium-demo/
> ├── debezium_dlt_loader.py          # PostgreSQL CDC loader
> ├── debezium_dlt_loader_mysql.py    # MySQL CDC loader
> ├── config_helper_universal.py      # Config generator
> ├── tests/
> │   ├── test_postgres_cdc.sh        # PostgreSQL end-to-end test script
> │   └── test_mysql_cdc.sh           # MySQL end-to-end test script
> ├── requirements.txt                # Python dependencies
> ├── docker-compose.yml              # PostgreSQL database setup
> ├── MYSQL.md                              # MySQL-specific setup guide
> ├── .dlt/
> │   ├── example.secrets.toml        # Config template
> │   └── example.config.toml         # Primary keys template
> └── README.md                       # This file (PostgreSQL focus)
> ```

> **MySQL Setup:** For MySQL-specific setup instructions, see [MYSQL.md](MYSQL.md).
