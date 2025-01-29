import time
import traceback

import dlt
import pendulum
import requests
from dlt.destinations.adapters import weaviate_adapter
from pydantic import BaseModel
from restack_ai.function import function, log


class PipelineInput(BaseModel):
    pipeline_name: str
    destination: str
    add_limit: int
    dev_mode: bool


@function.defn()
async def anime_pipeline(input: PipelineInput) -> str:
    @dlt.resource(table_name="anime", write_disposition="merge", primary_key="mal_id")
    def get_anime(
        aired_from=dlt.sources.incremental(
            "aired.from", initial_value="2024-07-01T00:00:00+00:00"
        )
    ):
        yield pagination(
            "anime",
            params={
                "order_by": "start_date",
                "start_date": remove_hms(aired_from.last_value),
                "status": "airing",
            },
            base_url="https://api.jikan.moe/v4/",
        )

    try:
        # Set pipeline name, destination, and dataset name
        pipeline = dlt.pipeline(
            pipeline_name=input.pipeline_name,
            destination=input.destination,
            progress="log",
            dev_mode=input.dev_mode,
        )

        data = get_anime().add_limit(input.add_limit)

        if input.destination == "weaviate":
            data = weaviate_adapter(
                data,
                vectorize=["title", "synopsis"],
            )

        # Run the pipeline using the defined resource
        pipeline.run(data)
        return str(pipeline.last_trace)
    except Exception as e:
        log.error("Something went wrong!", error=e)
        log.error(traceback.format_exc())
        raise e


def remove_hms(date: str) -> str:
    date_obj = pendulum.parse(date)
    return date_obj.to_date_string()


def pagination(endpoint: str, params: dict, base_url: str):
    has_next_page = True
    page = 1
    retries = 0

    while has_next_page:
        params.update({"page": page})

        try:
            response = requests.get(f"{base_url}{endpoint}", params)
            if response.status_code == 429:  # Rate limit error
                wait_time = min(2 ** retries, 60)  # Exponential backoff, max 60s
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
                continue  # Retry the same request

            response.raise_for_status()  # Raise an error for 4xx or 5xx responses
            retries = 0  # Reset retries on a successful request
            data = response.json()

            if "data" in data:
                yield data["data"]

            has_next_page = data.get("pagination", {}).get("has_next_page", False)
            page += 1

        except requests.RequestException as e:
            print(f"Request failed for {endpoint}: {e}")
            break

        time.sleep(0.5)