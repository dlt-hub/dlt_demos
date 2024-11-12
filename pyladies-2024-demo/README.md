## Overview

`dlt` is an open-source library that you can add to your Python scripts to load data from various and often messy data sources into well structured, live datasets. Below we give you a preview how you can get data from APIs, files, Python objects or pandas dataframes and move it into a local or remote database, data lake or a vector data store.

Let's get started!

## Installation

Official releases of dlt can be installed from [PyPI](https://pypi.org/project/dlt/):

```shell
pip install dlt
```

Command above just installs library core, in example below we use `duckdb` as a [destination](https://dlthub.com/docs/dlt-ecosystem/destinations), so let's add it:

```shell
pip install -q "dlt[duckdb]"
```

> Use clean virtual environment for your experiments! Here are [detailed instructions](https://dlthub.com/docs/reference/installation).

## Quick start

Let's load a list of Python objects (dicts) into `duckdb` database and inspect the created dataset.

> We gonna use `dev_mode` for our test examples. If you create a new pipeline script you will be experimenting a lot. 
> If you want that each time the pipeline resets its state and loads data to a new dataset, set the `dev_mode` argument of the `dlt.pipeline` method to True. 
> Each time the pipeline is created, dlt adds datetime-based suffix to the dataset name.

Run the command:
```shell
python getting-started.py
```

### Now explore your data!

#### If you run it locally

To see the schema of your created database, run Streamlit command `dlt pipeline <pipeline_name> show`.

To use `streamlit`, install it first.

```shell
pip install streamlit
```

For example above pipeline name is “quick_start”, so run:

```shell
dlt pipeline quick_start show
```
[This command](https://dlthub.com/docs/reference/command-line-interface#show-tables-and-data-in-the-destination) generates and launches a simple Streamlit app that you can use to inspect the schemas and data in the destination.

## Load data from variety of sources

Use dlt to load practically any data you deal with in your Python script into a dataset.

The library will create/update tables, infer data types and deal with nested data automatically:
- list of dicts
- json 
- csv/parquet
- API
- database
- etc.

### from JSON

When creating a schema during normalization, dlt recursively unpacks this nested structure into relational tables, creating and linking [children and parent tables](https://dlthub.com/docs/general-usage/destination-tables#nested-tables).

```shell
python load_from_json.py
```

### from API

Below we load 100 most recent followers from our [own dlt-hub organisation](https://github.com/dlt-hub/dlt) into "followers" table.

```shell
python github_pipeline.py
```

### from Database

Use the SQL source to extract data from databases like PostgreSQL, MySQL, SQLite, Oracle, and more.

```shell
pip install pymysql
```

## Real-life example

For this example, we will be loading Pokemon data from the PokeAPI with the help of transformers to load Pokemon details in parallel.

```shell
python poke_pipeline.py
```
