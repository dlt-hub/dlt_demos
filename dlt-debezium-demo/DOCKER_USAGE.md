# Docker Setup Usage Guide

This Docker setup includes Java 17+ and all Python dependencies, so you don't need to install anything locally!

## Quick Start

### 1. Set up configuration

Copy the example secrets file:
```bash
cp .dlt/example.secrets.toml .dlt/secrets.toml
```

Edit `.dlt/secrets.toml` - the hostnames should be:
- PostgreSQL: `postgres_source` (Docker service name)
- MySQL: `mysql_source` (Docker service name)

### 2. Start the databases

```bash
docker-compose up -d
```

This starts PostgreSQL and MySQL (and pgAdmin).

### 3. Run the CDC pipeline

**Option A: Run interactively (recommended for testing)**
```bash
docker-compose --profile cdc run --rm debezium_dlt_pipeline
```

**Option B: Run in background**
```bash
docker-compose --profile cdc up -d debezium_dlt_pipeline
```

**Option C: Run with custom command**
```bash
# For PostgreSQL
docker-compose --profile cdc run --rm debezium_dlt_pipeline python debezium_dlt_loader.py

# For MySQL
docker-compose --profile cdc run --rm debezium_dlt_pipeline python debezium_dlt_loader_mysql.py
```

### 4. View logs

```bash
docker-compose logs -f debezium_dlt_pipeline
```

### 5. Stop everything

```bash
docker-compose down
```

## Benefits

- Java 17 and Python dependencies are pre-installed in the container
- No local installation required
- Consistent environment across machines  

## Troubleshooting

**Check if Java is working:**
```bash
docker-compose --profile cdc run --rm debezium_dlt_pipeline java -version
```

**Check Python dependencies:**
```bash
docker-compose --profile cdc run --rm debezium_dlt_pipeline pip list
```

**Rebuild the container (if you update requirements.txt):**
```bash
docker-compose build debezium_dlt_pipeline
```
