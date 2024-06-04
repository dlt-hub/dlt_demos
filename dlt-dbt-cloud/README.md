# dlt_dbt_cloud
Repository with demos of using DLT and DBT Cloud

## Installation

```sh
pip install dlt[bigquery]
```

## Set up the pokemon pipeline

To get started with this data pipeline, follow these steps:

### Init the pipeline

Enter the following command:

```sh
dlt init pokemon bigquery
```

For more information, read the
[Add a verified source.](https://dlthub.com/docs/walkthroughs/add-a-verified-source)

### Add credentials

1. In the `.dlt` folder, there's a file called `secrets.toml`. It's where you store sensitive
   information securely, like access tokens. Keep this file safe.

   Use the following format for service account authentication:

   ```toml
   [sources.source_name]
   secret = "Please set me up!"
   ```
   
   [Pokemon verified source](https://github.com/dlt-hub/verified-sources/tree/master/sources/pokemon) 
   doesn't require authentication, so we don't need to provide credentials. 
    
2. Enter credentials for the BigQuery destination as per the [docs](https://dlthub.com/docs/dlt-ecosystem/destinations/bigquery):
    ```toml
    [destination.bigquery]
    location = "US"
    
    [destination.bigquery.credentials]
    project_id = "project_id" # please set me up!
    private_key = "private_key" # please set me up!
    client_email = "client_email" # please set me up!
    ```


For more information, read the [General Usage: Credentials.](https://dlthub.com/docs/general-usage/credentials)

## Set up the dbt Cloud

### Sign in dbt Cloud 
Go through this [Quickstart for dbt Cloud and BigQuery](https://docs.getdbt.com/quickstarts/bigquery?step=1).

### Create the dbt model
Create the model for your data with the tutorial: [How to build SQL models](https://docs.getdbt.com/docs/build/sql-models).

### Update pipeline script

Add the following code into your pipeline script (`pipelines/pokemon_pipeline.py`):

```python
from dlt.helpers.dbt_cloud import run_dbt_cloud_job

run_info = run_dbt_cloud_job()
print(f"Job run status: {run_info['status_humanized']}")
```

### Credentials

Use the following format for dbt Cloud API authentication in `.dlt/secrets.toml`:

```toml
[dbt_cloud]
api_token = "set me up!" # required for authentication
account_id = "set me up!" # required for both helpers function
job_id = "set me up!" # optional only for run_dbt_cloud_job function (you can pass this explicitly as an argument to the function)
```

More information about dbt cloud helpers in [DBT Cloud Client and Helper Functions](https://dlthub.com/docs/dlt-ecosystem/transformations/dbt/dbt_cloud).

## Run the pipeline

Now you are ready to run the pipeline! To get started, run the following command:

```bash
python pokemon_pipeline.py
```
