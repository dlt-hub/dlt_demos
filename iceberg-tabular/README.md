# Demo: GitHub Issues data pipeline

This Python script utilizes the `dlt` library to create a data pipeline for extracting and loading
GitHub issues data into [Athena/Glue Catalog](https://dlthub.com/docs/dlt-ecosystem/destinations/athena). 
The pipeline focuses on fetching open issues from a specified GitHub
repository, storing data as parquet files in s3 buckets and creating external tables in AWS Glue Catalog.
You can then query those tables with Athena SQL commands which 
will then scan the whole folder of parquet files and return the results.

In this demo we load data in Iceberg format (`force_iceberg = "True"`).
We can use AWS Glue as a Data Catalog, or we can load the Iceberg data into Tabular.io.

## Prerequisites

Before using the script, ensure you have the following prerequisites installed:

- Python
- `dlt` library with Athena dependencies (`pip install dlt[athena]`)


## Usage

* **Clone the Repository:**

   ```bash
   git clone https://github.com/dlt-hub/dlt_demos.git
   cd dlt_demos/iceberg-tabular
   ```
* **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
* **Credentials Configuration:**

    Copy `secrets.toml`:
    ```bash
    cp .dlt/example.secrets.toml .dlt/secrets.toml
    ```
    Ensure you set up the necessary credentials for the filesystem (S3) and Athena destinations in your
    `secrets.toml` file. Replace the placeholders with your actual credentials.
    
    ```toml
    [destination.filesystem]
    bucket_url = "s3://[your_bucket_name]" # replace with your bucket name,
    
    [destination.filesystem.credentials]
    aws_access_key_id = "please set me up!" # copy the access key here
    aws_secret_access_key = "please set me up!" # copy the secret access key here
    
    [destination.athena]
    force_iceberg = "True" # load data in the iceberg format
    query_result_bucket="s3://[results_bucket_name]" # replace with your query results bucket name
    
    [destination.athena.credentials]
    aws_access_key_id="please set me up!" # same as credentials for filesystem
    aws_secret_access_key="please set me up!" # same as credentials for filesystem
    region_name="please set me up!" # set your aws region, for example "eu-central-1" for Frankfurt
    database="awsdatacatalog"
    ```
* **Run the Script:**

   ```bash
   python github_pipeline.py --organisation-name=dlt-hub --repo-name=dlt
   ```
   CLI Options:
   * `--organisation-name`: GitHub organization name (required).
   * `--repo-name`: GitHub repository name (required).
   * `--pipeline-name`: Name of the dlt pipeline.
   * `--dataset-name`: Name of the dataset.


## Notes

- The script reads only open issues to minimize the number of API calls, considering the limit for
  non-authenticated GitHub users.
- The `updated_at` parameter ensures that only issues updated since the last execution are fetched.
- The pipeline utilizes Athena as the destination for storing the GitHub issues data.

Feel free to customize the script and pipeline configuration according to your requirements.
