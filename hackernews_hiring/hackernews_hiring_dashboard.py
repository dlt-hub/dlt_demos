import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import dlt
    from wordcloud import WordCloud
    import io

    return WordCloud, alt, dlt, io, mo


@app.cell
def _(dlt):
    pipeline = dlt.pipeline("hackernews_hiring", destination="warehouse", dataset_name="hn_hiring")
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(dataset, mo):
    months_df = dataset("""
        SELECT
            thread_id,
            STRFTIME(TO_TIMESTAMP(MIN(time)), '%b %Y') AS month
        FROM hn_hiring.tool_extractions
        GROUP BY thread_id
        ORDER BY MIN(time)
    """).df()
    month_list = months_df["month"].tolist()
    latest_thread = int(months_df["thread_id"].iloc[-1])
    latest_month = month_list[-1]
    month_range = "–".join([month_list[0].split()[0], month_list[-1]]) if len(month_list) > 1 else month_list[0]
    mo.md(f"## Hacker News Who's Hiring: Data Stack Analysis ({month_range})")
    return latest_month, latest_thread, month_list, month_range


@app.cell
def _():
    # Frontend and general-purpose tools excluded from data/infra charts.
    # These tools genuinely appear in data job posts — many companies want full-stack
    # data engineers — but they're not what this analysis is about. Excluding them is
    # an editorial decision, not a statistical one.
    EXCLUDED = {
        'react', 'typescript', 'javascript', 'vue', 'angular', 'next.js', 'nuxt',
        'svelte', 'html', 'css', 'tailwind', 'redux', 'webpack', 'vite', 'babel',
        'node.js', 'node', 'express', 'nestjs', 'ruby', 'rails', 'php', 'laravel',
        'jquery', 'flutter', 'react native', 'swift', 'kotlin', 'ios', 'android',
        'expo', 'vercel', 'stripe', 'graphql', 'rest', 'sass', 'bootstrap',
    }
    return (EXCLUDED,)


@app.cell
def _(latest_month, mo):
    mo.md(f"""
    ### Current Month Snapshot — {latest_month}

    The first two charts split job posts by role type — data/ML/analytics vs platform/infra/devops/SRE — so you can see how different the tool stacks are between these communities. The third buckets tools into three categories to answer: how much has AI bled into data hiring?

    **A note on filtering:** frontend and general-purpose tools (React, TypeScript, Vue, Node.js, etc.) are excluded from these charts. They do appear in data job posts — many companies want full-stack data engineers — but they're not what this analysis is about. This is an editorial decision, not a statistical one.
    """)
    return


@app.cell
def _(EXCLUDED, dataset, latest_thread):
    df_chart1a = dataset(f"""
        SELECT lower(trim(t.value)) AS tool, COUNT(*) AS mentions
        FROM hn_hiring.tool_extractions__named_tools t
        JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
        JOIN hn_hiring.job_posts j ON j.comment_id = e.comment_id
        WHERE e.thread_id = {latest_thread}
          AND (
              lower(j.role) LIKE '%data%'
           OR lower(j.role) LIKE '%ml%'
           OR lower(j.role) LIKE '%machine learn%'
           OR lower(j.role) LIKE '%analyt%'
          )
        GROUP BY lower(trim(t.value))
        ORDER BY mentions DESC
    """).df()
    df_chart1a = df_chart1a[~df_chart1a["tool"].isin(EXCLUDED)].head(25)
    return (df_chart1a,)


