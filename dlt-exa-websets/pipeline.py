# trunk-ignore-all(pyright/reportUntypedFunctionDecorator)
#!/usr/bin/env python3
"""Exa Webset -> dlt -> MotherDuck pipeline.

Creates an Exa Webset, polls until complete, loads raw items via dlt, then
attaches the dataset and runs Ibis transforms into analytics tables.

Only EXA_API_KEY is required. Everything else has sensible defaults so you
can run the pipeline immediately:

    export EXA_API_KEY="..."
    python scripts/dlt_exa_websets/pipeline.py

Environment variables:
  EXA_API_KEY         - Exa API key (required)
  EXA_QUERY           - Search query (default: "AI startups in San Francisco founded after 2020")
  EXA_ENTITY_TYPE     - company | person | article | research_paper | custom (default: company)
  EXA_COUNT           - Max items to collect (default: 10)
  EXA_CRITERIA        - JSON array of criterion strings (optional)
  EXA_ENRICHMENTS     - JSON array of enrichment dicts (optional)
  MOTHERDUCK_TOKEN    - MotherDuck service token (optional; falls back to local DuckDB)
  MOTHERDUCK_DATABASE - Database name (default: exa-websets)
"""

from __future__ import annotations

# ── Imports ──────────────────────────────────────────────────────────────────

import hashlib
import json
import os
import sys
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Literal

import dlt
import ibis.expr.types as ir
import requests
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

# ── Constants ────────────────────────────────────────────────────────────────

BASE_URL = "https://api.exa.ai/websets/v0"
PAGE_SIZE = 100
POLL_INTERVAL = 10
POLL_TIMEOUT = 3600
REQUEST_TIMEOUT = 30

DEFAULT_QUERY = "AI startups in San Francisco founded after 2020"
DEFAULT_ENTITY_TYPE = "company"
DEFAULT_COUNT = 10

MOTHERDUCK_DATABASE = os.environ.get("MOTHERDUCK_DATABASE", "exa-websets")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PIPELINES_DIR = str(PROJECT_ROOT / "tmp" / "exa_websets" / "pipelines")


# ── Pydantic Models ─────────────────────────────────────────────────────────


