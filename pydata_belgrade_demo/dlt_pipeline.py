import dlt
from dlt.sources.helpers import requests

# Resource 1: Basic information about cryptocurrencies on coinpaprika.com:
@dlt.resource(name = "coin_list", write_disposition="replace")
def coin_list():
    response = requests.get('https://api.coinpaprika.com/v1/coins')
    yield from response.json()

# Resource 2 - Transformer: Detailed descriptive information about a single coin
@dlt.transformer(data_from = coin_list().add_limit(2)) 
def coin_details(coin):
    coin_id = coin['id']
    response = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}')
    yield response.json()

# Resource 3 - Transformer: The last 50 timeline tweets from the official Twitter profile for a given coin
@dlt.transformer(data_from = coin_list().add_limit(2))
def coin_tweets(coin):
    coin_id = coin['id']
    response = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}/twitter')
    data = response.json()
    data_with_id = [{'id': coin_id, **entry} for entry in data]
    yield data_with_id

# Source: Combines the above three resources into a single source
@dlt.source
def crypto_data(name = "crypto_source"):
    yield coin_list()
    yield coin_details()
    yield coin_tweets()

# Main function to run the pipeline
def load_coin_details() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="crypto_pipeline",
        destination='postgres',
        full_refresh=True,
        dataset_name="crypto_data"
    )
    info = pipeline.run(crypto_data().add_limit(2))
    print(info)

if __name__ == "__main__":
    load_coin_details()
