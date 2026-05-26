from __future__ import annotations

import logging
import os
import time
from typing import Iterator

import dlt
from dlthub.common.license.license import create_self_signed_license

os.environ["RUNTIME__LICENSE"] = create_self_signed_license(
    "dlthub.data_quality dlthub.destinations.iceberg dlthub.transformation"
)
from parallel import Parallel, RateLimitError

from etl_01_extract_from_bigquery_github_archive import (
    PIPELINE_NAME as GITHUB_STARS_PIPELINE_NAME,
)
from models import StructuredOutput, system_prompt

# ---------------------------------------------------------------------------
# Section 1: Constants
# ---------------------------------------------------------------------------

PIPELINE_NAME: str = "parallel_enrichment"
TABLE_NAME: str = "repos"
RESOURCE_NAME: str = "enrich_repos"
LAST_MONTH_ID_STATE_KEY: str = "last_enriched_month_id"
REQUEST_DELAY_SECONDS: float = 0.2
RATE_LIMIT_BACKOFF_SECONDS: int = 60

logger: logging.Logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Section 2: Parallel AI client
# ---------------------------------------------------------------------------


def get_repo_data(client: Parallel, repo_url: str) -> StructuredOutput:
    result = client.task_run.execute(
        input=f"{system_prompt()}\n\nExtract metadata for: {repo_url}",
        processor="lite-fast",
        output=StructuredOutput,
    )
    return StructuredOutput.model_validate(result.output.content)


# ---------------------------------------------------------------------------
# Section 3: Enrichment transformation
# ---------------------------------------------------------------------------


def get_new_repo_names(
    source_dataset: dlt.Dataset,
    last_month_id: str | None,
) -> tuple[list[str], str | None]:
    rows = (
        source_dataset.table("repos_with_stars")
        .select("repo_name", "month_id")
        .fetchall()
    )

    seen: set[str] = set()
    new_repos: list[str] = []
    max_month_id = last_month_id

    for row in rows:
        repo_name, month_id = row[0], row[1]

        if last_month_id and month_id <= last_month_id:
            continue

        if max_month_id is None or month_id > max_month_id:
            max_month_id = month_id

        if repo_name in seen:
            continue

        seen.add(repo_name)
        new_repos.append(repo_name)

    logger.info(
        "Source: %d total rows, %d new unique repos (after month_id=%s)",
        len(rows),
        len(new_repos),
        last_month_id,
    )

    return new_repos, max_month_id


def get_last_month_id(pipeline: dlt.Pipeline) -> str | None:
    for source_state in pipeline.state.get("sources", {}).values():
        resources = source_state.get("resources", {})
        if RESOURCE_NAME in resources:
            return resources[RESOURCE_NAME].get(LAST_MONTH_ID_STATE_KEY)
    return None


@dlt.hub.transformation(
    name=RESOURCE_NAME,
    table_name=TABLE_NAME,
    write_disposition={"disposition": "merge", "strategy": "upsert"},
    primary_key="repo_name",
)
def enrich_repos(
    source_dataset: dlt.Dataset,
    last_month_id: str | None,
) -> Iterator[dict[str, str]]:
    repo_names, new_last_month_id = get_new_repo_names(
        source_dataset=source_dataset,
        last_month_id=last_month_id,
    )

    if new_last_month_id and new_last_month_id != last_month_id:
        dlt.current.resource_state()[LAST_MONTH_ID_STATE_KEY] = new_last_month_id

    logger.info("Enriching %d repos", len(repo_names))

    if not repo_names:
        return

    client = Parallel(api_key=dlt.secrets["sources.parallel.api_key"], max_retries=3)

    try:
        for repo_name in repo_names:
            repo_url = f"https://github.com/{repo_name}"

            for attempt in range(2):
                try:
                    result = get_repo_data(client=client, repo_url=repo_url)
                    yield {
                        "repo_name": repo_name,
                        "description": result.description,
                        "programming_language": result.programming_language.value,
                        "license": result.license.value,
                    }
                    break
                except RateLimitError:
                    if attempt == 0:
                        logger.warning(
                            "Rate limited, waiting %ds before retry",
                            RATE_LIMIT_BACKOFF_SECONDS,
                        )
                        time.sleep(RATE_LIMIT_BACKOFF_SECONDS)
                        continue
                    logger.exception("Rate limited again, skipping %s", repo_name)
                except Exception:
                    logger.exception("Failed to enrich %s, skipping", repo_name)
                    break

            time.sleep(REQUEST_DELAY_SECONDS)

    finally:
        client.close()


# ---------------------------------------------------------------------------
# Section 4: Entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    source_pipeline = dlt.attach(GITHUB_STARS_PIPELINE_NAME)
    enrichment_pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination="filesystem",
        dataset_name=PIPELINE_NAME,
    )

    last_month_id = get_last_month_id(pipeline=enrichment_pipeline)
    logger.info("Last enriched month_id: %s", last_month_id)

    load_info = enrichment_pipeline.run(
        enrich_repos(
            source_dataset=source_pipeline.dataset(),
            last_month_id=last_month_id,
        ),
    )

    print(f"Pipeline load info: {load_info}")  # noqa: T201


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    main()