class CompanyRef(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    location: str | None = None


class CompanyProperties(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    location: str | None = None
    employees: int | None = None
    industry: str | None = None
    about: str | None = None
    logo_url: str | None = None


class PersonProperties(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    location: str | None = None
    position: str | None = None
    company: CompanyRef | None = None
    picture_url: str | None = None


class ArticleProperties(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str
    author: str | None = None
    published_at: str | None = None


class Reference(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    url: str
    title: str | None = None


class Evaluation(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    criterion: str
    reasoning: str
    satisfied: Literal["yes", "no", "unclear"]
    references: list[Reference] = []


class EnrichmentResult(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    enrichment_id: str
    status: Literal["pending", "completed", "canceled"]
    format: Literal["text", "date", "number", "options", "email", "phone", "url"]
    result: list[str] | None = None
    reasoning: str | None = None
    references: list[Reference] = []


class WebsetItemProperties(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["company", "person", "article", "research_paper", "custom"]
    url: str
    description: str
    content: str | None = None
    company: CompanyProperties | None = None
    person: PersonProperties | None = None
    article: ArticleProperties | None = None
    research_paper: ArticleProperties | None = None
    custom: ArticleProperties | None = None


class WebsetItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    source: str
    source_id: str
    webset_id: str
    properties: WebsetItemProperties
    evaluations: list[Evaluation] = []
    enrichments: list[EnrichmentResult] = []
    created_at: str
    updated_at: str


# ── Exa HTTP Client ─────────────────────────────────────────────────────────


class ExaWebsetClient:
    """Thin wrapper around the Exa Websets v0 REST API."""

    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Execute request with retry on 429/5xx (3 attempts, exponential backoff)."""
        url = f"{BASE_URL}/{path.lstrip('/')}"
        backoff = 2
        last_resp: requests.Response | None = None

        for attempt in range(3):
            resp = self.session.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
            if resp.status_code == 429 or resp.status_code >= 500:
                last_resp = resp
                if attempt < 2:
                    print(
                        f"  Retry {attempt + 1}/3 after {resp.status_code}, sleeping {backoff}s"
                    )
                    time.sleep(backoff)
                    backoff *= 2
                    continue
            return resp

        # All retries exhausted — return last response for caller to handle
        assert last_resp is not None  # noqa: S101
        return last_resp

    def create_webset(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST /v0/websets. On 409, return existing webset."""
        resp = self._request("POST", "/websets", json=body)
        if resp.status_code == 409:
            return resp.json()
        resp.raise_for_status()
        return resp.json()

    def get_webset(self, webset_id: str) -> dict[str, Any]:
        """GET /v0/websets/{id}."""
        resp = self._request("GET", f"/websets/{webset_id}")
        resp.raise_for_status()
        return resp.json()

    def list_items(
        self, webset_id: str, limit: int = 100, cursor: str | None = None
    ) -> dict[str, Any]:
        """GET /v0/websets/{id}/items with pagination."""
        params: dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        resp = self._request("GET", f"/websets/{webset_id}/items", params=params)
        resp.raise_for_status()
        return resp.json()

    def get_enrichment(self, webset_id: str, enrichment_id: str) -> dict[str, Any]:
        """GET /v0/websets/{id}/enrichments/{eid}."""
        resp = self._request("GET", f"/websets/{webset_id}/enrichments/{enrichment_id}")
        resp.raise_for_status()
        return resp.json()

    def create_or_resume(
        self,
        query: str,
        entity_type: str,
        count: int,
        criteria: list[str] | None,
        enrichments: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        """Build request body, create webset, handle 409 resume."""
        hash_input = json.dumps(
            {
                "query": query,
                "entity_type": entity_type,
                "count": count,
                "criteria": criteria or None,
                "enrichments": enrichments or None,
            },
            sort_keys=True,
        )
        external_id = f"elvis-{hashlib.sha256(hash_input.encode()).hexdigest()[:12]}"
        body: dict[str, Any] = {
            "search": {
                "query": query,
                "entity": {"type": entity_type},
                "count": count,
            },
            "externalId": external_id,
        }
        if criteria:
            body["search"]["criteria"] = [{"description": c} for c in criteria]
        if enrichments:
            body["enrichments"] = enrichments
        return self.create_webset(body)

    def poll_until_idle(
        self,
        webset_id: str,
        timeout: int = POLL_TIMEOUT,
        interval: int = POLL_INTERVAL,
    ) -> dict[str, Any]:
        """Block until status=='idle'. Log progress. Raise TimeoutError."""
        start = time.time()
        while True:
            webset = self.get_webset(webset_id)
            status = webset.get("status", "unknown")

            if status == "idle":
                print(f"  Webset {webset_id} is idle (complete).")
                return webset

            if status == "paused":
                msg = f"Webset {webset_id} is paused — check the Exa dashboard."
                raise RuntimeError(msg)

            # Log progress from the first search object
            searches = webset.get("searches", [{}])
            progress = searches[0].get("progress", {}) if searches else {}
            found = progress.get("found", "?")
            analyzed = progress.get("analyzed", "?")
            completion = progress.get("completion", "?")
            print(
                f"  Status: {status} | Found: {found}"
                f" | Analyzed: {analyzed} | Completion: {completion}%"
            )

            elapsed = time.time() - start
            if elapsed > timeout:
                msg = f"Webset {webset_id} not idle after {timeout}s"
                raise TimeoutError(msg)

            time.sleep(interval)

    def get_enrichment_map(
        self, webset_id: str, enrichment_ids: list[str]
    ) -> dict[str, str]:
        """Return {enrichment_id: description} for all enrichments."""
        mapping: dict[str, str] = {}
        for eid in enrichment_ids:
            data = self.get_enrichment(webset_id, eid)
            mapping[eid] = data.get("description", "")
        return mapping


# ── Item Normalization ───────────────────────────────────────────────────────


ENTITY_BLOCK_FIELDS = ("company", "person", "article", "research_paper", "custom")


def normalize_item(item: WebsetItem, enrichment_map: dict[str, str]) -> dict[str, Any]:
    """Flatten a parsed WebsetItem into a dlt-friendly dict.

    Generic across entity types: hoists whichever entity block (company,
    person, article, research_paper, custom) is populated into top-level
    columns without prefixes. Switching entity_type produces a different
    column set automatically.

    Nested dicts (e.g. person.company = {name, location}) are flattened
    one level with `parent_child` naming.
    """
    props = item.properties
    row: dict[str, Any] = {
        # Top-level
        "id": item.id,
        "source": item.source,
        "source_id": item.source_id,
        "webset_id": item.webset_id,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        # From properties
        "entity_type": props.type,
        "url": props.url,
        "description": props.description,
        "content": props.content,
    }

    # Hoist whichever entity block is populated. Use model_dump so unknown
    # nested dicts still flatten reasonably without enumerating every field.
    for block_name in ENTITY_BLOCK_FIELDS:
        block = getattr(props, block_name, None)
        if block is None:
            continue
        for key, value in block.model_dump(by_alias=False).items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    row[f"{key}_{sub_key}"] = sub_value
            else:
                row[key] = value

    # Enrichments — add description from map, serialize to dicts
    row["enrichments"] = [
        {
            **e.model_dump(by_alias=False),
            "description": enrichment_map.get(e.enrichment_id, ""),
        }
        for e in item.enrichments
    ]

    # Evaluations — serialize to dicts
    row["evaluations"] = [e.model_dump(by_alias=False) for e in item.evaluations]

    return row


# ── dlt Resources (Stage 1 — Ingest) ────────────────────────────────────────


@dlt.resource(name="webset_items", write_disposition="merge", primary_key="id")
def webset_items_resource(
    client: ExaWebsetClient,
    webset_id: str,
    enrichment_map: dict[str, str],
) -> Iterator[dict[str, Any]]:
    """Cursor-paginate all items from a completed webset."""
    cursor = None
    while True:
        page = client.list_items(webset_id, limit=PAGE_SIZE, cursor=cursor)
        for raw_item in page["data"]:
            parsed = WebsetItem.model_validate(raw_item)
            yield normalize_item(parsed, enrichment_map)
        if not page.get("hasMore", False):
            break
        cursor = page.get("nextCursor")


@dlt.resource(name="webset_metadata", write_disposition="append")
def webset_metadata_resource(
    webset: dict[str, Any],
    enrichment_map: dict[str, str],
) -> Iterator[dict[str, Any]]:
    """Emit a single metadata row for this webset run."""
    # Webset response shape: `searches` is an array — take the first.
    searches = webset.get("searches") or []
    first_search = searches[0] if searches else {}
    entity = first_search.get("entity") or {}
    yield {
        "id": webset["id"],
        "title": webset.get("title"),
        "external_id": webset.get("externalId"),
        "status": webset["status"],
        "entity_type": entity.get("type"),
        "query": first_search.get("query"),
        "enrichment_count": len(enrichment_map),
        "enrichment_descriptions": json.dumps(list(enrichment_map.values())),
        "created_at": webset.get("createdAt"),
        "updated_at": webset.get("updatedAt"),
    }


# ── Ibis Transforms (Stage 2 — Analytics) ───────────────────────────────────


def transform_entities(dataset: dlt.Dataset) -> ir.Table:
    """Pass-through analytics view of webset_items.

    Generic across entity types — whatever columns the ingest stage produced
    (company, person, article, ...) are kept as-is. Drop dlt housekeeping
    columns so the analytics table is clean.
    """
    items = dataset["webset_items"].to_ibis()
    keep = [c for c in items.columns if not c.startswith("_dlt_")]
    return items.select(*keep)


def transform_enrichment_summary(dataset: dlt.Dataset) -> ir.Table:
    """Group enrichments by enrichment_id/status, aggregate counts."""
    enr = dataset["webset_items__enrichments"].to_ibis()
    return enr.group_by("enrichment_id", "status", "format").aggregate(
        total_count=enr.count(),
        completed_count=(enr.status == "completed").cast("int64").sum(),
    )


# ── Pipeline Orchestration ──────────────────────────────────────────────────


def _parse_config() -> dict[str, Any]:
    """Read pipeline configuration from environment variables.

    Only EXA_API_KEY is required. Everything else has sensible defaults.
    """
    if not os.environ.get("EXA_API_KEY"):
        print("ERROR: EXA_API_KEY env var is required.", file=sys.stderr)
        raise SystemExit(1)

    query = os.environ.get("EXA_QUERY", DEFAULT_QUERY)
    entity_type = os.environ.get("EXA_ENTITY_TYPE", DEFAULT_ENTITY_TYPE)
    count = int(os.environ.get("EXA_COUNT", str(DEFAULT_COUNT)))

    criteria_raw = os.environ.get("EXA_CRITERIA")
    criteria: list[str] | None = json.loads(criteria_raw) if criteria_raw else None

    enrichments_raw = os.environ.get("EXA_ENRICHMENTS")
    enrichments: list[dict[str, Any]] | None = (
        json.loads(enrichments_raw) if enrichments_raw else None
    )

    use_motherduck = bool(os.environ.get("MOTHERDUCK_TOKEN"))
    if not use_motherduck:
        print("MOTHERDUCK_TOKEN not set — loading to local DuckDB instead.")

    return {
        "query": query,
        "entity_type": entity_type,
        "count": count,
        "criteria": criteria,
        "enrichments": enrichments,
        "use_motherduck": use_motherduck,
    }


def _make_destination(use_motherduck: bool) -> Any:
    """Build dlt destination — MotherDuck when token is available, else local DuckDB."""
    if use_motherduck:
        creds = f"md:///{MOTHERDUCK_DATABASE}?token={os.environ['MOTHERDUCK_TOKEN']}"
        return dlt.destinations.motherduck(credentials=creds)
    return dlt.destinations.duckdb(
        credentials=str(PROJECT_ROOT / "tmp" / "exa_websets" / "exa_websets.duckdb")
    )


def run_ingest(client: ExaWebsetClient, config: dict[str, Any]) -> dlt.Pipeline:
    """Stage 1: Create/resume webset, poll, paginate, load items."""
    webset = client.create_or_resume(
        query=config["query"],
        entity_type=config["entity_type"],
        count=config["count"],
        criteria=config["criteria"],
        enrichments=config["enrichments"],
    )
    webset_id = webset["id"]
    print(f"  Webset ID: {webset_id} | Status: {webset.get('status')}")

    # Poll until all searches and enrichments complete
    webset = client.poll_until_idle(webset_id)

    # Collect enrichment IDs from the webset response
    enrichment_ids = [e["id"] for e in webset.get("enrichments", [])]
    enrichment_map = client.get_enrichment_map(webset_id, enrichment_ids)

    pipeline = dlt.pipeline(
        pipeline_name="exa_webset_ingest",
        destination=_make_destination(config["use_motherduck"]),
        dataset_name="exa_websets_raw",
        pipelines_dir=PIPELINES_DIR,
    )

    load_info = pipeline.run(
        [
            webset_items_resource(client, webset_id, enrichment_map),
            webset_metadata_resource(webset, enrichment_map),
        ]
    )
    print("── ingest load info ──")
    print(load_info)

    return pipeline


def run_transform(ingest_pipeline: dlt.Pipeline, *, use_motherduck: bool) -> None:
    """Stage 2: Attach to raw dataset, run Ibis transforms, load analytics."""
    raw_dataset = ingest_pipeline.dataset()

    transform_pipeline = dlt.pipeline(
        pipeline_name="exa_webset_transform",
        destination=_make_destination(use_motherduck),
        dataset_name="exa_websets_analytics",
        pipelines_dir=PIPELINES_DIR,
    )

    transforms: dict[str, Any] = {
        "entities": transform_entities,
        "enrichment_summary": transform_enrichment_summary,
    }

    for table_name, transform_fn in transforms.items():
        try:
            ibis_expr = transform_fn(raw_dataset)
            transform_pipeline.run(
                ibis_expr.to_pyarrow_batches(),
                table_name=table_name,
                write_disposition="replace",
            )
            print(f"  Loaded transform table: {table_name}")
        except Exception as exc:  # noqa: BLE001
            print(f"  Skipping {table_name}: {exc}")

    print("── transform complete ──")


def run() -> None:
    """Main: resolve env vars, run ingest, run transform."""
    config = _parse_config()
    client = ExaWebsetClient(os.environ["EXA_API_KEY"])

    query_preview = config["query"][:80]
    print(f"Creating Exa Webset: {query_preview}...")

    ingest_pipeline = run_ingest(client, config)

    # Check if any items were loaded
    try:
        raw_dataset = ingest_pipeline.dataset()
        items_table = raw_dataset["webset_items"].to_ibis()
        item_count = items_table.count().execute()
    except Exception:  # noqa: BLE001
        item_count = 0

    if item_count == 0:
        print("No items loaded — skipping transforms.")
        return

    print(f"Loaded {item_count} items. Running transforms...")
    run_transform(ingest_pipeline, use_motherduck=config["use_motherduck"])
    print("Done.")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run()
