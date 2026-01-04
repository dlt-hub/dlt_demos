# Change Data Capture with Debezium and dlt

## Overview

This project demonstrates **Change Data Capture (CDC)** using the Embedded Debezium Engine combined with dlt. While this demo focuses on PostgreSQL, the architecture is compatible with MySQL, Oracle, SQL Server, MongoDB, DB2, and Cassandra.

By utilizing an Embedded Debezium Engine running within Python, this solution removes the requirement for external Kafka or Zookeeper clusters, providing a localized deployment for capturing database events.

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

Edit `.dlt/secrets.toml` with your PostgreSQL database connection details. See `.dlt/example.secrets.toml` for full configuration options.

Note on strategy:
Merge requires primary keys (set in `.dlt/config.toml` or on the dlt resource).
If primary keys are missing, the pipeline automatically uses Append mode.

### 3. Initialization

Start the source database:

```bash
docker-compose up -d
```

## Architecture: MERGE vs. APPEND

The pipeline implements `dlt` write dispositions based on the presence of primary keys. For a deep dive into how these modes handle schema evolution and data deduplication, refer to the [dlt destinations documentation](https://dlthub.com/docs/general-usage/incremental-loading#choosing-a-write-disposition).

### Loading Strategies

| Disposition | Requirement | Behavior on Delete |
| --- | --- | --- |
| **MERGE** | Primary Key defined | Row updated with `deleted=True` |
| **APPEND** | No Primary Key | New audit record with `__op='delete'` |

## Executing the Demo

### Manual Real-Time Stream

Start the CDC pipeline:

```bash
python debezium_dlt_loader.py
```

The pipeline will perform an initial snapshot and begin streaming changes. Terminate with `Ctrl+C`.

### Database Preparation

Connect to PostgreSQL to prepare the test environment:

```bash
docker exec -it postgres_source_event_driven psql -U myuser -d mydb
```

```sql
-- Create a test table
CREATE TABLE IF NOT EXISTS test_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Enable CDC via Publication
DROP PUBLICATION IF EXISTS debezium_pub;
CREATE PUBLICATION debezium_pub FOR TABLE test_users;

-- Capture full row state for deletes
ALTER TABLE test_users REPLICA IDENTITY FULL;
```

### Verification

Perform database operations in the PostgreSQL terminal to see them replicated in DuckDB (local storage: `.dlt/pipelines/debezium_cdc/`):

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

## Technical Notes

* **Replica Identity:** Always set `REPLICA IDENTITY FULL` on PostgreSQL tables. Without this, `DELETE` events will only contain the Primary Key, resulting in `NULL` values for all other columns in the destination.
* **Alternative:** For PostgreSQL-only use cases, consider dlt's native `pg_replication` source. It provides a simpler setup that does not require Java or the Debezium engine.
* **MySQL Setup:** For MySQL-specific instructions, see [MYSQL.md](MYSQL.md).

## Project Structure

```text
dlt-debezium-demo/
├── debezium_dlt_loader.py          # PostgreSQL CDC loader
├── debezium_dlt_loader_mysql.py    # MySQL CDC loader
├── config_helper_universal.py      # Config generator
├── tests/
│   ├── test_postgres_cdc.sh        # PostgreSQL end-to-end test script
│   └── test_mysql_cdc.sh           # MySQL end-to-end test script
├── requirements.txt                # Python dependencies
├── docker-compose.yml              # PostgreSQL database setup
├── MYSQL.md                        # MySQL-specific setup guide
├── .dlt/
│   ├── example.secrets.toml        # Config template
│   └── example.config.toml         # Primary keys template
└── README.md                       # This file
```
