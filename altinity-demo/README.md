# GitHub to Iceberg Pipeline with Altinity Cloud

End-to-end guide for loading GitHub data into Apache Iceberg using dlt and querying it from ClickHouse via Altinity Cloud.

---

## Prerequisites

- Python 3.12+
- An [Altinity Cloud](https://altinity.cloud) account with a cluster and managed Iceberg catalog

---

## 1. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Or with `uv`:

```bash
uv venv
source .venv/bin/activate
```

---

## 2. Install Dependencies

```bash
pip install "dlt[filesystem,pyiceberg]>=1.9.1" "dlthub>=0.9.1"
```

---

## 3. Self-License dlthub

After installation, issue a trial license for the Iceberg destination:

```bash
dlt license issue dlthub.iceberg
```

This prints your license key and inserts it into your `.dlt` config automatically. To verify:

```bash
dlt license info
```

---

## 4. Scaffold the Pipeline

Use the dlt CLI to generate a GitHub API pipeline targeting the Iceberg destination:

```bash
dlt init github_api iceberg
```

This creates `github_api_pipeline.py` and a `.dlt/` config directory.

In `github_api_pipeline.py`, update the pipeline name and dataset name to reflect the Iceberg destination:

```python
pipeline = dlt.pipeline(
    pipeline_name="github_iceberg_pipeline",  # was: github_api_pipeline
    destination='iceberg',
    dataset_name="github_iceberg_data",       # was: github_api_data
    progress="log",
)
```

---

## 5. Get Altinity Cloud Credentials

In the [Altinity Cloud Manager (ACM)](https://altinity.cloud):

1. Click **+ Setup Environment**
2. Fill in the **Environment Setup** dialog:
   - **Environment Name** — e.g. `dlthub-xbymv`
   - **Choose your cloud** — select `AWS` (or your preferred provider)
   - **Choose a region** — e.g. `EU West (London) — eu-west-2`
   - **Availability Zones** — select `eu-west-2a` and `eu-west-2b`
   - **Pick the account** — select `Use Altinity's cloud account`
3. Click **OK**
4. Once the environment is ready, navigate to it and go to the **Catalogs** tab
5. You will see a message saying "Iceberg catalogs are not enabled" — click the **Enable** button
6. Wait for enablement to complete (click refresh to check status)
7. Once enabled, the catalog details will be displayed:
   - **Catalog URL** — the REST catalog endpoint (e.g. `https://iceberg-catalog.<env-id>.altinity.cloud`)
   - **Auth Token** — a bearer token for catalog authentication
   - **Warehouse** — the S3 bucket URI (e.g. `s3://<bucket-name>-iceberg`)

---

## 6. Configure `.dlt/secrets.toml`

Edit `.dlt/secrets.toml` with your GitHub token and Altinity credentials:

```toml
# GitHub personal access token (needs repo read access)
access_token = "ghp_..."

[destination.iceberg]
catalog_type = "rest"

[destination.iceberg.credentials]
type = "rest"
uri = "https://iceberg-catalog.<env-id>.altinity.cloud"
warehouse = "s3://<bucket-name>-iceberg"

[destination.iceberg.credentials.properties]
token = "<your-altinity-auth-token>"
header.X-Iceberg-Access-Delegation = "vended-credentials"
```

> **Important:** Use `vended-credentials` (not `remote-signing`) for the `X-Iceberg-Access-Delegation` header. This tells the REST catalog to return temporary S3 credentials, which is required for the default PyArrow file IO to write data. Do **not** set `py-io-impl` — leave it as the default (`PyArrowFileIO`).

---

## 7. Run the Pipeline

```bash
uv run python github_api_pipeline.py
```

The pipeline loads two resources into the `github_iceberg_data` namespace in your Iceberg catalog:

- `repos` — all public repos for `dlt-hub` org (full replace on each run)
- `issues` — open issues for `dlt-hub/dlt`, loaded incrementally by `updated_at`

A successful run looks like:

```
Pipeline github_iceberg_pipeline load step completed in 10.73 seconds
1 load package(s) were loaded to destination iceberg and into dataset github_iceberg_data
Load package ... is LOADED and contains no failed jobs
```

---

## 8. Connect Altinity ClickHouse Cluster to the Iceberg Catalog

In the Altinity Cloud Manager:

1. Go to your **Cluster**
2. The first time you connect a data lake, you need to enable the `allow_experimental_database_iceberg` property. The ACM will prompt you to do this automatically when you first attempt to connect — click **Enable** when prompted.
3. Click **Connect to Data Lake Catalog**
4. Fill in the dialog:
   - **Catalog Type**: `Altinity.Cloud`
   - **Catalog**: `Default`
   - **Database**: `github_iceberg_data`
   - **Access Level**: `Read` (or `Read/Write`)
5. Click **Connect**

The ACM automatically configures the `DataLakeCatalog` engine and injects credentials. Once connected, all Iceberg tables in the `github_iceberg_data` namespace are queryable from ClickHouse.

---

## 9. Query the Data in ClickHouse

Use the **Query** tab in the ACM (or any ClickHouse client).

> **Note:** Run one query at a time without a semicolon — the console does not support multi-statement execution.

```sql
-- List connected databases
SHOW DATABASES

-- List tables in the Iceberg database
SHOW TABLES FROM github_iceberg_data

-- Query issues (note the namespace.table quoting)
SELECT * FROM github_iceberg_data."github_iceberg_data.issues" LIMIT 10

-- Query repos
SELECT * FROM github_iceberg_data."github_iceberg_data.repos" LIMIT 10

-- Count rows
SELECT count() FROM github_iceberg_data."github_iceberg_data.issues"
```

> **Why the double quoting?** Iceberg tables are stored under a namespace (`github_iceberg_data.issues`). ClickHouse exposes them with the full `namespace.table` name, which requires quoting because of the dot.

---

## 10. Incremental Updates

After the first run, subsequent pipeline runs are incremental:

- `issues` — only fetches issues updated since the last run
- `repos` — always does a full replace

```bash
uv run python github_api_pipeline.py
```

