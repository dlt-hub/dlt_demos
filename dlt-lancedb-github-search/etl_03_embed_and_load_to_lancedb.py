from __future__ import annotations

import dlt
from dlt.destinations.adapters import lancedb_adapter

from etl_02_enrich_github_repos_with_descriptions_from_parallel import (
    PIPELINE_NAME as SOURCE_PIPELINE_NAME,
)
from etl_02_enrich_github_repos_with_descriptions_from_parallel import (
    TABLE_NAME as SOURCE_TABLE_NAME,
)

PIPELINE_NAME: str = "lancedb_embeddings"
LANCEDB_TABLE_NAME: str = "repos"
CHUNK_SIZE: int = 10000


def main() -> None:
    source_pipeline = dlt.attach(SOURCE_PIPELINE_NAME)
    lancedb_pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination="lancedb",
    )

    table = source_pipeline.dataset().table(SOURCE_TABLE_NAME)

    load_info = lancedb_pipeline.run(
        lancedb_adapter(
            table.iter_arrow(chunk_size=CHUNK_SIZE),
            embed="description",
        ),
        table_name=LANCEDB_TABLE_NAME,
        write_disposition={"disposition": "merge", "strategy": "upsert"},
        primary_key="repo_name",
    )

    print(f"Pipeline load info: {load_info}")  # noqa: T201


if __name__ == "__main__":
    main()
