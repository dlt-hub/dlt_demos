# NOTE: this notebook assumes a successful run of `pipeline.py` against
# the local DuckDB destination at tmp/exa_websets/exa_websets.duckdb

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="full")

with app.setup:
    import os
    from pathlib import Path

    import dlt
    import marimo as mo


@app.cell(hide_code=True)
def _():
    from dlthub.common.license.license import create_self_signed_license

    os.environ["RUNTIME__LICENSE"] = create_self_signed_license(
        "dlthub.data_quality dlthub.destinations.iceberg dlthub.transformation"
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Attach to the pipeline

    - `dlt.attach` reconnects to the pipeline created by `pipeline.py` — no re-ingestion happens here

    ```py
    pipeline = dlt.attach(pipeline_name="exa_webset_ingest")

    pipeline.dataset()
    ```
    """)
    return


@app.cell
def _():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    PIPELINES_DIR = str(PROJECT_ROOT / "tmp" / "exa_websets" / "pipelines")
    DUCKDB_PATH = str(PROJECT_ROOT / "tmp" / "exa_websets" / "exa_websets.duckdb")

    pipeline = dlt.attach(
        pipeline_name="exa_webset_ingest",
        destination=dlt.destinations.duckdb(credentials=DUCKDB_PATH),
        pipelines_dir=PIPELINES_DIR,
    )
    return (pipeline,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Tables in the dataset

    ```py
    pipeline.dataset().tables
    ```
    """)
    return


@app.cell
def _(pipeline):
    pipeline.dataset().tables
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Build the items dataframe

    - Hide IDs, timestamps, and long-text fields that don't help the demo
    - Derive a `domain_type` column (`.ai` vs `other`) so we can slice on TLD
    - Stays generic across entity types — whatever entity-specific columns the ingest stage hoisted (company, person, article) survive the deny-list automatically

    ```py
    items_df = pipeline.dataset().webset_items.df()
    items_df["domain_type"] = items_df["url"].map(classify_domain)
    ```
    """)
    return


@app.cell
def _(pipeline):
    def _domain_type(url: str | None) -> str:
        if not url:
            return "unknown"
        u = url.lower().split("://", 1)[-1].split("/", 1)[0]
        if u.endswith(".ai"):
            return ".ai"
        if u.endswith(".com"):
            return ".com"
        return "other"

    items_df = pipeline.dataset().webset_items.df()
    items_df["domain_type"] = items_df["url"].map(_domain_type)
    items_df = items_df[["name", "url", "domain_type", "employees", "description"]]
    return (items_df,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Filter the items
    """)
    return


@app.cell
def _(items_df):
    employees_min = mo.ui.number(value=0, start=0, step=1, label="employees ≥")
    domain_filter = mo.ui.dropdown(
        options=["all", ".ai", ".com", "other"],
        value="all",
        label="domain",
    )
    include_unknown = mo.ui.checkbox(
        value=True,
        label="include rows with missing employee count",
    )
    mo.hstack([employees_min, domain_filter, include_unknown])
    return domain_filter, employees_min, include_unknown


