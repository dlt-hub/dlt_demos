import os
import dlt

from stripe import stripe_source

stripe_api_key = os.getenv('STRIPE_API_KEY')


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="stripe_pipeline",
        destination='duckdb',
        dataset_name="stripe_data",
        progress="log",
        export_schema_path="schemas/export"
    )
    source = stripe_source(stripe_api_key, password="").with_resources("get_customers", "get_subscriptions")
    info = pipeline.run(source)
    print(info)