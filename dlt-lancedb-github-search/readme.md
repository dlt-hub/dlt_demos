# github-search-app

ETL pipelines that ingest GitHub stars from BigQuery, enrich them via Parallel AI, and sync to LanceDB Cloud for semantic search.

## Setup

### Prerequisites

- Python 3.13+ with [uv](https://docs.astral.sh/uv/)
- GCP credentials (ADC or secrets.toml)

### Secrets

Copy the template below to `.dlt/secrets.toml` and fill in your values:

```toml
[destination.filesystem.credentials]
aws_access_key_id = "your-r2-access-key-id"
aws_secret_access_key = "your-r2-secret-access-key"
endpoint_url = "https://<account-id>.r2.cloudflarestorage.com"

[destination.lancedb.credentials]
embedding_model_provider_api_key = "your-gemini-api-key"
api_key = "your-lancedb-api-key"
```

## Project Structure

```
etl_01_github_stars.py        # Pipeline 1: BigQuery -> filesystem/R2
etl_02_parallel_enrichment.py # Pipeline 2: GitHub stars -> Parallel AI -> enriched dataset
etl_03_r2_to_lancedb.py       # Pipeline 3: R2 -> LanceDB Cloud
models.py                     # Shared enums, Pydantic model, system prompt
```

## Pipelines

| Pipeline | File | Purpose |
|----------|------|---------|
| `github_stars` | `etl_01_github_stars.py` | Ingest GitHub stars from BigQuery |
| `parallel_enrichment` | `etl_02_parallel_enrichment.py` | Enrich repos via Parallel AI Task API |
| `lancedb_embeddings` | `etl_03_r2_to_lancedb.py` | Sync enriched data from R2 to LanceDB Cloud |

## Profile Configuration

Destination-specific settings are split by profile so the same pipeline code writes locally in dev and to R2 in prod.

| Profile | Config file | `destination.filesystem.bucket_url` |
|---------|-------------|-------------------------------------|
| `dev` | `.dlt/dev.config.toml` | `./out/github-stars` (local) |
| `prod` | `.dlt/prod.config.toml` | `s3://github-search-app-stars` (R2) |

Shared settings (source config, LanceDB) live in `.dlt/config.toml`. Profile-scoped files override values in the shared config. Switch profiles with `WORKSPACE__PROFILE=prod uv run python ...` or `dlt profile <name> pin`.

## Running

```bash
uv run python etl_01_github_stars.py
uv run python etl_02_parallel_enrichment.py
uv run python etl_03_r2_to_lancedb.py
```

## dlt AI

This project uses [`dlt`](https://dlthub.com/) with AI-assisted tooling for pipeline development, secrets management, and deployment.

### Setup

```bash
# Check AI setup status (dlt version, agent, toolkits)
uv run dlt ai status

# Install AI rules and skills for your coding agent
uv run dlt ai init --agent claude

# Install MCP server config
uv run dlt ai mcp install
```

### Secrets Management

```bash
# List secret file locations
uv run dlt ai secrets list

# View secrets (redacted)
uv run dlt ai secrets view-redacted

# Merge a TOML fragment into the secrets file
uv run dlt ai secrets update-fragment --path .dlt/secrets.toml
```

### Toolkits

```bash
# List available toolkits
uv run dlt ai toolkit list

# Show toolkit contents
uv run dlt ai toolkit <name> info

# Install a toolkit
uv run dlt ai toolkit <name> install
```

### MCP Server

```bash
# Run the MCP server (stdio mode)
uv run dlt ai mcp run --stdio

# Run with custom port
uv run dlt ai mcp run --port 8000

# Enable/disable features
uv run dlt ai mcp run --features -secrets +context
```
