from dagster import Definitions, load_assets_from_modules, define_asset_job
from dagster_snowflake_pandas import SnowflakePandasIOManager
from dagster_snowflake import SnowflakeResource
from . import assets
from . import resources
import toml
import os


# Load your secrets from the secrets.toml file accessed by dlt
with open(os.getcwd() + '/.dlt/secrets.toml', 'r') as secrets_file:
    secrets = toml.load(secrets_file) 


# Set your secret values
snowflake_user = secrets["destination"]["snowflake"]["credentials"]["username"]
snowflake_password = secrets["destination"]["snowflake"]["credentials"]["password"]
snowflake_warehouse = secrets["destination"]["snowflake"]["credentials"]["warehouse"]
snowflake_database = secrets["destination"]["snowflake"]["credentials"]["database"]
snowflake_account = secrets["destination"]["snowflake"]["credentials"]["host"]
snowflake_schema = secrets["destination"]["snowflake"]["credentials"]["schema"]


# Set your dlt pipelines as Dagster jobs
dlt_pipelines = define_asset_job(name = "dlt_pipelines", selection= ['google_trends_asset', 'hacker_news_full_asset'])


# Set your Dagster definition 
defs = Definitions(
    assets = load_assets_from_modules([assets]),
    jobs = [dlt_pipelines],
    resources = {
        "pipeline": resources.DltPipeline(
            pipeline_name = "dagster_pipeline",
            dataset_name = "dagster_snoflake_demo",
            destination = "snowflake",
            description = ""
        ),
        "io_manager": SnowflakePandasIOManager(
            account = snowflake_account,
            user = snowflake_user, 
            password = snowflake_password,
            warehouse = snowflake_warehouse,
            database = snowflake_database,
            schema = snowflake_schema,
            # role = snowflake_role # Optional
        ),
        "image_storage": resources.LocalFileStorage(
            dir = "charts"
        ),
        "snowflake": SnowflakeResource(
            account = snowflake_account,
            user = snowflake_user, 
            password = snowflake_password,
            database = snowflake_database,
            schema = snowflake_schema,
        )
    }
)