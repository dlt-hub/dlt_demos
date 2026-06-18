import marimo

__generated_with = "0.19.10"
app = marimo.App(width="full")

with app.setup:
    import dlt
    import marimo as mo


@app.cell
def _():
    pipeline = dlt.attach(
        pipeline_name="github_stars_etl",
        destination="filesystem",
        dataset_name="github_stars",
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
            mo.md("## Repos With Stars"),
            pipeline.dataset().repos_with_stars.arrow(),
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
    repos = pipeline.dataset().repos_with_stars.to_ibis()
    repos.to_pyarrow()
    return (repos,)


@app.cell(hide_code=True)
def _(ibis, repos):
    stars_by_month = repos.group_by("month_id").aggregate(
        total_stars=ibis._.star_count.sum(),
        repo_count=ibis._.repo_name.count(),
    )
    mo.vstack(
        [
            mo.md("## Stars by Month"),
            stars_by_month.to_pyarrow(),
        ]
    )
    return


@app.cell(hide_code=True)
def _(ibis, repos):
    top_repos = (
        repos.group_by("repo_name")
        .aggregate(
            total_stars=ibis._.star_count.sum(),
        )
        .order_by(ibis.desc("total_stars"))
        .head(20)
    )
    mo.vstack(
        [
            mo.md("## Top 20 Repos by Total Stars"),
            top_repos.to_pyarrow(),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
