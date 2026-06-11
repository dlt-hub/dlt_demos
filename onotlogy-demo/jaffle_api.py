"""Sample Shop dlt pipeline.

Loads customers, orders, items, products, supplies, and stores
from a public sample online-shop REST API into a local warehouse.
"""

import dlt
from dlt.sources.rest_api import rest_api_source


def sample_shop():
    return rest_api_source(
        {
            "client": {
                "base_url": "https://jaffle-shop.dlthub.com/api/v1/",
                "paginator": {
                    "type": "header_link",
                },
            },
            "resource_defaults": {
                "parallelized": False,
            },
            "resources": [
                {"name": "customers", "primary_key": "id"},
                {"name": "orders", "primary_key": "id"},
                {"name": "items", "primary_key": "id"},
                {"name": "products", "primary_key": "sku"},
                {"name": "supplies", "primary_key": "id"},
                {"name": "stores", "primary_key": "id"},
            ],
        }
    )


def load_sample_shop():
    """Load sample shop data from the public REST API."""

    pipeline = dlt.pipeline(
        pipeline_name="sample_shop_pipeline",
        destination="duckdb",
        dataset_name="sample_shop",
    )

    load_info = pipeline.run(sample_shop().add_limit(1))
    print(load_info)


if __name__ == "__main__":
    load_sample_shop()