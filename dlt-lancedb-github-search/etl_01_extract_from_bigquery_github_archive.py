from __future__ import annotations

import logging
from typing import Any, Iterator

import dlt
from dlt.sources.credentials import GcpServiceAccountCredentials
from google.cloud import bigquery

PIPELINE_NAME = "github_stars_etl"
DATASET_NAME = "github_stars"

logger = logging.getLogger(__name__)


@dlt.resource(primary_key=["repo_name", "month_id"], write_disposition="append")
def repos_with_stars(
    credentials: GcpServiceAccountCredentials = dlt.secrets.value,
    data_project_id: str = dlt.config.value,
    dataset_id: str = dlt.config.value,
    billing_project_id: str = dlt.config.value,
    min_stars: int = dlt.config.value,
    start_month_id: str = dlt.config.value,
    end_month_id: str = dlt.config.value,
    month_cursor: dlt.sources.incremental[
        str
    ] = dlt.sources.incremental(  # trunk-ignore(pyright/reportAssignmentType)
        "month_id",
        initial_value="201501",
    ),
) -> Iterator[dict[str, Any]]:
    start_year, start_month = int(start_month_id[:4]), int(start_month_id[4:])
    end_year, end_month = int(end_month_id[:4]), int(end_month_id[4:])
    m0 = start_year * 12 + start_month - 1
    m1 = end_year * 12 + end_month - 1
    months = [(m // 12, m % 12 + 1) for m in range(m0, m1 + 1)]

    client = bigquery.Client(
        project=billing_project_id,
        credentials=credentials.to_native_credentials(),
    )

    logger.info("Processing %d months", len(months))

    for year, month in months:
        month_id = f"{year}{month:02d}"

        if month_cursor.last_value and month_id <= month_cursor.last_value:
            logger.info("Skipping month %s (already processed)", month_id)
            continue

        logger.info("Querying BigQuery for month %s", month_id)

        query = f"""
        SELECT
          t.repo.name as repo_name,
          COUNT(t.id) AS star_count
        FROM
          `{data_project_id}.{dataset_id}.{year}{month:02d}` AS t
        WHERE
          t.type = 'WatchEvent'
          AND DATE_TRUNC(t.created_at, MONTH) = TIMESTAMP '{year}-{month:02d}-01'
        GROUP BY
          t.repo.name
        HAVING
          COUNT(t.id) > {min_stars}
        ORDER BY
          COUNT(t.id) DESC
        """

        row_count = 0
        for row in client.query(query).result():
            row_count += 1
            yield {
                "repo_name": row.repo_name,
                "star_count": row.star_count,
                "year": year,
                "month": month,
                "month_id": month_id,
            }

        logger.info("Month %s: yielded %d repos", month_id, row_count)


def main() -> None:
    logger.info("Starting pipeline %s", PIPELINE_NAME)

    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination="filesystem",
        dataset_name=DATASET_NAME,
    )

    load_info = pipeline.run(repos_with_stars())
    logger.info("Pipeline complete")
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    main()
