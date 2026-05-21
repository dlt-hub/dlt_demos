"""Emit metadata from a dlt pipeline run to DataHub.

Public API:
    create_default_lineage_relationships(dataset_name) -> {table_name: upstream_urn}
    integrate_dlt_pipeline_with_datahub(pipeline, ...) -> {"container": ..., "datasets": [...]}
"""

from __future__ import annotations

import warnings
from typing import Dict, List, Optional, Tuple

# The datahub.sdk module is marked experimental and emits a warning on import.
# Suppress it so demo logs stay readable.
warnings.filterwarnings("ignore", message=r".*datahub SDK.*")

from datahub.emitter.mcp_builder import DatabaseKey
from datahub.metadata.urns import DatasetUrn, TagUrn
from datahub.sdk import Container, Dataset
from datahub.sdk.main_client import DataHubClient

# dlt creates these internal tables alongside user data; we register them in DataHub
# under the same container so the picture is complete, but they're not "interesting".
_DLT_INTERNAL_TABLES = {"_dlt_loads", "_dlt_pipeline_state", "_dlt_version"}

# dlt -> SQL type names that DataHub's resolver recognises.
_DLT_TO_SQL_TYPE = {
    "text": "VARCHAR",
    "bigint": "BIGINT",
    "double": "DOUBLE",
    "bool": "BOOLEAN",
    "timestamp": "TIMESTAMP",
    "date": "DATE",
    "time": "TIME",
    "decimal": "DECIMAL",
    "json": "JSON",
    "binary": "BLOB",
    "wei": "VARCHAR",
}


def _columns_for_table(pipeline, table_name: str) -> List[Tuple[str, str]]:
    schema = pipeline.default_schema
    table = schema.tables.get(table_name)
    if not table:
        return []
    fields: List[Tuple[str, str]] = []
    for col_name, col in table.get("columns", {}).items():
        sql_type = _DLT_TO_SQL_TYPE.get(col.get("data_type") or "text", "VARCHAR")
        fields.append((col_name, sql_type))
    return fields


def create_default_lineage_relationships(dataset_name: str) -> Dict[str, str]:
    """Return upstream-URN-by-table-name for the GitHub demo source.

    The demo pulls from two GitHub REST endpoints, so we model each as an upstream
    Dataset under the `github` platform. Edit this map when pointing the pipeline
    at a different source.
    """
    _ = dataset_name  # unused for this hardcoded demo map; kept for API symmetry
    return {
        "repos": "urn:li:dataset:(urn:li:dataPlatform:github,dlt-hub/repos,PROD)",
        "issues": "urn:li:dataset:(urn:li:dataPlatform:github,dlt-hub/dlt/issues,PROD)",
    }


def integrate_dlt_pipeline_with_datahub(
    *,
    pipeline,
    platform_name: str = "dltHub",
    datahub_server: str = "http://localhost:8080",
    datahub_ui_url: str = "http://localhost:9002",
    create_container: bool = True,
    add_lineage: bool = True,
    lineage_relationships: Optional[Dict[str, str]] = None,
) -> dict:
    """Emit a container, one Dataset per loaded table, and source→destination lineage.

    Returns:
        {
            "container": {"urn": str, "url": str} | None,
            "datasets": [str, ...],          # dataset URNs
            "lineage_edges": [(upstream, downstream), ...],
        }
    """
    _ = platform_name  # surfaced in container description; kept as an explicit knob

    client = DataHubClient(server=datahub_server)
    destination_platform = pipeline.destination.destination_name
    dataset_name = pipeline.dataset_name

    container = None
    container_info = None
    if create_container:
        key = DatabaseKey(platform=destination_platform, database=dataset_name)
        container = Container(
            container_key=key,
            display_name=dataset_name,
            description=(
                f"dlt pipeline `{pipeline.pipeline_name}` "
                f"(orchestrator: {platform_name}, destination: {destination_platform})"
            ),
            subtype="Database",
        )
        client.entities.upsert(container)
        container_urn = str(container.urn)
        container_info = {
            "urn": container_urn,
            "url": f"{datahub_ui_url}/container/{container_urn}",
        }

    dataset_urns: List[str] = []
    lineage_edges: List[Tuple[str, str]] = []

    schema = pipeline.default_schema
    for table_name, table_def in schema.tables.items():
        if table_name in _DLT_INTERNAL_TABLES:
            continue
        columns = _columns_for_table(pipeline, table_name)
        default_description = (
            f"Loaded by dlt pipeline `{pipeline.pipeline_name}` "
            f"into `{destination_platform}://{dataset_name}.{table_name}`."
        )
        ds = Dataset(
            platform=destination_platform,
            name=f"{dataset_name}.{table_name}",
            schema=columns or None,
            description=table_def.get("description") or default_description,
            tags=[TagUrn("dlt-ingested")],
            parent_container=container.urn if container is not None else None,
        )
        client.entities.upsert(ds)
        dataset_urns.append(str(ds.urn))

        if add_lineage:
            parent = (table_def or {}).get("parent")
            if parent:
                # Child table (e.g. `repos__topics`) → parent table (`repos`)
                # within the destination platform.
                upstream = (
                    f"urn:li:dataset:(urn:li:dataPlatform:{destination_platform},"
                    f"{dataset_name}.{parent},PROD)"
                )
                client.lineage.add_lineage(upstream=upstream, downstream=ds.urn)
                lineage_edges.append((upstream, str(ds.urn)))
            elif lineage_relationships and table_name in lineage_relationships:
                # Root table → external upstream (e.g. GitHub API endpoint).
                # DataHub's UI hides lineage edges that point at "ghost" URNs
                # (URNs with no entity behind them). Upsert a minimal Dataset
                # for the upstream so the edge renders in the lineage graph.
                upstream = lineage_relationships[table_name]
                upstream_urn = DatasetUrn.from_string(upstream)
                stub = Dataset(
                    platform=upstream_urn.platform,
                    name=upstream_urn.name,
                    env=upstream_urn.env,
                    description=f"Source for {table_name} (registered as a lineage stub).",
                )
                client.entities.upsert(stub)
                client.lineage.add_lineage(upstream=upstream, downstream=ds.urn)
                lineage_edges.append((upstream, str(ds.urn)))

    return {
        "container": container_info,
        "datasets": dataset_urns,
        "lineage_edges": lineage_edges,
    }
