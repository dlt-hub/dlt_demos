"""Transform sample_shop source tables into the retail_sales CDM.

Star schema per .schema/retail_sales/CDM.dbml:
  dimensions: dim_customer, dim_product, dim_store, dim_supply (all SCD Type 1)
  facts:      fact_orders (order grain), fact_order_items (line grain)

Key contract: all surrogate keys are VARCHAR md5 hashes of the source natural
keys. Conformed dimensions carry an 'unknown' sentinel row so fact FKs are
never NULL. Facts derive surrogate keys from source columns directly (same
hash expression), never from dim_* outputs.
"""

import os
from pathlib import Path

import dlt

PIPELINE = "sample_shop_pipeline"


@dlt.source
def retail_sales_to_cdm(dataset: dlt.Dataset):
    # dimensions first — facts join on their surrogate keys
    yield dim_customer(dataset)
    yield dim_product(dataset)
    yield dim_store(dataset)
    yield dim_supply(dataset)
    # facts after
    yield fact_orders(dataset)
    yield fact_order_items(dataset)


@dlt.hub.transformation(
    write_disposition="replace",
    columns={
        "customer_sk": {"data_type": "text", "nullable": False},
        "source_id": {"data_type": "text", "nullable": True},
        "source_pipeline": {"data_type": "text", "nullable": False},
        "name": {"data_type": "text", "nullable": True},
    },
)
def dim_customer(dataset: dlt.Dataset):
    yield dataset(
        """
        SELECT * FROM (
            SELECT
                MD5(id) AS customer_sk,
                id AS source_id,
                'sample_shop_pipeline' AS source_pipeline,
                name
            FROM customers
            UNION ALL
            SELECT
                'unknown',
                CAST(NULL AS VARCHAR),
                'sample_shop_pipeline',
                'Unknown customer'
        ) AS dim_customer
        """
    )


@dlt.hub.transformation(
    write_disposition="replace",
    columns={
        "product_sk": {"data_type": "text", "nullable": False},
        "source_id": {"data_type": "text", "nullable": True},
        "source_pipeline": {"data_type": "text", "nullable": False},
        "name": {"data_type": "text", "nullable": True},
        "type": {"data_type": "text", "nullable": True},
        "price": {"data_type": "double", "nullable": True},
        "description": {"data_type": "text", "nullable": True},
    },
)
def dim_product(dataset: dlt.Dataset):
    yield dataset(
        """
        SELECT * FROM (
            SELECT
                MD5(sku) AS product_sk,
                sku AS source_id,
                'sample_shop_pipeline' AS source_pipeline,
                name,
                type,
                price,
                description
            FROM products
            UNION ALL
            SELECT
                'unknown',
                CAST(NULL AS VARCHAR),
                'sample_shop_pipeline',
                'Unknown product',
                CAST(NULL AS VARCHAR),
                CAST(NULL AS DOUBLE),
                CAST(NULL AS VARCHAR)
        ) AS dim_product
        """
    )


@dlt.hub.transformation(
    write_disposition="replace",
    columns={
        "store_sk": {"data_type": "text", "nullable": False},
        "source_id": {"data_type": "text", "nullable": True},
        "source_pipeline": {"data_type": "text", "nullable": False},
        "name": {"data_type": "text", "nullable": True},
        "opened_at": {"data_type": "timestamp", "nullable": True},
        "tax_rate": {"data_type": "double", "nullable": True},
    },
)
def dim_store(dataset: dlt.Dataset):
    yield dataset(
        """
        SELECT * FROM (
            SELECT
                MD5(id) AS store_sk,
                id AS source_id,
                'sample_shop_pipeline' AS source_pipeline,
                name,
                opened_at,
                tax_rate
            FROM stores
            UNION ALL
            SELECT
                'unknown',
                CAST(NULL AS VARCHAR),
                'sample_shop_pipeline',
                'Unknown store',
                CAST(NULL AS TIMESTAMP),
                CAST(NULL AS DOUBLE)
        ) AS dim_store
        """
    )


