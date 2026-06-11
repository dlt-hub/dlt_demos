# Ontology demo — Jaffle Shop → retail_sales CDM

End-to-end example of the dlthub transformations workflow: ingest a REST API
with dlt, annotate the source schema, derive a business ontology, design a
Kimball-style Canonical Data Model (CDM), and materialize it with
`@dlt.hub.transformation` functions.

```
jaffle_api.py            .schema/retail_sales/           transformations/
  (ingest)        →        taxonomy.json                   retail_sales_to_cdm.py
sample_shop_pipeline       sample_shop_pipeline.dbml  →      (star schema)
  (duckdb)                 ontology.ison / ontology.md     dataset: retail_sales
                           CDM.dbml
```

## Files in this demo

Each file is an artifact of one workflow step, in the order it was created:

| File | Step | What it is |
|---|---|---|
| [`jaffle_api.py`](jaffle_api.py) | ingest | dlt pipeline that loads the Jaffle Shop REST API into duckdb (`sample_shop_pipeline`, dataset `sample_shop`) |
| [`tools/get_sample_shop_schema.py`](tools/get_sample_shop_schema.py) | annotate-sources | helper that reads the pipeline's schema and exports it as DBML |
| [`.schema/retail_sales/sample_shop_pipeline.dbml`](.schema/retail_sales/sample_shop_pipeline.dbml) | annotate-sources | the source schema, annotated in place — every table carries a note with its business concept, role, or exclusion reason |
| [`.schema/retail_sales/taxonomy.json`](.schema/retail_sales/taxonomy.json) | annotate-sources | machine-readable record of all annotation decisions: concept definitions, table→concept mappings, natural keys, excluded tables; `_name` (`retail_sales`) names the CDM and the output dataset |
| [`.schema/retail_sales/ontology.ison`](.schema/retail_sales/ontology.ison) | create-ontology | the entity graph in [Graph ISON](https://graph.ison.dev/) format — entity nodes, attribute nodes, relationship edges, assumptions |
| [`.schema/retail_sales/ontology.md`](.schema/retail_sales/ontology.md) | create-ontology | human-readable version of the ontology: per-entity attribute and relationship tables plus all assumptions |
| [`.schema/retail_sales/CDM.dbml`](.schema/retail_sales/CDM.dbml) | generate-cdm | the implementation-ready star schema spec — table types, grains, surrogate keys, SCD types encoded as DBML notes |
| [`transformations/retail_sales_to_cdm.py`](transformations/retail_sales_to_cdm.py) | create-transformation | runnable `@dlt.hub.transformation` script that materializes the CDM from the source tables |

## Source

`jaffle_api.py` loads the public [Jaffle Shop API](https://jaffle-shop.dlthub.com/api/v1/)
into duckdb (pipeline `sample_shop_pipeline`, dataset `sample_shop`). Six
resources: `customers`, `orders`, `items`, `products`, `supplies`, `stores`.
The demo run uses `.add_limit(1)` — one API page (~100 rows) per resource.

Use cases driving the model: order & revenue analytics, customer purchase
behavior, product performance, store operations.

## Ontology

The ontology (`.schema/retail_sales/ontology.ison`, human-readable version in
[`ontology.md`](.schema/retail_sales/ontology.md)) is the entity graph derived
from the annotated source schema — six entities, five relationships, all
grounded in actual source columns:

```
Customer ◄──PLACED_BY── Order ──PLACED_AT──► Store
                          ▲
                          │ PART_OF
                       OrderItem ──FOR_PRODUCT──► Product ◄──SUPPLY_FOR── Supply
```

| Entity | Source table | Notes |
|---|---|---|
| Customer | `customers` | |
| Order | `orders` | header carries subtotal, tax, total |
| OrderItem | `items` | no quantity/price columns — one row per unit, price lives on Product |
| Product | `products` | natural key is `sku`, not a synthetic id |
| Supply | `supplies` | cost components; supply id repeats per product sku |
| Store | `stores` | |

Excluded: `orders__items` (dlt nested duplicate of `items`) and dlt internal
tables. Concept mappings and exclusions are recorded in
[`taxonomy.json`](.schema/retail_sales/taxonomy.json) and embedded as notes in
[`sample_shop_pipeline.dbml`](.schema/retail_sales/sample_shop_pipeline.dbml).

## CDM

[`CDM.dbml`](.schema/retail_sales/CDM.dbml) translates the ontology into a
Kimball star schema — two facts at different grains, four Type-1 dimensions:

**Dimensions**

| Table | Surrogate key | Notes |
|---|---|---|
| `dim_customer` | `customer_sk` = md5(id) | conformed |
| `dim_product` | `product_sk` = md5(sku) | conformed; carries current unit price |
| `dim_store` | `store_sk` = md5(id) | conformed |
| `dim_supply` | `supply_sk` = md5(id + sku) | FK to `dim_product`; id alone is not unique |

**Facts**

| Table | Grain | Measures |
|---|---|---|
| `fact_orders` | one row per order | `subtotal`, `tax_paid`, `order_total` |
| `fact_order_items` | one row per item per order | `unit_price` (joined from products) |

Design conventions:

- **Key contract: `varchar`** — every surrogate key is an md5 hex hash of the
  source natural key, applied consistently across dims and facts.
- **No NULL foreign keys** — conformed dimensions carry an `'unknown'`
  sentinel row; facts coalesce missing FKs to it.
- **Two facts, not one** — order-level tax/totals can't be cleanly allocated
  to lines, while product analysis needs line grain. `order_id` is kept as a
  degenerate dimension on both facts to bridge them.
- **Line items inherit `customer_sk`, `store_sk`, `ordered_at`** from the
  order header so line-grain analysis needs no fact-to-fact join.
- **Lineage** — every dimension carries `source_id` and `source_pipeline`.

## Transformation

[`transformations/retail_sales_to_cdm.py`](transformations/retail_sales_to_cdm.py)
implements the CDM as six `@dlt.hub.transformation` functions wrapped in a
`@dlt.source` — dimensions first, facts after. All logic is ANSI SQL; facts
derive surrogate keys from source columns directly (never from `dim_*`
outputs), and every computed column has an explicit `columns=` type hint.

The CDM is written into the **same duckdb database** as the source
(`.dlt/data/dev/sample_shop_pipeline.duckdb`, schema `retail_sales`), so raw
and modeled data can be joined in one connection. A separate
`retail_sales.duckdb` file would collide with the dataset name and trigger
duckdb's ambiguous catalog/schema error.

## Run it

```sh
uv sync
uv run python jaffle_api.py                          # 1. ingest source
uv run python transformations/retail_sales_to_cdm.py # 2. build the CDM
```

Inspect the output:

```sh
uv run python -c "
import duckdb
con = duckdb.connect('.dlt/data/dev/sample_shop_pipeline.duckdb', read_only=True)
print(con.execute('''
    SELECT p.name, COUNT(*) AS units, SUM(f.unit_price) AS revenue
    FROM retail_sales.fact_order_items f
    JOIN retail_sales.dim_product p USING (product_sk)
    GROUP BY p.name ORDER BY revenue DESC
''').df())
"
```
