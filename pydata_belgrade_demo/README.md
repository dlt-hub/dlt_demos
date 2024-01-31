# Loading Nested Data from an API into a PostgreSQL Database with dlt

## Overview

This demo project demonstrates how to load nested data from separate API endpoints, where multiple endpoints rely on the response of one endpoint. It demonstrates how to set up `dlt` (Data Loading Tool) resources, including transformer resources and a source that merges them into a single dataset. Additionally, it includes a pipeline that handles the data ingestion process. PostgreSQL is used as the storage destination, and data is sourced from the Coinpaprika API.

![Pipeline overview](https://storage.googleapis.com/dlt-blog-images/belgrade_demo_overview.png)


## Prerequisites
 
1. Docker Desktop

    > Download [Docker Desktop](https://www.docker.com/products/docker-desktop/) to download.

2. DBeaver or another database administration tool of your choice

    > Download [DBeaver](https://dbeaver.io/download/).

Alternatively, use [DuckDB as destination](https://dlthub.com/docs/getting-started) for a simpler setup.
    
## Setup Guide

1. Clone this repository.

2. Install the necessary dependencies for PostgreSQL:

    ```bash
    pip install -r requirements.txt
    ```

3. Setup PostgreSQL using the public image:

   ```bash
    $ docker pull postgres
    ```

4. Run the Docker container using the postgres:latest image with the command below:

    ```bash
    $ docker run -itd -e POSTGRES_USER=loader -e POSTGRES_PASSWORD=password -p 5432:5432 -v /data:/var/lib/postgresql/data --name postgresql postgres    
    ```

    > Replace `/data` with the absolute path to your local directory that you want to map to `/var/lib/postgresql/data` inside the container.

5. Connect to the database:

    ```bash
    PGPASSWORD=password psql -h localhost -p 5432 -U loader     
    ```

6. Create a new database:

    ```bash
    CREATE DATABASE demo_data;
    ```

7. Create an empty `secrets.toml` in the `.dlt` directory and enter your credentials:

    ```env
    [destination.postgres.credentials]

    database = "demo_data"
    username = "loader"
    password = "password" # replace with your password
    host = "localhost" # or the IP address location of your database
    port = 5432
    connect_timeout = 15    
    ```

## Your `dlt` Pipeline

1. Understand your resources and sources.

    In the context of `dlt`, a source is a location that holds data with a certain structure, organized into one or more resources. It can also refer to the software component (i.e., a Python function) that extracts data from the source location using one or more resource components. For example, if the source is an API, then a resource is an endpoint in that API. If the source is a database, then a resource is a table in that database.

    The demo has two resources:

    - `coin_list()` yields a list of cryptocurrencies from coinpaprika.com:

        ```python
        @dlt.resource(name = "coin_list", write_disposition="replace")
        def coin_list():
            response = requests.get('https://api.coinpaprika.com/v1/coins')
            yield from response.json()
        ```
    - `coin_information(coin)` is a transformer resource that fetches comprehensive details from three distinct API endpoints for each cryptocurrency provided by `coin_list()`. The responses are then merged into one object for loading into a single database table:

        ```python
        @dlt.transformer(data_from = coin_list().add_limit(2)) 
        def coin_information(coin):
            coin_id = coin['id']
            details = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}')
            ohlc = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/latest')
            exchanges = requests.get(f'https://api.coinpaprika.com/v1/coins/{coin_id}/exchanges')
            yield details.json() | ohlc.json()[0] | {"exchanges": exchanges.json()}
        ```
    These resources are combined into the `crypto_data()` source,which corresponds to a dataset with tables generated from the two resources:

    ```python
    @dlt.source
    def crypto_data(name = "crypto_source"):
        yield coin_list()
        yield coin_information()        
    ```

    The `@dlt.resource` and `@dlt.source` decorators declare a function as a resource/source in `dlt`, offering flexibility with essential functionalities. 

    > Note that the decorators use `yield` to produce data on-the-fly, instead of loading all data into memory at once. 

2. Understand your pipeline.

    We define a pipeline named `crypto_pipeline` with PostgreSQL as destination:

    ```python
    def load_coin_details() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="crypto_pipeline",
        destination='postgres',
        full_refresh=True,
        dataset_name="crypto_data",
    )
    info = pipeline.run(crypto_data())
    ```
    `full_refresh` is set to `True`, creating new dataset instances each time the pipeline runs. If set to `False`, the pipeline will update the existing dataset instead of creating new ones.

    The default `write_disposition` in `pipeline.run()` is set to `append`, meaning new data will be added to the existing data in the destination. Other options include:

    - `replace`: This replaces the existing data in the destination with the new data.
    - `merge`: This option merges the new data into the destination using a `merge_key`. It can also deduplicate or upsert new data using a `private_key`.


3. Run your pipeline:

    ```bash
    $ python3 dlt_pipeline_merged.py
    ```

## Viewing Your Data in DBeaver

1. Connect DBeaver to your database.

    - Click `New Database Connection` in the top left corner.
    - Choose PostgreSQL.
    - Enter `demo_data` as the database.
    - Enter `loader` as the username.
    - Enter `password` as the password.
    - Test the connection.

2. Once connected, you can view your data. It should look like this:

    ![DBeaver view of demo_data](https://storage.googleapis.com/dlt-blog-images/belgrade_demo_DBeaver.png)

    > To get a better understanding of how the nested data was normalized with `dlt`, view the example respones returned by the API endpoints in `example_api_responses`.

## Contact / Support
For guidance on running custom pipelines with `dlt`, consider joining our [Slack community](https://dlthub-community.slack.com).

Visit our [documentation page](https://dlthub.com/docs/intro) for more detailed information.