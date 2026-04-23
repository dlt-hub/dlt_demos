import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd

    return alt, mo


@app.cell
def _():
    import duckdb as _ddb
    class _Dataset:
        def __init__(self, con):
            self._con = con
        def __call__(self, query):
            _con = self._con
            class _R:
                def df(self): return _con.execute(query).df()
            return _R()
    _av_con = _ddb.connect("alpha_vantage.duckdb", read_only=True)
    _av_con.execute("SET search_path = 'market_data_20260419013010'")
    av_dataset = _Dataset(_av_con)
    _gdelt_con = _ddb.connect("gdelt.duckdb", read_only=True)
    _gdelt_con.execute("SET search_path = 'gdelt_data'")
    gdelt_dataset = _Dataset(_gdelt_con)
    return av_dataset, gdelt_dataset


@app.cell
def _(mo):
    mo.md("""
    # Geopolitical Market Correlation Dashboard
    Iran–USA news (GDELT) vs WTI oil and Bitcoin prices (Alpha Vantage)
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Market Prices
    """)
    return


@app.cell
def _(av_dataset):
    df_chart1 = av_dataset("""
        SELECT TRY_CAST(date AS DATE) AS date, TRY_CAST(value AS DOUBLE) AS price_usd
        FROM wti_oil_prices
        WHERE value != '.' AND TRY_CAST(date AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        ORDER BY date
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1):
    _chart = alt.Chart(df_chart1).mark_line(color="#f4a100", strokeWidth=2).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("price_usd:Q", title="WTI Price ($/barrel)", scale=alt.Scale(zero=False)),
        tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("price_usd:Q", title="$/bbl", format=".2f")],
    ).properties(title="WTI Crude Oil Price — Last 90 Days", width=700, height=300)
    _chart
    return


@app.cell
def _(av_dataset):
    df_chart2 = av_dataset("""
        SELECT TRY_CAST(date AS DATE) AS date, open_usd, high_usd, low_usd, close_usd
        FROM btc_daily_prices
        WHERE TRY_CAST(date AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        ORDER BY date
    """).df()
    return (df_chart2,)


@app.cell
def _(alt, df_chart2):
    _band = alt.Chart(df_chart2).mark_area(opacity=0.15, color="#f7931a").encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("low_usd:Q", scale=alt.Scale(zero=False)),
        y2=alt.Y2("high_usd:Q"),
    )
    _line = alt.Chart(df_chart2).mark_line(color="#f7931a", strokeWidth=2).encode(
        x="date:T",
        y=alt.Y("close_usd:Q", title="BTC Price (USD)", scale=alt.Scale(zero=False)),
        tooltip=[
            alt.Tooltip("date:T", title="Date"),
            alt.Tooltip("high_usd:Q", title="High", format=".0f"),
            alt.Tooltip("low_usd:Q", title="Low", format=".0f"),
            alt.Tooltip("close_usd:Q", title="Close", format=".0f"),
        ],
    )
    _chart = (_band + _line).properties(
        title="Bitcoin Price — Last 90 Days (with daily range)", width=700, height=300
    )
    _chart
    return


@app.cell
def _(df_chart1, df_chart2):
    _combined = df_chart1[["date", "price_usd"]].merge(
        df_chart2[["date", "close_usd"]], on="date", how="inner"
    )
    _combined = _combined.copy()
    _combined["WTI Oil"] = (_combined["price_usd"] / _combined["price_usd"].iloc[0] - 1) * 100
    _combined["Bitcoin"] = (_combined["close_usd"] / _combined["close_usd"].iloc[0] - 1) * 100
    df_chart3 = _combined[["date", "WTI Oil", "Bitcoin"]].melt(
        "date", var_name="asset", value_name="pct_change"
    )
    return (df_chart3,)


@app.cell
def _(alt, df_chart3):
    _chart = alt.Chart(df_chart3).mark_line(strokeWidth=2).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("pct_change:Q", title="% Change from 90 Days Ago"),
        color=alt.Color(
            "asset:N",
            scale=alt.Scale(domain=["WTI Oil", "Bitcoin"], range=["#1f77b4", "#f7931a"]),
        ),
        tooltip=[alt.Tooltip("date:T"), alt.Tooltip("asset:N"), alt.Tooltip("pct_change:Q", format=".1f")],
    ).properties(title="WTI vs Bitcoin — Normalized % Change (last 90 days)", width=700, height=300)
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Correlation Analysis
    """)
    return


@app.cell
def _(av_dataset):
    df_chart4 = av_dataset("""
        WITH wti_pct AS (
          SELECT TRY_CAST(date AS DATE) AS date, TRY_CAST(value AS DOUBLE) AS price,
                 LAG(TRY_CAST(value AS DOUBLE)) OVER (ORDER BY date) AS prev_price
          FROM wti_oil_prices WHERE value != '.'
            AND TRY_CAST(date AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        ),
        btc_pct AS (
          SELECT TRY_CAST(date AS DATE) AS date, close_usd,
                 LAG(close_usd) OVER (ORDER BY date) AS prev_close
          FROM btc_daily_prices
          WHERE TRY_CAST(date AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        )
        SELECT w.date,
               ROUND((w.price - w.prev_price) / w.prev_price * 100, 2) AS wti_pct_change,
               ROUND((b.close_usd - b.prev_close) / b.prev_close * 100, 2) AS btc_pct_change
        FROM wti_pct w JOIN btc_pct b ON w.date = b.date
        WHERE w.prev_price IS NOT NULL AND b.prev_close IS NOT NULL
    """).df()
    return (df_chart4,)


@app.cell
def _(alt, df_chart4):
    _chart = alt.Chart(df_chart4).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X("wti_pct_change:Q", title="WTI Daily % Change", scale=alt.Scale(zero=True)),
        y=alt.Y("btc_pct_change:Q", title="BTC Daily % Change", scale=alt.Scale(zero=True)),
        color=alt.condition(
            alt.datum.wti_pct_change > 0,
            alt.value("#2ca02c"),
            alt.value("#d62728"),
        ),
        tooltip=[
            alt.Tooltip("date:T", title="Date"),
            alt.Tooltip("wti_pct_change:Q", title="WTI %", format=".2f"),
            alt.Tooltip("btc_pct_change:Q", title="BTC %", format=".2f"),
        ],
    ).properties(
        title="WTI vs BTC Daily % Change — Correlation Scatter (last 90 days)", width=500, height=400
    )
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Geopolitical News Coverage
    """)
    return


@app.cell
def _(gdelt_dataset):
    df_chart5 = gdelt_dataset("""
        SELECT DATE_TRUNC('day', seendate)::DATE AS news_date, COUNT(*) AS article_count
        FROM articles GROUP BY 1 ORDER BY 1
    """).df()
    return (df_chart5,)


@app.cell
def _(alt, df_chart5):
    _chart = alt.Chart(df_chart5).mark_bar(color="#d62728").encode(
        x=alt.X("news_date:T", title="Date"),
        y=alt.Y("article_count:Q", title="Article Count"),
        tooltip=[alt.Tooltip("news_date:T", title="Date"), alt.Tooltip("article_count:Q", title="Articles")],
    ).properties(title="Iran-USA News Volume by Day (GDELT)", width=700, height=250)
    _chart
    return


@app.cell
def _(gdelt_dataset):
    df_chart8 = gdelt_dataset("""
        SELECT domain, COUNT(*) AS article_count
        FROM articles WHERE domain IS NOT NULL AND domain != ''
        GROUP BY 1 ORDER BY 2 DESC LIMIT 10
    """).df()
    return (df_chart8,)


@app.cell
def _(alt, df_chart8):
    _chart = alt.Chart(df_chart8).mark_bar(color="#17becf").encode(
        x=alt.X("article_count:Q", title="Article Count"),
        y=alt.Y("domain:N", sort="-x", title="Domain"),
        tooltip=[alt.Tooltip("domain:N", title="Domain"), alt.Tooltip("article_count:Q", title="Articles")],
    ).properties(title="Top 10 Domains Covering Iran-USA News", width=600, height=300)
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ### Top Headlines on Peak News Days
    """)
    return


