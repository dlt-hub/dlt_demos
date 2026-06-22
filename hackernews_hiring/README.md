# Hacker News Who's Hiring: Data Stack Analysis

A monthly data pipeline and interactive dashboard that reads [Y Combinator's Hacker News](https://news.ycombinator.com) ["Ask HN: Who is Hiring?"](https://news.ycombinator.com/item?id=48357725) thread, extracts tools and technologies from every job post using Claude Haiku, stores the results in MotherDuck, and visualises them in a live marimo notebook deployed on dltHub Platform.

**Live dashboard:** https://app.dlthub.com/n/47c7dc76-acbb-4226-9ac7-bc09bbc82300/ea69acba-819f-43c8-940f-edabee4de040

---

## What it does

Each month, Hacker News hosts a "Who is Hiring?" thread with hundreds of job posts from companies. This project:

1. **Fetches** the latest thread via the [HN Algolia API](https://hn.algolia.com/api)
2. **Extracts** tool and technology mentions from each job post using Claude Haiku — only new posts are processed on each run (incremental, merge-based)
3. **Stores** structured data (job posts, named tools, custom tooling notes) in MotherDuck
4. **Visualises** the results as an interactive marimo dashboard deployed on dltHub

The dashboard shows:
- Top tools by role type — data/ML/analytics vs platform/infra/devops
- AI/LLM vs cloud vs data stack category breakdown
- Cloud provider (AWS, GCP, Azure) trends over time
- AI coding tools (Cursor, Copilot, Claude, Codex, Gemini) adoption over time
- Word clouds by role type
- What companies are building from scratch

---

## Tech stack

| Component | Tool |
|-----------|------|
| Pipeline | [dlt](https://dlthub.com/docs/intro) |
| LLM extraction | Claude Haiku (via Anthropic API) |
| Warehouse | [MotherDuck](https://motherduck.com) — started with local DuckDB, migrated to MotherDuck for cloud deployment as suggested by Claude on dltHub AI Workbench |
| Dashboard | [marimo](https://marimo.io) + [Altair](https://altair-viz.github.io) — when you use dltHub AI Workbench with an AI coding assistant (Claude, Codex, Cursor), it generates marimo notebooks automatically when you use the skills to explore data or create notebooks, using Altair for charts |
| Deployment | [dltHub Platform](https://dlthub.com/docs/hub/getting-started/platform-tutorial) |

---

## Prerequisites

- Python 3.10–3.14
- [uv](https://docs.astral.sh/uv/) (recommended package manager)
- An [Anthropic API key](https://console.anthropic.com)
- A [MotherDuck](https://motherduck.com) account (free tier works)
- A [dltHub](https://dlthub.com) account (free trial available)

> Any of these are freely swappable — use dltHub AI Workbench in your terminal with Claude, Codex, or Cursor to swap in a different LLM, warehouse, or data source with minimal code changes.

---

## Setup

### 1. Clone and install

```bash
git clone <this-repo>
cd hackernews
uv sync
```

### 2. Configure credentials

Add your secrets to `.dlt/prod.secrets.toml` (for the pipeline) and `.dlt/access.secrets.toml` (for the dashboard):

```toml
anthropic_api_key = "your-anthropic-api-key"

[destination.warehouse.credentials]
password = "your-motherduck-token"
```

And configure the destination type in `.dlt/prod.config.toml` and `.dlt/access.config.toml`:

```toml
[destination.warehouse]
destination_type = "motherduck"
```

For local development with DuckDB instead, set in `.dlt/dev.config.toml`:

```toml
[destination.warehouse]
destination_type = "duckdb"
```

> **Note:** `*.secrets.toml` files are gitignored. Never commit secrets to version control. See [credential setup docs](https://dlthub.com/docs/hub/pipeline-operations/workspace-setup).

### 3. Run locally

```bash
uv run python hackernews_hiring_pipeline.py
```

This fetches the current "Who is Hiring?" thread and runs Claude Haiku on each job post. Subsequent runs are incremental — only new comments are processed.

### 4. View the dashboard locally

```bash
uv run marimo edit hackernews_hiring_dashboard.py
```

---

## Deploy to dltHub

dltHub is a managed platform for running dlt pipelines and marimo notebooks in the cloud. It handles scheduling, secrets, monitoring, and public sharing. See the [platform tutorial](https://dlthub.com/docs/hub/getting-started/platform-tutorial) and [deployment reference](https://dlthub.com/docs/hub/pipeline-operations/deployments).

> dlt is free and open source. dltHub is a paid platform — see [pricing](https://dlthub.com/pricing). A 14-day free trial is available.

### 1. Install and log in

```bash
uvx dlthub-init@latest   # initialises workspace if not already done
dlthub login
dlthub workspace connect
```

### 2. Sync credentials to the platform

```bash
dlthub workspace configuration sync
```

This securely syncs your `prod` and `access` profile secrets to the platform runtime.

### 3. Deploy

```bash
dlthub deploy
```

This registers all jobs defined in `__deployment__.py`. The pipeline is scheduled to run on the 1st and 15th of each month at 9am UTC.

### 4. Run the pipeline

```bash
dlthub run run_pipeline
```

### 5. Serve the dashboard

```bash
dlthub serve hackernews_hiring_dashboard
```

### 6. Share publicly

```bash
dlthub job publish hackernews_hiring_dashboard
```

---

## Customising for different roles or APIs

The easiest way to modify this project is to use an AI coding assistant (Claude, Codex, Cursor, or similar) with the codebase open:

- **Different role filters** — the bar charts and word clouds filter by role type using SQL `LIKE` patterns in `hackernews_hiring_dashboard.py`. Add or change the patterns to focus on different roles (e.g. `%security%`, `%backend%`).
- **Different tools to track** — Chart 4 (AI coding tools over time) has a hardcoded list. Add any tool name that Claude Haiku would have extracted.
- **Different data source** — the pipeline uses the [HN Algolia API](https://hn.algolia.com/api) and HN Firebase API. Swap these out for any other job board or API by replacing `hackernews_hiring_pipeline.py`. dlt supports [REST APIs, SQL databases, files, and more](https://dlthub.com/docs/intro).
- **Different LLM** — the extraction prompt in `hackernews_hiring_pipeline.py` uses Claude Haiku. Swap the `anthropic` client for any other provider.

For deeper changes — adding new charts, new data sources, or transformations — use [dltHub AI Workbench](https://dlthub.com/docs/hub/getting-started/platform-tutorial), which provides an agent-assisted development environment connected directly to your pipeline data.

---

## Project structure

```
hackernews/
├── hackernews_hiring_pipeline.py   # dlt pipeline: fetches HN data, runs Claude Haiku
├── hackernews_hiring_dashboard.py  # marimo dashboard: charts and word clouds
├── __deployment__.py               # registers jobs for dltHub Platform
├── pyproject.toml                  # dependencies
└── .dlt/
    ├── dev.config.toml             # local DuckDB config
    ├── prod.config.toml            # production MotherDuck config
    ├── access.config.toml          # dashboard MotherDuck config
    ├── prod.secrets.toml           # production secrets (gitignored)
    └── access.secrets.toml         # dashboard secrets (gitignored)
```

---

## Getting started with dltHub

If you want to build your own pipeline and dashboard from scratch, dltHub provides a full AI-assisted workflow.

**Start a new playground (best for learning):**

```bash
uvx dlthub-start@latest
```

This scaffolds a fresh workspace with example pipelines and connects to the platform. Run it in your terminal — it walks you through authentication interactively.

**Add dltHub to an existing project:**

```bash
uvx dlthub-init@latest
```

**Install AI Workbench toolkits** — these are the skills Claude / Codex / Cursor use to build pipelines, notebooks, and transformations:

```bash
dlthub ai toolkit install rest-api-pipeline      # ingest from any REST API
dlthub ai toolkit install data-exploration       # explore data, build charts
dlthub ai toolkit install dlthub-platform        # deploy and schedule on dltHub
dlthub ai toolkit install transformations        # model and transform data
dlthub ai toolkit install data-quality           # add data quality checks
```

Once a toolkit is installed, open your project in Claude Code, Cursor, or any AI coding assistant and describe what you want to build. The toolkits provide the skills and rules the assistant uses to generate production-ready code.

See the [installation guide](https://dlthub.com/docs/hub/getting-started/installation) and [platform tutorial](https://dlthub.com/docs/hub/getting-started/platform-tutorial) to get set up.

---

## Links

- [dltHub Platform Tutorial](https://dlthub.com/docs/hub/getting-started/platform-tutorial)
- [dltHub Installation](https://dlthub.com/docs/hub/getting-started/installation)
- [dlt vs dltHub explained](https://dlthub.com/docs/hub/getting-started/oss-and-dlthub)
- [Deployment reference](https://dlthub.com/docs/hub/pipeline-operations/deployments)
- [Credentials & workspace setup](https://dlthub.com/docs/hub/pipeline-operations/workspace-setup)
- [dltHub pricing](https://dlthub.com/pricing)
- [HN Algolia API](https://hn.algolia.com/api)