@dlt.hub.transformation(
    write_disposition="replace",
    columns={
        "supply_sk": {"data_type": "text", "nullable": False},
        "source_id": {"data_type": "text", "nullable": True},
        "source_pipeline": {"data_type": "text", "nullable": False},
        "name": {"data_type": "text", "nullable": True},
        "cost": {"data_type": "double", "nullable": True},
        "perishable": {"data_type": "bool", "nullable": True},
        "product_sk": {"data_type": "text", "nullable": False},
    },
)
def dim_supply(dataset: dlt.Dataset):
    # supply id repeats per sku, so the surrogate key hashes both
    yield dataset(
        """
        SELECT
            MD5(id || '|' || COALESCE(sku, '')) AS supply_sk,
            id AS source_id,
            'sample_shop_pipeline' AS source_pipeline,
            name,
            cost,
            perishable,
            CASE WHEN sku IS NULL THEN 'unknown' ELSE MD5(sku) END AS product_sk
        FROM supplies
        """
    )


@dlt.hub.transformation(
    write_disposition="replace",
    columns={
        "order_sk": {"data_type": "text", "nullable": False},
        "order_id": {"data_type": "text", "nullable": False},
        "customer_sk": {"data_type": "text", "nullable": False},
        "store_sk": {"data_type": "text", "nullable": False},
        "ordered_at": {"data_type": "timestamp", "nullable": True},
        "subtotal": {"data_type": "double", "nullable": True},
        "tax_paid": {"data_type": "double", "nullable": True},
        "order_total": {"data_type": "double", "nullable": True},
    },
)
def fact_orders(dataset: dlt.Dataset):
    yield dataset(
        """
        SELECT
            MD5(id) AS order_sk,
            id AS order_id,
            CASE WHEN customer_id IS NULL THEN 'unknown' ELSE MD5(customer_id) END AS customer_sk,
            CASE WHEN store_id IS NULL THEN 'unknown' ELSE MD5(store_id) END AS store_sk,
            ordered_at,
            subtotal,
            tax_paid,
            order_total
        FROM orders
        """
    )


@dlt.hub.transformation(
    write_disposition="replace",
    columns={
        "order_item_sk": {"data_type": "text", "nullable": False},
        "order_id": {"data_type": "text", "nullable": True},
        "item_id": {"data_type": "text", "nullable": False},
        "customer_sk": {"data_type": "text", "nullable": False},
        "store_sk": {"data_type": "text", "nullable": False},
        "product_sk": {"data_type": "text", "nullable": False},
        "ordered_at": {"data_type": "timestamp", "nullable": True},
        "unit_price": {"data_type": "double", "nullable": True},
    },
)
def fact_order_items(dataset: dlt.Dataset):
    # customer/store/ordered_at inherited from the order header;
    # unit_price joined from products — the source has no line-level price
    yield dataset(
        """
        SELECT
            MD5(i.id) AS order_item_sk,
            i.order_id AS order_id,
            i.id AS item_id,
            CASE WHEN o.customer_id IS NULL THEN 'unknown' ELSE MD5(o.customer_id) END AS customer_sk,
            CASE WHEN o.store_id IS NULL THEN 'unknown' ELSE MD5(o.store_id) END AS store_sk,
            CASE WHEN i.sku IS NULL THEN 'unknown' ELSE MD5(i.sku) END AS product_sk,
            o.ordered_at,
            p.price AS unit_price
        FROM items AS i
        LEFT JOIN orders AS o ON i.order_id = o.id
        LEFT JOIN products AS p ON i.sku = p.sku
        """
    )


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parents[1])  # run from project root

    source_pipeline = dlt.attach(pipeline_name=PIPELINE)
    source_dataset = source_pipeline.dataset()

    # write into the source duckdb database (catalog sample_shop_pipeline,
    # schema retail_sales) — a database file named retail_sales.duckdb would
    # collide with the dataset name and trigger duckdb's ambiguous
    # catalog/schema binder error; co-locating also lets analysts join CDM
    # tables with raw data
    # absolute path — dlt resolves relative duckdb paths against its own
    # data dir, not the cwd
    source_db_path = str(
        Path(".dlt/data/dev/sample_shop_pipeline.duckdb").resolve()
    )
    cdm_pipeline = dlt.pipeline(
        pipeline_name="retail_sales",
        destination=dlt.destinations.duckdb(source_db_path),
        dataset_name="retail_sales",
    )
    load_info = cdm_pipeline.run(retail_sales_to_cdm(source_dataset))
    print(load_info)
