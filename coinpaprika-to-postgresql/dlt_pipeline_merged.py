import dlt
from dlt.sources.helpers import requests


# Resource 1: Retrieves a basic list of cryptocurrencies from coinpaprika.com
@dlt.resource(name = "coin_list", write_disposition="replace")
def coin_list():
    response = requests.get('https://api.coinpaprika.com/v1/coins')
    yield from response.json()


# Resource 2 - Transformer: Extracts detailed information for each coin
@dlt.transformer(data_from = coin_list().add_limit(10)) # The limit is added to avoid exceeding the API's request quota
def coin_information(coin):
    coin_id = coin['id']
    # Fetching detailed information including the list of team members, tags, and links for each coin
    details = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}')
    # Fetching the latest OHLCV (Open, High, Low, Close, Volume) data as a list with a single dictionary
    ohlc = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/latest')
    # Fetching exchanges where the coin is traded as a nested list
    exchanges = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}/exchanges')
    # Merging details, OHLCV, and exchanges data and yielding as one record
    yield details.json() | ohlc.json()[0] | {"exchanges": exchanges.json()}


# Source: Aggregates the coin list and detailed coin information into a single source
@dlt.source
def crypto_data(name = "crypto_source"):
    yield coin_list()
    yield coin_information()


# Main function to execute the data loading pipeline
def load_coin_details() -> None:
    # Setting up the pipeline with PostgreSQL as the destination
    pipeline = dlt.pipeline(
        pipeline_name="crypto_pipeline",
        destination='postgres',
        full_refresh=True,
        dataset_name="crypto_data",
    )
    # Running the pipeline and printing execution details
    info = pipeline.run(crypto_data())
    print(info)


if __name__ == "__main__":
    load_coin_details()
