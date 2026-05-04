# dlt + DataHub demo

A minimal end-to-end demo: a `dlt` pipeline pulls data from the GitHub REST API into DuckDB, then publishes its datasets, schemas, and lineage to a locally-running DataHub instance.

The goal is to showcase the DataHub features that work naturally with a `dlt` pipeline — cataloging, containers, lineage, schema tracking, run history, ownership, and tags.

---

## What you'll see at the end

- `repos` and `issues` tables loaded into DuckDB from the GitHub API.
- Both tables (and dlt's internal `_dlt_loads` / `_dlt_pipeline_state`) catalogued in DataHub with full schemas.
- A pipeline **container** in DataHub grouping the tables.
- A **lineage** graph: `GitHub API → dlt pipeline → DuckDB tables`.
- Each pipeline run recorded as an **operation** event (success/fail, row counts).

---

## Prerequisites

| Tool | Why | Install |
| --- | --- | --- |
| Docker Desktop | Runs the local DataHub stack (GMS, MySQL, Elasticsearch, Kafka, UI) | https://www.docker.com/products/docker-desktop |
| Python **3.11** | DataHub CLI prints a warning above 3.11; stay on 3.11 to avoid surprises | `brew install python@3.11` |
| `uv` | Project / dependency manager | `brew install uv` |
| GitHub PAT | Auth for the GitHub REST API (any classic token with `public_repo` is fine) | https://github.com/settings/tokens |

Make sure Docker Desktop is **running** and has at least **8 GB RAM** allocated (Settings → Resources). The DataHub quickstart is a heavy stack.

If your venv is on Python 3.13+, you'll see `Python versions above 3.11 are not actively tested with yet` from the `datahub` CLI. To pin 3.11:

```bash
uv venv --python 3.11
uv pip install -r requirements.txt
```

---

## Step 1 — Clone and create the virtualenv

```bash
git clone <this-repo>
cd datahub
uv venv --python 3.11
```

You don't need to `source .venv/bin/activate` — every command below uses `uv run`, which picks up the venv automatically.

## Step 2 — Install Python dependencies

```bash
uv pip install -r requirements.txt
uv pip install "acryl-datahub[datahub-rest]"
```

`acryl-datahub` ships both the `datahub` CLI (used to launch the local stack) and the Python SDK v2 (`datahub.sdk.DataHubClient` + `LineageClient`) used by `dlt_to_datahub.py` to emit metadata.

## Step 3 — Launch DataHub locally

Make sure Docker Desktop is **running** before this step (the quickstart talks to the local Docker daemon).

```bash
uv run datahub docker quickstart
```

First run pulls ~5 GB of images and takes 5–10 minutes. When it finishes you'll have:

| Service | URL | Purpose |
| --- | --- | --- |
| DataHub UI | http://localhost:9002 | Browser UI (login: `datahub` / `datahub`) |
| GMS | http://localhost:8080 | Metadata service — what the pipeline emits to |

Sanity check:

```bash
curl http://localhost:8080/health   # should return "GOOD"
```

To stop / reset later:

```bash
uv run datahub docker quickstart --stop   # stop, keep data
uv run datahub docker nuke                # wipe everything
```

## Step 4 — Configure the GitHub token

The dlt CLI already created `.dlt/secrets.toml`. Put your PAT there:

```toml
# .dlt/secrets.toml
[sources]
access_token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

`.dlt/` is gitignored, so this won't be committed.

## Step 5 — Run the pipeline

```bash
uv run python rest_api_pipeline.py
```

What happens, in order:

1. dlt pulls `repos` + `issues` from the GitHub API into DuckDB (`github_pipeline.duckdb`).
2. `dlt_to_datahub.integrate_dlt_pipeline_with_datahub()` connects to GMS (`localhost:8080`) using `DataHubClient`, then for each loaded table:
   - Upserts a `Container` (one per pipeline dataset)
   - Upserts a `Dataset` with schema + columns (typed)
   - Calls `client.lineage.add_lineage(upstream=<github URN>, downstream=<duckdb URN>)`
3. The script prints the container URL plus each lineage edge it emitted.

Verify in DuckDB:

```bash
uv run python -c "import duckdb; con = duckdb.connect('github_pipeline.duckdb'); print(con.sql('SHOW ALL TABLES'))"
```

## Step 6 — Explore in DataHub

Open http://localhost:9002 and walk through:

**Auto-emitted by the pipeline:**

1. **Search** — type `repos` or `issues`. Tables (and child tables like `repos__topics`) show up.
2. **Container** — `github_data` groups every loaded table under one pipeline run.
3. **Schema tab** — typed columns extracted from dlt's inferred schema.
4. **Lineage tab** — *Upstreams* shows `dlt-hub/repos` (GitHub) → `repos` (DuckDB). *Downstreams* shows the parent → child chain (`repos → repos__topics`). Toggle `direct` / `indirect` to expand the graph.
5. **Documentation** — every dataset has a default `Loaded by dlt pipeline ...` description.
6. **Tags** — every dataset is tagged `dlt-ingested`. Search `tag:dlt-ingested` to filter.
7. **Search by tag** — top-bar filter `tags = dlt-ingested` to see everything dlt loaded across all pipelines.

**Manually set in the UI (the governance demo):**

8. **Owners** — open `github_data.repos` → click `+` next to Owners → assign yourself.
9. **Domain** — assign a domain like `Source Systems`.
10. **Glossary terms** — open `issues` schema → tag `user.email` with a `PII` glossary term.
11. **Long-form docs** — write a richer Markdown description in the *Documentation* tab.

**Re-run for run history:**

12. `uv run python rest_api_pipeline.py` again. Each run shows up under the dataset's *Stats / Operations* view with timestamp + row counts.

---

## Demo talking points (DataHub features that pair with dlt)

| Feature | What dlt provides | What DataHub adds |
| --- | --- | --- |
| Cataloging | Loaded tables + JSON schemas | Searchable, browsable inventory across all sources |
| Containers | Pipeline name + dataset name | Visual grouping, navigable as one unit |
| Lineage | `load_info` (source URL → tables) | Cross-pipeline graph, click-through navigation |
| Schema evolution | Schema inferred each run | Versioned schema history, diff view |
| Run history | `load_info` per run | Operation timeline, success/fail trends |
| Governance | — | Tags, glossary terms, PII classification, ownership |
| Quality | — | Assertions (freshness, row counts, null rates) |
| Documentation | — | Markdown descriptions on tables and columns |

Features that exist in DataHub but **aren't relevant to this demo** (mention only if asked): ML features/models, BI dashboard lineage, fine-grained access policies (DuckDB is a local file — only meaningful with Snowflake / BigQuery / MotherDuck).

---

## Auto-emitted vs. manually-curated metadata

DataHub treats catalog metadata in two layers, and the demo deliberately covers both. Knowing the split is the heart of the talk track.

| Field | Set by | Why |
| --- | --- | --- |
| Schema (columns, types) | `dlt_to_datahub.py` (auto) | Inferred by dlt during load — emitting it costs nothing |
| Container | `dlt_to_datahub.py` (auto) | Group of tables loaded by one pipeline run |
| Lineage | `dlt_to_datahub.py` (auto) | We know the source and destination URNs at emit time |
| Description | `dlt_to_datahub.py` (auto, default) | Falls back to `"Loaded by dlt pipeline <name>..."` if dlt has no description |
| Tags | `dlt_to_datahub.py` (auto, default) | Every emitted dataset gets `dlt-ingested` so users can search "what came from dlt?" |
| **Owners** | **UI (manual)** | Ownership is a human decision — who's accountable for this dataset |
| **Domain** | **UI (manual)** | Business grouping (e.g. "Source Systems", "Marketing") — set by a steward, not a pipeline |
| **Glossary terms** | **UI (manual)** | Maps columns to business concepts (`Customer Email`, `PII`) — needs business context |
| **Documentation (long-form)** | UI (manual, optional) | Helper sets a one-line default; rich Markdown docs are added in the UI |

**Why the split?** Auto-emitted metadata describes *what was loaded* — facts the pipeline knows. Manually-curated metadata describes *what the data means and who owns it* — judgements humans make. DataHub's value comes from holding both in one place.

**To extend auto-emission**, edit `dlt_to_datahub.py`:
```python
# datahub.sdk.Dataset accepts these as constructor kwargs:
ds = Dataset(
    platform=...,
    name=...,
    owners=[CorpUserUrn("alice")],     # auto-set the pipeline owner
    domain=DomainUrn("source-systems"),
    terms=[GlossaryTermUrn("PII")],
    ...
)
```
Use sparingly — the more you auto-emit, the less of the "humans curate the catalog" story you can demo.

---

## How `dlt_to_datahub.py` uses the SDK

The helper is a thin wrapper around DataHub's Python SDK v2 (`datahub.sdk.*`). The shape:

```python
from datahub.sdk.main_client import DataHubClient
from datahub.sdk import Dataset, Container
from datahub.emitter.mcp_builder import DatabaseKey

client = DataHubClient(server="http://localhost:8080")

# 1. Container per pipeline dataset
container = Container(
    container_key=DatabaseKey(platform="duckdb", database="github_data"),
    display_name="github_data",
    subtype="Database",
)
client.entities.upsert(container)

# 2. Dataset per loaded table
ds = Dataset(
    platform="duckdb",
    name="github_data.repos",
    schema=[("id", "BIGINT"), ("name", "VARCHAR"), ...],
    parent_container=container.urn,
)
client.entities.upsert(ds)

# 3. Lineage from GitHub → DuckDB
client.lineage.add_lineage(
    upstream="urn:li:dataset:(urn:li:dataPlatform:github,dlt-hub/repos,PROD)",
    downstream=ds.urn,
)
```

Note: the SDK is marked `ExperimentalWarning`. The import path will move from `datahub.sdk.*` to `datahub.*` once it stabilises — `dlt_to_datahub.py` filters this warning so demo logs stay clean.

---

## Project layout

```
.
├── README.md                 # this file
├── requirements.txt          # dlt[duckdb] + acryl-datahub
├── rest_api_pipeline.py      # dlt source + pipeline + DataHub emit call
├── dlt_to_datahub.py         # local module wrapping datahub.sdk: integrate_dlt_pipeline_with_datahub, create_default_lineage_relationships
├── .dlt/
│   ├── config.toml
│   └── secrets.toml          # GitHub PAT (gitignored)
└── github_pipeline.duckdb    # created on first run
```

---

## Troubleshooting

**`datahub docker quickstart` hangs or fails on Mac (Apple Silicon)**
Allocate ≥ 8 GB RAM in Docker Desktop. Run `datahub docker nuke` and retry.

**`Connection refused` to `localhost:8080`**
Wait — GMS takes ~60 s after `quickstart` returns before it's healthy. `curl localhost:8080/health` should print `GOOD`.

**Pipeline runs but nothing shows up in DataHub**
Check the `datahub_server` URL in `rest_api_pipeline.py` matches the GMS port (`8080`, not the UI `9002`). Look for `aspects emitted` lines in the run log.

**GitHub 401 / 403**
PAT is wrong or expired. Regenerate at https://github.com/settings/tokens and update `.dlt/secrets.toml`.

**Schema not updating after re-run**
dlt's `repos` resource uses `write_disposition="replace"` so schema changes are picked up. `issues` is `append` + incremental, so only new rows arrive — for a schema-evolution demo, run against `repos`.
