import marimo

__generated_with = "0.23.3"
app = marimo.App(width="full")

with app.setup:
    import dlt
    import marimo as mo

    LANCEDB_TABLE_NAME = "repos"


@app.cell
def _():
    pipeline = dlt.attach(pipeline_name="lancedb_embeddings", destination="lancedb")
    return (pipeline,)


@app.cell(hide_code=True)
def _(pipeline):
    mo.vstack(
        [
            mo.md("## Pipeline Info"),
            mo.md(
                f"Pipeline is using destination type: {pipeline.destination.destination_type}"
            ),
        ]
    )
    return


@app.cell
def _(pipeline):
    client = pipeline.destination_client()
    table = client.db_client.open_table(LANCEDB_TABLE_NAME)
    return (table,)


@app.cell(hide_code=True)
def _(table):
    mo.vstack(
        [
            mo.md("## LanceDB Table Info"),
            mo.md(f"**URI:** `{table._conn.uri}`"),
            mo.md(f"**Rows:** {table.count_rows()}"),
            mo.md(f"**Version:** {table.version}"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(table):
    arrow_tbl = table.to_arrow()
    non_vector_cols = [c for c in arrow_tbl.column_names if c != "vector"]
    mo.vstack(
        [
            mo.md("## Repos (without vectors)"),
            arrow_tbl.select(non_vector_cols),
        ]
    )
    return (arrow_tbl,)


@app.cell(hide_code=True)
def _(arrow_tbl):
    mo.vstack(
        [
            mo.md("## Vector Schema"),
            mo.md(
                f"**Vector column dtype:** `{arrow_tbl.schema.field('vector').type}`"
            ),
        ]
    )
    return


@app.cell
def _(pipeline):
    pipeline.default_schema.to_mermaid()
    return


@app.cell(hide_code=True)
def _(pipeline):
    mo.vstack(
        [
            mo.md("## Pipeline Mermaid Diagram"),
            mo.mermaid(pipeline.default_schema.to_mermaid()),
        ]
    )
    return


@app.cell
def _():
    query_text = mo.ui.text(
        value="open source AI agent",
        label="Semantic search query",
        full_width=True,
    )
    query_text
    return (query_text,)


@app.cell(hide_code=True)
def _(query_text, table):
    results = table.search(query_text.value).limit(5).to_arrow().drop(["vector"])
    mo.vstack(
        [
            mo.md(f"## Top 5 results for: *{query_text.value}*"),
            results,
        ]
    )
    return


if __name__ == "__main__":
    app.run()