@app.cell
def _(gdelt_dataset):
    df_chart16 = gdelt_dataset("""
        WITH top_days AS (
            SELECT DATE_TRUNC('day', seendate)::DATE AS day
            FROM articles
            GROUP BY 1
            ORDER BY COUNT(*) DESC
            LIMIT 5
        )
        SELECT
            td.day AS date,
            a.title,
            a.domain
        FROM top_days td
        JOIN articles a ON DATE_TRUNC('day', a.seendate)::DATE = td.day
        QUALIFY ROW_NUMBER() OVER (PARTITION BY td.day ORDER BY a.seendate) <= 5
        ORDER BY td.day DESC, a.seendate
    """).df()
    return (df_chart16,)


@app.cell
def _(df_chart16, mo):
    _table = mo.ui.table(df_chart16)
    _table
    return


@app.cell
def _(mo):
    mo.md("""
    ## Market Volatility
    """)
    return


@app.cell
def _(av_dataset):
    df_chart9 = av_dataset("""
        WITH lagged AS (
          SELECT TRY_CAST(date AS DATE) AS date, TRY_CAST(value AS DOUBLE) AS price,
                 LAG(TRY_CAST(value AS DOUBLE)) OVER (ORDER BY date) AS prev_price
          FROM wti_oil_prices WHERE value != '.'
            AND TRY_CAST(date AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        )
        SELECT date, ROUND((price - prev_price) / prev_price * 100, 2) AS pct_change
        FROM lagged WHERE prev_price IS NOT NULL
    """).df()
    return (df_chart9,)