@app.cell
def _(alt, df_chart1a, latest_month, mo):
    _order = df_chart1a.sort_values("mentions", ascending=False)["tool"].tolist()
    _chart = alt.Chart(df_chart1a).mark_bar(color="#4C78A8").encode(
        x=alt.X("mentions:Q", title="Job Posts Mentioning Tool"),
        y=alt.Y("tool:N", sort=_order, title=None),
        tooltip=["tool:N", "mentions:Q"]
    ).properties(
        title=f"Top 25 Tools — Data / ML / Analytics Roles ({latest_month})",
        width=500,
        height=500
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(EXCLUDED, dataset, latest_thread):
    df_chart1b = dataset(f"""
        SELECT lower(trim(t.value)) AS tool, COUNT(*) AS mentions
        FROM hn_hiring.tool_extractions__named_tools t
        JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
        JOIN hn_hiring.job_posts j ON j.comment_id = e.comment_id
        WHERE e.thread_id = {latest_thread}
          AND (
              lower(j.role) LIKE '%platform%'
           OR lower(j.role) LIKE '%infra%'
           OR lower(j.role) LIKE '%devops%'
           OR lower(j.role) LIKE '%sre%'
          )
        GROUP BY lower(trim(t.value))
        ORDER BY mentions DESC
    """).df()
    df_chart1b = df_chart1b[~df_chart1b["tool"].isin(EXCLUDED)].head(25)
    return (df_chart1b,)


@app.cell
def _(alt, df_chart1b, latest_month, mo):
    _order = df_chart1b.sort_values("mentions", ascending=False)["tool"].tolist()
    _chart = alt.Chart(df_chart1b).mark_bar(color="#72B7B2").encode(
        x=alt.X("mentions:Q", title="Job Posts Mentioning Tool"),
        y=alt.Y("tool:N", sort=_order, title=None),
        tooltip=["tool:N", "mentions:Q"]
    ).properties(
        title=f"Top 25 Tools — Platform / Infra / DevOps / SRE Roles ({latest_month})",
        width=500,
        height=500
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(dataset, latest_thread):
    df_chart2 = dataset(f"""
        WITH categorized AS (
            SELECT lower(trim(t.value)) AS tool,
                CASE
                    WHEN lower(trim(t.value)) IN ('openai','anthropic','langchain','llamaindex','pinecone','weaviate','pgvector','chroma','qdrant','hugging face','mistral','claude','gpt','llm','ollama','cohere','together ai','replicate','langsmith','langfuse') THEN 'AI / LLM'
                    WHEN lower(trim(t.value)) IN ('aws','gcp','azure','s3','bigquery','redshift','snowflake','databricks','google cloud','amazon web services','ec2','lambda','cloudwatch','sagemaker','vertex ai','azure ml','cloud run') THEN 'Cloud / Warehouse'
                    WHEN lower(trim(t.value)) IN ('dbt','airflow','spark','kafka','flink','dagster','prefect','luigi','beam','nifi','dlt','fivetran','stitch','airbyte','meltano','great expectations','duckdb','trino','presto','hive') THEN 'Data Stack'
                    ELSE NULL
                END AS category,
                COUNT(*) AS mentions
            FROM hn_hiring.tool_extractions__named_tools t
            JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
            WHERE e.thread_id = {latest_thread}
            GROUP BY lower(trim(t.value))
        )
        SELECT tool, category, mentions
        FROM categorized
        WHERE category IS NOT NULL
        ORDER BY category, mentions DESC
    """).df()
    df_chart2 = df_chart2.groupby("category").head(8).reset_index(drop=True)
    return (df_chart2,)


@app.cell
def _(alt, df_chart2, latest_month, mo):
    _tool_order2 = df_chart2.sort_values("mentions", ascending=False)["tool"].tolist()
    _chart = alt.Chart(df_chart2).mark_bar().encode(
        x=alt.X("mentions:Q", title="Mentions"),
        y=alt.Y("tool:N", sort=_tool_order2, title=None),
        color=alt.Color("category:N",
            scale=alt.Scale(
                domain=["AI / LLM", "Cloud / Warehouse", "Data Stack"],
                range=["#F58518", "#4C78A8", "#72B7B2"]
            ),
            legend=alt.Legend(title="Category")
        ),
        tooltip=["tool:N", "category:N", "mentions:Q"]
    ).properties(
        title=f"AI / LLM vs Cloud vs Data Stack — {latest_month}",
        width=500,
        height=450
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo, month_range):
    mo.md(f"""
    ### Trends Over Time ({month_range})

    These charts track specific tool mentions as a percentage of all job posts each month, so volume differences between months don't skew the comparison. Chart 3 tracks cloud provider dominance — AWS, GCP, and Azure — to see if any shift is happening in which cloud data teams are hiring for. Chart 4 tracks AI coding tools explicitly named in job posts (Cursor, Copilot, Claude, Claude Code, Gemini) — these are companies that consider AI-assisted development part of the role, not just a nice-to-have.
    """)
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        WITH posts_per_month AS (
            SELECT thread_id, COUNT(DISTINCT comment_id) AS total
            FROM hn_hiring.tool_extractions
            GROUP BY thread_id
        )
        SELECT
            STRFTIME(TO_TIMESTAMP(MIN(e.time)), '%b %Y') AS month,
            lower(trim(t.value)) AS cloud,
            COUNT(*) * 100.0 / p.total AS pct_posts
        FROM hn_hiring.tool_extractions__named_tools t
        JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
        JOIN posts_per_month p ON p.thread_id = e.thread_id
        WHERE lower(trim(t.value)) IN ('aws', 'gcp', 'azure')
        GROUP BY lower(trim(t.value)), e.thread_id, p.total
        ORDER BY MIN(e.time)
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3, mo, month_list):
    _chart = alt.Chart(df_chart3).mark_line(point=True, strokeWidth=2).encode(
        x=alt.X("month:N", sort=month_list, title=None),
        y=alt.Y("pct_posts:Q", title="% of Job Posts"),
        color=alt.Color("cloud:N",
            scale=alt.Scale(
                domain=["aws", "gcp", "azure"],
                range=["#F58518", "#4C78A8", "#72B7B2"]
            ),
            legend=alt.Legend(title="Cloud")
        ),
        tooltip=["cloud:N", "month:N", alt.Tooltip("pct_posts:Q", format=".1f")]
    ).properties(
        title="Cloud Provider Mentions Over Time — AWS vs GCP vs Azure",
        width=500,
        height=300
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(dataset):
    df_chart4 = dataset("""
        WITH posts_per_month AS (
            SELECT thread_id, COUNT(DISTINCT comment_id) AS total
            FROM hn_hiring.tool_extractions
            GROUP BY thread_id
        )
        SELECT
            STRFTIME(TO_TIMESTAMP(MIN(e.time)), '%b %Y') AS month,
            lower(trim(t.value)) AS tool,
            COUNT(*) * 100.0 / p.total AS pct_posts
        FROM hn_hiring.tool_extractions__named_tools t
        JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
        JOIN posts_per_month p ON p.thread_id = e.thread_id
        WHERE lower(trim(t.value)) IN ('claude', 'claude code', 'cursor', 'copilot', 'gemini', 'codex')
        GROUP BY lower(trim(t.value)), e.thread_id, p.total
        ORDER BY MIN(e.time)
    """).df()
    return (df_chart4,)


@app.cell
def _(alt, df_chart4, mo, month_list):
    _chart = alt.Chart(df_chart4).mark_line(point=True, strokeWidth=2).encode(
        x=alt.X("month:N", sort=month_list, title=None),
        y=alt.Y("pct_posts:Q", title="% of Job Posts"),
        color=alt.Color("tool:N", legend=alt.Legend(title="AI Tool")),
        tooltip=["tool:N", "month:N", alt.Tooltip("pct_posts:Q", format=".1f")]
    ).properties(
        title="AI Coding Tools Named in Job Posts Over Time",
        width=500,
        height=300
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo, month_range):
    mo.md(f"""
    ### Tool Landscapes — {month_range}

    Two word clouds showing which tools dominate each community, sized by total mentions across all months. The same frontend tools excluded from the bar charts are excluded here. Data/ML roles and platform/infra roles are kept separate — a data engineer's stack looks nothing like an SRE's, and mixing them buries the signal.
    """)
    return


@app.cell
def _(EXCLUDED, WordCloud, dataset, io, mo):
    _df = dataset("""
        SELECT lower(trim(t.value)) AS tool, COUNT(*) AS mentions
        FROM hn_hiring.tool_extractions__named_tools t
        JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
        JOIN hn_hiring.job_posts j ON j.comment_id = e.comment_id
        WHERE lower(j.role) LIKE '%data%'
           OR lower(j.role) LIKE '%ml%'
           OR lower(j.role) LIKE '%machine learn%'
           OR lower(j.role) LIKE '%analyt%'
        GROUP BY lower(trim(t.value))
    """).df()
    _df = _df[~_df["tool"].isin(EXCLUDED)]
    _freq = dict(zip(_df["tool"], _df["mentions"]))
    _wc = WordCloud(width=900, height=400, background_color="white", colormap="Blues", max_words=80).generate_from_frequencies(_freq)
    _buf = io.BytesIO()
    _wc.to_image().save(_buf, format="PNG")
    mo.vstack([mo.md("**Data / ML / Analytics roles**"), mo.image(_buf.getvalue())])
    return


@app.cell
def _(EXCLUDED, WordCloud, dataset, io, mo):
    _df = dataset("""
        SELECT lower(trim(t.value)) AS tool, COUNT(*) AS mentions
        FROM hn_hiring.tool_extractions__named_tools t
        JOIN hn_hiring.tool_extractions e ON t._dlt_parent_id = e._dlt_id
        JOIN hn_hiring.job_posts j ON j.comment_id = e.comment_id
        WHERE lower(j.role) LIKE '%platform%'
           OR lower(j.role) LIKE '%infra%'
           OR lower(j.role) LIKE '%devops%'
           OR lower(j.role) LIKE '%sre%'
        GROUP BY lower(trim(t.value))
    """).df()
    _df = _df[~_df["tool"].isin(EXCLUDED)]
    _freq = dict(zip(_df["tool"], _df["mentions"]))
    _wc = WordCloud(width=900, height=400, background_color="white", colormap="GnBu", max_words=80).generate_from_frequencies(_freq)
    _buf = io.BytesIO()
    _wc.to_image().save(_buf, format="PNG")
    mo.vstack([mo.md("**Platform / Infra / DevOps / SRE roles**"), mo.image(_buf.getvalue())])
    return


@app.cell
def _(mo):
    mo.md("""
    ### What Companies Are Building From Scratch

    A subset of job posts mention custom or homegrown tooling — internal platforms, bespoke pipelines, purpose-built infrastructure that doesn't have a product name. Claude extracted a short description of what each company is building. These are sorted by description length as a rough proxy for how specific and interesting the use case is.
    """)
    return


@app.cell
def _(dataset):
    df_custom = dataset("""
        SELECT
            COALESCE(j.company_name, '—') AS company,
            COALESCE(j.role, '—') AS role,
            e.custom_tooling_notes AS what_they_re_building,
            STRFTIME(TO_TIMESTAMP(e.time), '%b %Y') AS month
        FROM hn_hiring.tool_extractions e
        JOIN hn_hiring.job_posts j ON j.comment_id = e.comment_id
        WHERE e.has_custom_tooling = true
          AND e.custom_tooling_notes IS NOT NULL
          AND LENGTH(e.custom_tooling_notes) > 40
        ORDER BY LENGTH(e.custom_tooling_notes) DESC
        LIMIT 60
    """).df()
    return (df_custom,)


@app.cell
def _(df_custom, mo):
    mo.ui.table(df_custom, selection=None)
    return


if __name__ == "__main__":
    app.run()
