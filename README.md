# Data Loading Demos

This repository contains Jupyter notebooks that illustrate various methods for loading data into different destinations (e.g. Weaviate database)
using the [dlt](https://github.com/dlt-hub/dlt) library.

## Repository Contents

### Weaviate demos

- [pdf_to_weaviate.ipynb](pdf_to_weaviate.ipynb): shows how to load data from PDF files, specifically invoices, into Weaviate.
- [sql_to_weaviate.ipynb](sql_to_weaviate.ipynb): shows how to import data from a public MySQL database into Weaviate.
- [zendesk_to_weaviate.ipynb](zendesk_to_weaviate.ipynb): loads data from a [Zendesk dlt source](https://dlthub.com/docs/dlt-ecosystem/verified-sources/zendesk) into Weaviate.

#### Prerequisites

To run these notebooks, you will need credentials of a Weaviate instance.

### Common demos

- [spotlight_demo.ipynb](spotlight_demo.ipynb): shows how to get data from APIs, files, Python objects and move it into a local or remote database.
  Demo was created for a [Data Talks Club: Open-Source Spotlight](https://youtube.com/playlist?list=PL3MmuxUbc_hJ5t5nnjzC0F2zan76Dpsz0&feature=shared) project.


## License

This repository is licensed under the [Apache License 2.0](LICENSE.txt). Please refer to the `LICENSE.txt` file for more details.

Happy coding and data loading! 🚀📊
