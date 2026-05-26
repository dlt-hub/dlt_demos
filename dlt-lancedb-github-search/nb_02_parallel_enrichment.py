import marimo

__generated_with = "0.19.10"
app = marimo.App(width="full")

with app.setup:
    import dlt
    import marimo as mo


@app.cell
def _():
    pipeline = dlt.attach(
        pipeline_name="parallel_enrichment",
        destination="filesystem",
        dataset_name="parallel_enrichment",
    )
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
    pipeline.dataset().tables
    return


@app.cell(hide_code=True)
def _(pipeline):
    mo.vstack(
        [
            mo.md("## Enriched Repos"),
            pipeline.dataset().repos.arrow(),
        ]
    )
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
    import ibis

    return (ibis,)


@app.cell
def _(pipeline):
    repos = pipeline.dataset().repos.to_ibis()
    repos.to_pyarrow()
    return (repos,)


@app.cell(hide_code=True)
def _(ibis, repos):
    by_language = (
        repos.group_by("programming_language")
        .aggregate(repo_count=ibis._.repo_name.count())
        .order_by(ibis.desc("repo_count"))
    )
    mo.vstack(
        [
            mo.md("## Repos by Programming Language"),
            by_language.to_pyarrow(),
        ]
    )
    return


@app.cell(hide_code=True)
def _(ibis, repos):
    by_license = (
        repos.group_by("license")
        .aggregate(repo_count=ibis._.repo_name.count())
        .order_by(ibis.desc("repo_count"))
    )
    mo.vstack(
        [
            mo.md("## Repos by License"),
            by_license.to_pyarrow(),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
