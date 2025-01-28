from restack_ai.function import function


@function.defn()
async def poke_pipeline() -> str:
    import dlt
    from dlt.sources.helpers import requests

    # Define a resource to fetch pokemons from PokeAPI
    @dlt.resource(table_name="pokemon_api")
    def get_pokemon():
        url = "https://pokeapi.co/api/v2/pokemon"
        response = requests.get(url)
        yield response.json()["results"]

    # Set pipeline name, destination, and dataset name
    pipeline = dlt.pipeline(
        pipeline_name="quick_start",
        destination="duckdb",
        dataset_name="mydata",
    )

    # Run the pipeline using the defined resource
    pipeline.run(get_pokemon)
    return str(pipeline.last_trace)
