import dlt
import requests

# url to request dlt-hub user
url = f"https://api.github.com/users/dlt-hub/followers"
# make the request and return the json
data = requests.get(url).json()

pipeline = dlt.pipeline(
    pipeline_name='from_api',
    destination='duckdb',
    dataset_name='mydata',
    dev_mode=True,
)
# dlt works with lists of dicts, so wrap data to the list
load_info = pipeline.run([data], table_name="followers")
print(load_info)
