# Loading Nested Data from an API into a PostgreSQL Database with dlt

## Overview

This demo project demonstrates how to load nested data from separate API endpoints, where multiple endpoints rely on the response of one endpoint. It demonstrates how to set up `dlt` (Data Loading Tool) resources, including transformer resources and a source that merges them into a single dataset. Additionally, it includes a pipeline that handles the data ingestion process. PostgreSQL is used as the storage destination, and data is sourced from the Coinpaprika API.


## Prerequisites
 
1. Docker Desktop.

    > Visit their [official page](https://www.docker.com/products/docker-desktop/) to download.

2. DBeaver or a different database administration tool of your choice.

    > [Download](https://dbeaver.io/download/) DBeaver.

You can also use [DuckDB as destination](https://dlthub.com/docs/getting-started) for easier setup.
    
## Setup Guide

1. Clone this repo.

2. Install the necessary dependencies for Postgres.

    ```bash
    pip install -r requirements.txt
    ```

3. Setup PostgreSQL using the public image.

   ```bash
    $ docker pull postgres
    ```

4. Run the Docker container using the postgres:latest image with the below command.

    ```bash
    $ docker run -itd -e POSTGRES_USER=loader -e POSTGRES_PASSWORD=password -p 5432:5432 -v /data:/var/lib/postgresql/data --name postgresql postgres    
    ```

    > Replace the first `/data` with the absolute path to the directory on your local machine that you want to map to `/var/lib/postgresql/data` inside the container.

5. Connect with the database.

    ```bash
    PGPASSWORD=password psql -h localhost -p 5432 -U loader     
    ```

6. Create a new database.

    ```bash
    CREATE DATABASE demo_data;
    ```

7. Create an empty `secrets.toml` in `.dlt` and enter your credentials. 

    ```env
    [destination.postgres.credentials]

    database = "demo_data"
    username = "loader"
    password = "password" # replace with your password
    host = "localhost" # or the IP address location of your database
    port = 5432
    connect_timeout = 15    
    ```

## Your dlt pipeline

1. Understand your resources and sources.

    > Explanation to be added by Anuun.

2. Understand your pipeline.

    > Explanation to be added by Anuun.

3. Run your pipeline. 

## View your data in DBeaver

1. Connect DBeaver to your database.

    - Click `New Database Connection` on the top left corner.
    - Choose PostgreSQL.
    - Enter `demo_data` as database.
    - Enter `loader` as username.
    - Enter `password` as password.
    - Test your connection.

2. View your data. It should look like this. 

    ![DBeaver view of demo_data](https://storage.googleapis.com/dlt-blog-images/belgrade_demo_DBeaver.png)