@app.cell
def _(domain_filter, employees_min, include_unknown, items_df):
    _df = items_df.copy()
    if domain_filter.value != "all":
        _df = _df[_df["domain_type"] == domain_filter.value]
    _emp = _df["employees"]
    _mask = _emp >= employees_min.value
    if include_unknown.value:
        _mask = _mask | _emp.isna()
    _df = _df[_mask]
    mo.vstack(
        [
            mo.md(f"## Webset Items ({len(_df)} of {len(items_df)} rows)"),
            mo.ui.table(_df, selection=None, page_size=25),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Schema diagram

    - dlt infers a parent/child schema directly from the API response shape
    - Lists like `evaluations` and `enrichments` become child tables linked back to `webset_items` via `_dlt_parent_id`
    - This is what makes "missing attribute" queries trivial — every nested field is a normal column somewhere
    """)
    return


@app.cell
def _(pipeline):
    # Only render the tables we actually show in the demo. dlt's
    # to_mermaid() emits the full schema (including staging + internal),
    # so we filter the per-table blocks down to the four we care about.
    _show = {
        "webset_items",
        "webset_items__evaluations",
        "webset_items__enrichments",
    }
    _full = pipeline.default_schema.to_mermaid(
        hide_columns=False,
        hide_descriptions=True,
        include_dlt_tables=False,
    )

    _kept_lines: list[str] = []
    _skip_block = False
    for _line in _full.splitlines():
        _stripped = _line.strip()
        # Table block opens with `name{` (no space). Drop trailing `{` and any
        # leading column-list whitespace to extract the table name.
        if _stripped.endswith("{") and not _stripped.startswith("erDiagram"):
            _name = _stripped[:-1].strip()
            _skip_block = _name not in _show
            if not _skip_block:
                _kept_lines.append(_line)
            continue
        if _stripped == "}":
            if not _skip_block:
                _kept_lines.append(_line)
            _skip_block = False
            continue
        if _skip_block:
            continue
        # Relationship lines like `parent }|--|| child : "..."`
        if "--" in _stripped:
            _parts = _stripped.split()
            if len(_parts) >= 3 and (_parts[0] not in _show or _parts[2] not in _show):
                continue
        _kept_lines.append(_line)

    mo.vstack(
        [
            mo.md("## Pipeline Mermaid Diagram"),
            mo.mermaid("\n".join(_kept_lines)),
        ]
    )
    return


@app.cell
def _():
    import dlthub  # noqa: F401
    import dlthub.data_quality as dq

    return (dq,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Data Quality Checks

    We use `dlthub.data_quality` to flag rows with missing attributes so we
    can decide what to do (re-fetch, enrich, drop, etc).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Define the checks

    - Auto-discovers entity columns from the live schema — no hardcoded `company_*` names
    - One `is_not_null` per attribute Exa is supposed to resolve (description, name, employees, etc.)
    - One `is_in` on `entity_type` to catch drift if the API ever returns an unexpected type
    - Skips API-guaranteed fields (`id`, `url`, timestamps) and noise columns (`logo_url`, `picture_url`)

    ```py
    import dlthub.data_quality as dq

    checks = [
        dq.checks.is_not_null("name"),
        dq.checks.is_not_null("employees"),
        dq.checks.is_in("entity_type", ["company", "person", "article"]),
        dq.checks.case("employees > 0"),  # arbitrary row predicate
    ]
    ```
    """)
    return


@app.cell
def _(dq, pipeline):
    # Only check attributes a Webset user actually cares about — the
    # entity-specific fields Exa is supposed to resolve. Skip API-guaranteed
    # fields (id, urls, timestamps), dlt internals, and noise columns
    # (logo_url, picture_url) that don't represent missing intelligence.
    _skip = {
        "id", "source", "source_id", "webset_id",
        "created_at", "updated_at",
        "entity_type", "url",
        "logo_url", "picture_url",
    }
    items_columns = [
        c
        for c in pipeline.dataset().webset_items.columns
        if c not in _skip and not c.startswith("_dlt_")
    ]

    webset_items_checks = [dq.checks.is_not_null(c) for c in items_columns]
    webset_items_checks.append(
        dq.checks.is_in("entity_type", ["company", "person", "article"]),
    )
    return items_columns, webset_items_checks


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Raw check matrix

    - `prepare_checks(..., level="row")` returns a `dlt.Relation` — SQL pushed to DuckDB, no data movement
    - One boolean column per check, plus `_dlt_id` so you can join back to the original row
    - Levels available: `"row"`, `"table"`, `"dataset"`
    - This is what gets persisted to disk later

    ```py
    rel = dq.prepare_checks(
        pipeline.dataset().webset_items,
        checks,
        level="row",
    )
    rel.arrow()  # also: .df(), .iter_arrow(), .to_sql()
    ```
    """)
    return


@app.cell
def _(dq, webset_items_checks, pipeline):
    # Run row-level checks and return a relation with one boolean column per check
    _query_rel = dq.prepare_checks(
        pipeline.dataset().webset_items,
        webset_items_checks,
        level="row",
    )
    _query_rel.arrow()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### CheckSuite

    - Wraps multiple tables of checks in one object — here `webset_items` and `webset_items__evaluations`
    - Provides `.get_failures(table, check_name)` and `.get_successes(...)` that return the offending rows themselves, not just booleans
    - Use it when you want to drill from "X rows are missing Y" straight to "show me those X rows"

    ```py
    suite = dq.CheckSuite(
        pipeline.dataset(),
        checks={
            "webset_items": items_checks,
            "webset_items__evaluations": eval_checks,
        },
    )
    suite.get_failures("webset_items", "name__is_not_null").arrow()
    ```
    """)
    return


@app.cell
def _(dq, webset_items_checks, pipeline):
    # CheckSuite gives us .get_successes / .get_failures per check
    evaluations_checks = [
        dq.checks.is_in("satisfied", ["yes", "no", "unclear"]),
        dq.checks.is_not_null("reasoning"),
    ]

    check_suite = dq.CheckSuite(
        pipeline.dataset(),
        checks={
            "webset_items": webset_items_checks,
            "webset_items__evaluations": evaluations_checks,
        },
    )
    check_suite.checks
    return (check_suite,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Failure summary — rows missing each attribute

    Iterates every column-level check and counts failing rows. Columns with
    high failure counts are the attributes Exa struggled to resolve for this
    webset.
    """)
    return


@app.cell
def _(check_suite, items_columns):
    import pyarrow as pa

    summary_rows = []
    for col in items_columns:
        check_name = f"{col}__is_not_null"
        failures = check_suite.get_failures("webset_items", check_name).arrow()
        summary_rows.append({"column": col, "missing_rows": failures.num_rows})
    pa.Table.from_pylist(summary_rows)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""### Failures: evaluations with unexpected `satisfied` value""")
    return


@app.cell
def _(check_suite):
    check_suite.get_failures(
        "webset_items__evaluations", "satisfied__is_in"
    ).arrow()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Persist check results

    - `dq.prepare_checks(...)` returns a `dlt.Relation`, so we can pass it straight to `pipeline.run()`
    - Materializes a check-results table inside the pipeline's dataset (here: `dlt_data_quality_webset_items`)
    - Choice of level (`row` / `table` / `dataset`) determines what shape gets persisted
    - You can route results to a different pipeline/destination if you want check history separate from raw data

    ```py
    pipeline.run(
        [dq.prepare_checks(dataset.webset_items, checks, level="row").arrow()],
        table_name="dlt_data_quality_webset_items",
        write_disposition="replace",
    )
    ```
    """)
    return


@app.cell
def _(dq, webset_items_checks, pipeline):
    load_info = pipeline.run(
        [
            dq.prepare_checks(
                pipeline.dataset().webset_items,
                webset_items_checks,
                level="row",
            ).arrow(),
        ],
        table_name="dlt_data_quality_webset_items",
        write_disposition="replace",
    )
    load_info
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Persisted check results

    - Same boolean matrix as the raw view above, now durably written to DuckDB
    - You can join it back to `webset_items` on `_dlt_id` to attribute failures to the original Exa item
    - Re-running the cell with `write_disposition="replace"` keeps the table in sync with the latest checks
    """)
    return


@app.cell
def _(pipeline):
    mo.vstack(
        [
            mo.md("## Persisted Check Results"),
            pipeline.dataset().dlt_data_quality_webset_items.arrow(),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
