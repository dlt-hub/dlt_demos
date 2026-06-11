"""Get sample_shop schema from the local duckdb pipeline and write as DBML."""
import os

import dlt

pipeline = dlt.attach(pipeline_name="sample_shop_pipeline")
schema = pipeline.default_schema

lines = []
for table_name, table in schema.tables.items():
    lines.append(f'Table "{table_name}" {{')
    for col_name, col in table.get("columns", {}).items():
        attrs = []
        if col.get("primary_key"):
            attrs.append("pk")
        if col.get("nullable") is False:
            attrs.append("not null")
        suffix = f' [{", ".join(attrs)}]' if attrs else ""
        lines.append(f'    "{col_name}" {col.get("data_type", "unknown")}{suffix}')
    lines.append("}")
    lines.append("")

output_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".schema", "retail_sales", "sample_shop_pipeline.dbml",
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    f.write("\n".join(lines))
print(f"Schema written to {output_path}")
print("Tables found:", list(schema.tables.keys()))
