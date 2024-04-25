# from tabular import Tabular
# t = Tabular(credential="t-w7-YQiFOhLI:t1L8RQG1T29iGaUmC0PI8R5fW4U")
# print(t.list_warehouses())
#
# from tabular import loader
#
# loader.enable_loading(
#     identifier="prod.default.invoices_table",
#     file_type="csv",
#     mode="append",
#     override=True
# )

import dlt
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema

catalog = load_catalog(
    "iceberg_demo",
    **{
        "uri": "https://api.tabular.io/ws/",
        "warehouse": "iceberg_demo",
        "credential": "t--1QfNhgwJgY:UBEOrBW-2wroKsXPIL38Wm6-bd4",
    }
)

print(catalog.list_tables('issues'))

schema = Schema()

catalog.create_table(
    identifier="issues._dlt_pipeline_state",
    schema=schema,
    location="s3://dlt-ci-test-bucket/github_issues/_dlt_pipeline_state/",
    properties={
        "fileloader.enabled": 'true',
        "fileloader.path": "s3://dlt-ci-test-bucket/github_issues/_dlt_pipeline_state/",
        "fileloader.file-format": "parquet",
        "fileloader.write-mode": "append",
        "fileloader.evolve-schema": "true"
    }
)

#
# from tabular import loader
#
# loader.enable_loading(
#     identifier="iceberg_demo.issues._dlt_pipeline_state",
#     file_type="parquet",
#     mode="append",
#     override=True,
#     catalog=catalog,
#     path="s3://dlt-ci-test-bucket/github_issues/_dlt_pipeline_state/"
# )

table = catalog.load_table("issues._dlt_pipeline_state")
with table.transaction() as transaction:
    transaction.set_properties("fileloader.enabled=false")

print(table.properties)