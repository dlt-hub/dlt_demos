# load test json to duckdb database

import json
import dlt

with open("test.json", 'r') as file:
    data = json.load(file)

pipeline = dlt.pipeline(
    pipeline_name='from_json',
    destination='duckdb',
    dataset_name='mydata',
    dev_mode=True,
)
# dlt works with lists of dicts, so wrap data to the list
load_info = pipeline.run([data], table_name="json_data")
print(load_info)