@app.cell
def _(alt, df_chart9):
    _chart = alt.Chart(df_chart9).mark_bar(color="#f4a100", opacity=0.8).encode(
        x=alt.X("pct_change:Q", bin=alt.Bin(step=0.5), title="Daily % Change"),
        y=alt.Y("count():Q", title="Number of Days"),
        tooltip=[alt.Tooltip("pct_change:Q", bin=alt.Bin(step=0.5)), alt.Tooltip("count():Q", title="Days")],
    ).properties(title="WTI Daily % Change — Distribution (last 90 days)", width=600, height=300)
    _chart
    return


@app.cell
def _(av_dataset):
    df_chart10 = av_dataset("""
        SELECT TRY_CAST(date AS DATE) AS date,
               ROUND((high_usd - low_usd) / close_usd * 100, 2) AS range_pct
        FROM btc_daily_prices
        WHERE TRY_CAST(date AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        ORDER BY date
    """).df()
    return (df_chart10,)


@app.cell
def _(alt, df_chart10):
    _chart = alt.Chart(df_chart10).mark_area(color="#f7931a", opacity=0.6).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("range_pct:Q", title="Daily Range (% of close price)"),
        tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("range_pct:Q", title="Range %", format=".2f")],
    ).properties(
        title="Bitcoin Daily Volatility — High−Low Range as % of Close (last 90 days)", width=700, height=280
    )
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## News–Market Correlation
    """)
    return


@app.cell
def _(df_chart5, df_chart9):
    _news = df_chart5.rename(columns={"news_date": "date"})
    df_chart11 = _news.merge(df_chart9, on="date", how="inner")
    return (df_chart11,)


@app.cell
def _(alt, df_chart11):
    _chart = alt.Chart(df_chart11).mark_circle(size=80, color="#d62728", opacity=0.7).encode(
        x=alt.X("article_count:Q", title="Iran-USA Articles That Day"),
        y=alt.Y("pct_change:Q", title="WTI % Change That Day"),
        tooltip=[
            alt.Tooltip("date:T", title="Date"),
            alt.Tooltip("article_count:Q", title="Articles"),
            alt.Tooltip("pct_change:Q", title="WTI % Change", format=".2f"),
        ],
    ).properties(title="Iran-USA News Volume vs WTI Daily % Change", width=500, height=400)
    _chart
    return


@app.cell
def _(df_chart5, df_chart9):
    _news_dates = set(df_chart5["news_date"].astype(str))
    df_chart12 = df_chart9.copy()
    df_chart12["day_type"] = df_chart12["date"].astype(str).apply(
        lambda d: "News Day" if d in _news_dates else "Quiet Day"
    )
    return (df_chart12,)


@app.cell
def _(alt, df_chart12):
    _chart = alt.Chart(df_chart12).mark_boxplot(extent="min-max").encode(
        x=alt.X("day_type:N", title="Day Type"),
        y=alt.Y("pct_change:Q", title="WTI Daily % Change"),
        color=alt.Color(
            "day_type:N",
            scale=alt.Scale(domain=["News Day", "Quiet Day"], range=["#d62728", "#aec7e8"]),
        ),
        tooltip=[alt.Tooltip("day_type:N"), alt.Tooltip("pct_change:Q", format=".2f")],
    ).properties(title="WTI % Change: News Days vs Quiet Days", width=400, height=400)
    _chart
    return


@app.cell
def _(df_chart1, df_chart5):
    _news = df_chart5.rename(columns={"news_date": "date"})
    _lag = df_chart1.merge(_news, on="date", how="left")
    _lag["article_count"] = _lag["article_count"].fillna(0)
    _lag["wti_norm"] = (
        (_lag["price_usd"] - _lag["price_usd"].min())
        / (_lag["price_usd"].max() - _lag["price_usd"].min())
    )
    _lag["news_norm"] = (
        (_lag["article_count"] - _lag["article_count"].min())
        / (_lag["article_count"].max() - _lag["article_count"].min() + 1e-9)
    )
    df_chart13 = _lag[["date", "wti_norm", "news_norm"]].melt(
        "date", var_name="series", value_name="value"
    )
    df_chart13 = df_chart13.assign(
        series=df_chart13["series"].map(
            {"wti_norm": "WTI Price (normalized)", "news_norm": "News Volume (normalized)"}
        )
    )
    return (df_chart13,)


@app.cell
def _(alt, df_chart13):
    _chart = alt.Chart(df_chart13).mark_line(strokeWidth=2).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title="Normalized Value (0–1)"),
        color=alt.Color(
            "series:N",
            scale=alt.Scale(
                domain=["WTI Price (normalized)", "News Volume (normalized)"],
                range=["#f4a100", "#d62728"],
            ),
        ),
        tooltip=[alt.Tooltip("date:T"), alt.Tooltip("series:N"), alt.Tooltip("value:Q", format=".2f")],
    ).properties(
        title="Iran-USA News Spikes vs WTI Price — Normalized Overlay", width=700, height=320
    )
    _chart
    return


@app.cell
def _(df_chart1, df_chart2, df_chart5):
    _wti = df_chart1[["date", "price_usd"]].copy()
    _btc = df_chart2[["date", "close_usd"]].copy()
    _news = df_chart5.rename(columns={"news_date": "date"}).copy()
    _m = _wti.merge(_btc, on="date", how="inner").merge(_news, on="date", how="left")
    _m["article_count"] = _m["article_count"].fillna(0)
    for _col, _label in [("price_usd", "WTI Oil"), ("close_usd", "Bitcoin"), ("article_count", "News Volume")]:
        _mn, _mx = _m[_col].min(), _m[_col].max()
        _m[_label] = (_m[_col] - _mn) / (_mx - _mn + 1e-9)
    df_chart14 = _m[["date", "WTI Oil", "Bitcoin", "News Volume"]].melt(
        "date", var_name="series", value_name="value"
    )
    return (df_chart14,)


@app.cell
def _(alt, df_chart14):
    _chart = alt.Chart(df_chart14).mark_line(strokeWidth=2).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title="Normalized Value (0–1)"),
        color=alt.Color(
            "series:N",
            scale=alt.Scale(
                domain=["WTI Oil", "Bitcoin", "News Volume"],
                range=["#f4a101", "#f2399a", "#d62728"],
            ),
        ),
        tooltip=[alt.Tooltip("date:T"), alt.Tooltip("series:N"), alt.Tooltip("value:Q", format=".2f")],
    ).properties(title="Iran-USA News + WTI + Bitcoin — Triple Normalized Overlay", width=700, height=320)
    _chart
    return


@app.cell
def _(df_chart5, df_chart9):
    import pandas as _pd
    _news = df_chart5.rename(columns={"news_date": "date"}).copy()
    _news["date"] = _pd.to_datetime(_news["date"])
    _wti = df_chart9.copy()
    _wti["date"] = _pd.to_datetime(_wti["date"])
    _wti["prev_date"] = _wti["date"] - _pd.Timedelta(days=1)
    df_chart15 = _news.merge(
        _wti[["prev_date", "pct_change"]],
        left_on="date", right_on="prev_date",
        how="inner",
    )[["date", "article_count", "pct_change"]].rename(columns={"pct_change": "next_day_wti_pct"})
    return (df_chart15,)


@app.cell
def _(alt, df_chart15):
    _chart = alt.Chart(df_chart15).mark_circle(size=70, opacity=0.7).encode(
        x=alt.X("article_count:Q", title="Iran-USA Articles (Day T)"),
        y=alt.Y("next_day_wti_pct:Q", title="WTI % Change (Day T+1)", scale=alt.Scale(zero=True)),
        color=alt.condition(
            alt.datum.next_day_wti_pct > 0,
            alt.value("#2ca02c"),
            alt.value("#d62728"),
        ),
        tooltip=[
            alt.Tooltip("date:T", title="Date"),
            alt.Tooltip("article_count:Q", title="Articles"),
            alt.Tooltip("next_day_wti_pct:Q", title="Next-day WTI %", format=".2f"),
        ],
    ).properties(title="Does News Volume Predict Next-Day WTI Price Move?", width=500, height=400)
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Events Deep Dive
    """)
    return


