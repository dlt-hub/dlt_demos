# Geopolitical Hormuz Dashboard

A marimo dashboard correlating Iran-USA news volume (GDELT), WTI crude oil prices, and Bitcoin prices during the Strait of Hormuz crisis (Jan–Apr 2026).

Built with the [dltHub AI Workbench](https://github.com/dlt-hub/dlthub-ai-workbench) in one afternoon.

## What's included

- `geopolitical_dashboard.py` — marimo dashboard
- `geopolitical_dashboard.pdf` — static snapshot of the dashboard as of Apr 18, 2026 (no setup needed to view)
- `alpha_vantage.duckdb` — WTI oil + BTC price data (snapshot Apr 18, 2026)
- `gdelt.duckdb` — Iran-USA news articles from GDELT (snapshot Apr 18, 2026)

## Run the dashboard

With pip:
```bash
pip install marimo duckdb altair pandas
marimo edit geopolitical_dashboard.py
```

With uv:
```bash
uv run python -m marimo edit geopolitical_dashboard.py
```

## Build your own pipelines

To get fresh data, build your own pipelines using the [dltHub AI Workbench](https://github.com/dlt-hub/dlthub-ai-workbench) — open Claude Code, give it the README, and describe what you want.
