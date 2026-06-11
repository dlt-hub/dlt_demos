# Ontology — retail_sales

Entity graph for the `retail_sales` CDM, derived from `sample_shop_pipeline` (Jaffle Shop API, duckdb).
All entities come from a single source pipeline, so there are no cross-source natural keys or merge strategies.

```
Customer ◄──PLACED_BY── Order ──PLACED_AT──► Store
                          ▲
                          │ PART_OF
                       OrderItem ──FOR_PRODUCT──► Product ◄──SUPPLY_FOR── Supply
```

## Customer

An individual who places orders.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| id | text | customers | primary key |
| name | text | customers | |

| Relationship | Direction | Via |
|---|---|---|
| PLACED_BY | Order → Customer | orders.customer_id |

## Order

A purchase transaction with subtotal, tax, and total, placed by a customer at a store.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| id | text | orders | primary key |
| customer_id | text | orders | FK → customers.id |
| store_id | text | orders | FK → stores.id |
| ordered_at | timestamp | orders | |
| subtotal | double | orders | |
| tax_paid | double | orders | |
| order_total | double | orders | |

| Relationship | Direction | Via |
|---|---|---|
| PLACED_BY | Order → Customer | orders.customer_id |
| PLACED_AT | Order → Store | orders.store_id |
| PART_OF | OrderItem → Order | items.order_id |

## OrderItem

A line item linking an order to a product SKU.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| id | text | items | primary key |
| order_id | text | items | FK → orders.id |
| sku | text | items | FK → products.sku |

| Relationship | Direction | Via |
|---|---|---|
| PART_OF | OrderItem → Order | items.order_id |
| FOR_PRODUCT | OrderItem → Product | items.sku |

## Product

A sellable item with type, price, and description.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| sku | text | products | primary key |
| name | text | products | |
| type | text | products | e.g. jaffle vs beverage |
| price | double | products | unit price |
| description | text | products | |

| Relationship | Direction | Via |
|---|---|---|
| FOR_PRODUCT | OrderItem → Product | items.sku |
| SUPPLY_FOR | Supply → Product | supplies.sku |

## Supply

An ingredient/supply with cost and perishable flag, consumed by a product.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| id | text | supplies | primary key (repeats per sku — see assumptions) |
| name | text | supplies | |
| cost | double | supplies | |
| perishable | bool | supplies | |
| sku | text | supplies | FK → products.sku |

| Relationship | Direction | Via |
|---|---|---|
| SUPPLY_FOR | Supply → Product | supplies.sku |

## Store

A physical location with opening date and tax rate.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| id | text | stores | primary key |
| name | text | stores | |
| opened_at | timestamp | stores | |
| tax_rate | double | stores | |

| Relationship | Direction | Via |
|---|---|---|
| PLACED_AT | Order → Store | orders.store_id |

## Assumptions & exclusions

1. **Single source** — every entity maps to exactly one table in `sample_shop_pipeline`; no cross-source stitching needed.
2. **orders__items excluded** — dlt nested child table duplicating the top-level `items` resource (identical columns).
3. **OrderItem has no quantity column** — each row represents one unit; quantities are derived by counting rows per order/sku.
4. **OrderItem has no price column** — line revenue must be joined from `products.price` via `sku`.
5. **Product PK is `sku`**, not a synthetic id.
6. **dlt internals excluded** — `_dlt_version`, `_dlt_loads`, `_dlt_pipeline_state`; lineage columns (`_dlt_id`, `_dlt_load_id`) are not modeled as business attributes.
7. **No semantic gaps** — all four stated use cases (order & revenue analytics, customer purchase behavior, product performance, store operations) are covered by existing source columns.
