"""GitHub REST API → DuckDB pipeline, with metadata + lineage published to DataHub."""

# mypy: disable-error-code="no-untyped-def,arg-type"

from typing import Optional
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator

from dlt_to_datahub import (
    create_default_lineage_relationships,
    integrate_dlt_pipeline_with_datahub,
)

DLT_PLATFORM_NAME = "dltHub"
DATAHUB_SERVER = "http://localhost:8080"
DATAHUB_UI_URL = "http://localhost:9002"


@dlt.source
def github_source(access_token: Optional[str] = dlt.secrets.value):
    # Optional auth: works with and without secrets
    auth = BearerTokenAuth(token=access_token) if access_token else None

    client = RESTClient(
        base_url="https://api.github.com",
        auth=auth,
        paginator=HeaderLinkPaginator(),
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    # Define a resource which fetches repos data
    @dlt.resource(name="repos", write_disposition="replace")
    def repos():
        for page in client.paginate("orgs/dlt-hub/repos"):
            yield page

    # Define a resource which fetches issues data (incremental by updated_at timestamp)
    @dlt.resource(name="issues", write_disposition="append")
    def issues(
        updated_at=dlt.sources.incremental(
            "updated_at",
            initial_value="2026-01-01T00:00:00Z",
        )
    ):
        for page in client.paginate(
            "repos/dlt-hub/dlt/issues",
            params={
                "state": "open",
                "sort": "updated",
                "direction": "desc",
                "since": updated_at.start_value,
                "per_page": "100",
            },
        ):
            yield page

    return [repos, issues]


def run_source() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="github_pipeline",
        destination="duckdb",
        dataset_name="github_data",
        progress="log",
    )

    load_info = pipeline.run(github_source())
    print(load_info)  # noqa: T201

    lineage_relationships = create_default_lineage_relationships(pipeline.dataset_name)

    result = integrate_dlt_pipeline_with_datahub(
        pipeline=pipeline,
        platform_name=DLT_PLATFORM_NAME,
        datahub_server=DATAHUB_SERVER,
        datahub_ui_url=DATAHUB_UI_URL,
        create_container=True,
        add_lineage=True,
        lineage_relationships=lineage_relationships,
    )

    print(f"\nEmitted {len(result['datasets'])} datasets to DataHub.")  # noqa: T201
    if result["container"]:
        print(f"Container: {result['container']['url']}")  # noqa: T201
    for upstream, downstream in result["lineage_edges"]:
        print(f"Lineage: {upstream}  ->  {downstream}")  # noqa: T201


if __name__ == "__main__":
    run_source()