# Change Data Capture with Debezium and dlt

## Overview

This is a demo that embeds the [Debezium Engine](https://debezium.io/documentation/reference/stable/development/engine.html) inside a `dlt` pipeline to capture database changes and load them into a destination.

It focuses on the simplest shape of CDC: **point-to-point replication** (source ➜ destination) running as a single process.

## What it does

- Captures **inserts, updates, and deletes** from a source database
- Loads changes into a destination table in near real time
- Handles schema drift with **dlt schema evolution** (new columns, `ALTER TABLE`, etc.)
- Supports two write patterns:
  - **MERGE mode:** keep one current table (updates apply, deletes are soft-deleted)
  - **APPEND mode:** keep an audit log of every change event

## When this is a good fit

**Use Embedded Debezium + dlt when:**
- **CDC without a streaming platform:** Capture changes without running Kafka or managing streaming infrastructure.
- **Rapid prototyping:** Go from a source database to a queryable destination in minutes.
- **Frequent schema changes:** Handle new columns and `ALTER TABLE` evolution automatically with dlt.
- **Lightweight runtime:** Deploy as a single container or VM.
- **Multi-DB pattern:** Use one consistent pattern across Postgres and MySQL, and extend it to SQL Server or Oracle.
- **Low-impact capture:** Read transaction logs (WAL/Binlog) to minimize load on the production database.
- **Audit-ready history:** Persist inserts, updates, and deletes to maintain a complete, queryable change log.

**When this may not be the best fit:**
- **Many consumers:** If 10+ downstream systems need the same change stream, a centralized broker like Kafka is usually more efficient. This architecture is optimized for point-to-point replication (source ➜ destination).
- **Very high throughput:** At tens of thousands of changes per second, the embedded engine and the Python/JVM boundary can become a bottleneck.
- **Horizontal scaling:** This runs as a single process. You can scale up (larger instance), but you can't scale out across multiple nodes like Kafka Connect.
- **Strict exactly-once requirements:** This provides at-least-once semantics. If the destination cannot tolerate duplicates on restart, you must rely on destination-side deduplication (for example merge write disposition) or use a true end-to-end exactly-once system.
- **Java-restricted environments:** Debezium requires a JVM. If you can't ship Java in your runtime environment, this isn't a good fit.

> **Note:** For PostgreSQL-only workloads, consider `dlt`'s native `pg_replication` source—no Java dependency.

## How it Works

- Debezium runs **embedded in-process**
- dlt handles:
  - schema management
  - loading into the destination
  - deduplication and merges (when configured)

This is designed for **source ➜ destination replication**, not for fan-out or complex stream processing.

### The Data Flow
A step-by-step breakdown of how data moves from your source database to your warehouse.
1. **Source:** Your database (Postgres, MySQL, etc.).
2. **Capture:** Debezium runs alongside the pipeline and streams changes directly from the database's transaction log.
3. **Event:** Every change is converted into a JSON event with operation-specific data (INSERT: new values, DELETE: old values, UPDATE: old and new values).
4. **Handler:** The `DltChangeHandler` collects these events and prepares them for the `dlt` pipeline.
5. **Loading**: The dlt pipeline loads the changes into the destination.
6. **Destination:** A local database (e.g., DuckDB) or a warehouse where the replicated data lands.

### System Diagram
```
Source Database (Docker)
───────────────────────
Postgres / MySQL / ...
(transaction log, e.g. WAL or binlog)

        │
        │ Change events
        ▼

Debezium Engine (Embedded)
─────────────────────────
• Runs in-process (background thread)
• Produces change events (JSON)

        │
        │ JSON events
        ▼

Python Process (dlt)
────────────────────
DltChangeHandler
• Converts events to records
• Handles batching
        │
        ▼
dlt Pipeline
• Schema evolution
• MERGE / APPEND
        │
        ▼
DuckDB / Warehouse
──────────────────
Final Destination
```

**Why Docker?**
The `docker-compose.yml` runs source databases with CDC already configured. The `Dockerfile` includes the Java runtime, so you don't need to install it locally. Only Docker is required to run the entire demo.

**Components:**
- **Debezium Engine:** Embedded via `pydbzengine`. Captures the database transaction log (WAL/binlog) in a background thread.
- **Python handler (`DltChangeHandler`):** Processes events into a dlt-compatible format and ensures batching.
- **dlt pipeline:** Normalizes nested JSON into relational tables and handles automatic schema migrations.
- **DuckDB:** Local destination for the demo (swappable for Snowflake, BigQuery, etc.).

## Setup Guide

> **Note:** You can run this entire demo using Docker without installing dependencies locally. See [DOCKER_USAGE.md](DOCKER_USAGE.md) for Docker setup instructions.

**Requirements:** Python 3.8+, Docker (Java 17+ only needed if running outside Docker)

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Executing the Demo

Run the pipeline locally or in Docker:

**Run locally:**
```bash
python debezium_dlt_loader.py
```

**Or run in Docker (no local Java/Python setup needed):**
```bash
docker-compose --profile cdc run --rm debezium_dlt_pipeline
```

> **Note:** For detailed Docker setup instructions, see [DOCKER_USAGE.md](DOCKER_USAGE.md).

### Database Preparation

Prepare your source database for CDC. This is required regardless of whether you run the pipeline locally or in Docker.

**PostgreSQL:**
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

> **Note:** For MySQL setup, see [MYSQL.md](MYSQL.md).

### Verification
Perform database operations in the Postgres terminal:
```sql
INSERT INTO test_users (name, email) VALUES ('Alice', 'alice@example.com');
UPDATE test_users SET email = 'alice.updated@example.com' WHERE name = 'Alice';
DELETE FROM test_users WHERE name = 'Alice';
```
Query the destination DuckDB file to verify near real-time replication.

## Loading Strategies: MERGE vs. APPEND

The pipeline selects a write disposition based on primary key configuration:

- **INSERT:** New rows inserted
- **UPDATE:** Rows updated (MERGE) or new audit records (APPEND)
- **DELETE:** Handled by write disposition (see table)

| Disposition | Requirement | Behavior on Delete |
| --- | --- | --- |
| **MERGE** | Primary or Merge key defined | Soft delete (`__deleted=True`) | 
| **APPEND** | No key defined | Audit record (`__op='delete'`) |

## From demo to production

This demo can run in production, but a 24/7 CDC pipeline needs a few guardrails.

### Hardening

- **Secrets:** `.dlt/secrets.toml` is gitignored. In production, use environment variables or a secrets manager.
- **No duplicates on restart:** Define `primary_key`s for all `MERGE` resources so a restart does not create duplicate rows.

### Reliability

- **Keep state between restarts:** Store the `.dlt` folder on persistent storage. If it's lost, the pipeline can lose its "last processed position" and may re-snapshot.
- **Memory safety:** Debezium runs as part of this process. Put a memory limit on the container/VM so one component can't exhaust all RAM and crash the job.

### Operations

- **If the pipeline stops, logs can pile up:** If CDC is paused for a long time, the source database may retain more change logs, which can consume disk. Monitor disk usage and alert if the pipeline is down.
- **Health checks:** Run this under an orchestrator (Docker restart policy, Kubernetes, systemd, Airflow/Prefect) so it restarts if it crashes or stalls.
- **Handle spikes:** Start with conservative batch sizes and increase gradually once you observe steady throughput.

## Troubleshooting & Reference

### Essential PostgreSQL Commands
- **Check replication slots:** `SELECT * FROM pg_replication_slots;`
- **Check REPLICA IDENTITY:** `SELECT relreplident, relname FROM pg_class WHERE relname = 'test_users';`
- **Drop slot:** `SELECT pg_drop_replication_slot('debezium_slot');`

### Technical Notes
- **Replica Identity:** Always set `REPLICA IDENTITY FULL` on Postgres. Without this, `DELETE` events won't contain previous column values.
- **Delete Handling:** DELETE operations are handled via soft-delete (MERGE mode) or audit records (APPEND mode). Rows are not physically removed from the destination.
- **MySQL Setup:** See [MYSQL.md](MYSQL.md) for binary log configuration.

## Project Structure
```text
R1-dlt-debezium-demo/
├── debezium_dlt_loader.py          # PostgreSQL CDC loader
├── debezium_dlt_loader_mysql.py    # MySQL CDC loader
├── config_helper_universal.py      # Debezium config generator
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Java + Python pipeline image
├── docker-compose.yml              # Local source DBs
├── .dlt/
│   ├── example.secrets.toml        # Config template
│   └── example.config.toml         # Primary keys template
└── README.md                       # This file
```

> **After first run:** `.dlt/secrets.toml` and `.dlt/debezium.properties` are generated locally.