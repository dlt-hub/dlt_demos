import dlt
from dlt.sources.helpers import requests

BASE_URL = "https://api.github.com/repos"


@dlt.resource(
    table_name="issues",
    write_disposition="merge",
    primary_key="id",
)
def get_issues(
    organisation_name: str,
    repo_name: str,
    updated_at=dlt.sources.incremental(
        "updated_at", initial_value="1970-01-01T00:00:00Z"
    ),
):
    # NOTE: we read only open issues to minimize number of calls to the API. There's a limit of ~50 calls for not authenticated Github users
    url = f"{BASE_URL}/{organisation_name}/{repo_name}/issues"

    while True:
        response = requests.get(
            url,
            params={
                "since": {updated_at.last_value},
                "per_page": 100,
                "sort": "updated",
                "directions": "desc",
                "state": "open",
            },
        )
        response.raise_for_status()
        yield response.json()

        # get next page
        if "next" not in response.links:
            break
        url = response.links["next"]["url"]


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_issues_pipeline",
        destination="athena",
        dataset_name="github_issues_data",
    )
    source_data = get_issues(organisation_name="dlt-hub", repo_name="dlt")
    load_info = pipeline.run(source_data)
    row_counts = pipeline.last_trace.last_normalize_info

    print(row_counts)
    print("------")
    print(load_info)
