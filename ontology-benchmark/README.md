# Ontology Benchmark

Benchmark code and results from the experiment described in [this blog post](https://dlthub.com/blog/ontology-benchmark).

The experiment tested whether adding an ontology to an LLM's context improves how well it answers questions about business data — across three conditions and two datasets.

## Conditions

| Condition | What the LLM gets |
|---|---|
| A | Table data only |
| B | Table data + `CDM_bare.dbml` |
| C | Table data + `CDM_bare.dbml` + `ontology.md` |

## Results

| Dataset | A | B | C |
|---|---|---|---|
| SaaS churn | 3/10 | 3/10 | 10/10 |
| OpenFDA drugs | 8/10 | 9/10 | 10/10 |

## Files

- `run_benchmark.py` — runs all 60 queries against the three conditions
- `ontology.md` — the SaaS churn ontology used in condition C
- `CDM_bare.dbml` — the bare schema used in conditions B and C (column names and types only, no rule references)
- `responses.md` — full model responses for all 60 questions, organised by question
- `results.json` — raw API responses
- `findings.md` — scored results with notes on each question
- `generate_responses_md.py` — script that generates `responses.md` from `results.json`

## Running the benchmark

You'll need an Anthropic API key and a DuckDB file with the SaaS churn data loaded.

```bash
pip install anthropic duckdb
export ANTHROPIC_API_KEY=your_key_here
python run_benchmark.py
```