@app.cell
def _(av_dataset):
    df_chart17_raw = av_dataset("""
        SELECT
            TRY_CAST(w.date AS DATE) AS date,
            TRY_CAST(w.value AS DOUBLE) AS wti_price,
            b.close_usd AS btc_close
        FROM wti_oil_prices w
        JOIN btc_daily_prices b ON TRY_CAST(w.date AS DATE) = TRY_CAST(b.date AS DATE)
        WHERE w.value != '.'
          AND TRY_CAST(w.date AS DATE) BETWEEN '2026-04-05' AND '2026-04-19'
        ORDER BY date
    """).df()
    _base_wti = df_chart17_raw["wti_price"].iloc[0]
    _base_btc = df_chart17_raw["btc_close"].iloc[0]
    df_chart17_raw["WTI Oil"] = (df_chart17_raw["wti_price"] / _base_wti - 1) * 100
    df_chart17_raw["Bitcoin"] = (df_chart17_raw["btc_close"] / _base_btc - 1) * 100
    df_chart17 = df_chart17_raw[["date", "WTI Oil", "Bitcoin"]].melt(
        "date", var_name="asset", value_name="pct_from_apr5"
    )
    return (df_chart17,)


@app.cell
def _(alt, df_chart17):
    _chart = alt.Chart(df_chart17).mark_line(strokeWidth=2.5).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("pct_from_apr5:Q", title="% Change from Apr 5"),
        color=alt.Color(
            "asset:N",
            scale=alt.Scale(domain=["WTI Oil", "Bitcoin"], range=["#1f77b4", "#f7931a"]),
        ),
        tooltip=[
            alt.Tooltip("date:T"),
            alt.Tooltip("asset:N"),
            alt.Tooltip("pct_from_apr5:Q", format=".1f", title="% from Apr 5"),
        ],
    ).properties(title="WTI vs BTC During Strait of Hormuz Threat (Apr 5–19)", width=700, height=320)
    _chart
    return


if __name__ == "__main__":
    app.run()
