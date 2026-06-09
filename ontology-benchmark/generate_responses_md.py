"""Generate responses.md from results.json — one section per question, A/B/C stacked."""

import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results.json"
OUTPUT = Path(__file__).parent / "responses.md"

results = json.loads(RESULTS.read_text())

from collections import defaultdict
grouped = defaultdict(dict)
questions = {}
for r in results:
    key = (r["experiment"], r["question_id"])
    grouped[key][r["condition"]] = r["response"]
    questions[key] = r["question"]

experiments = ["saas_churn", "openfda"]
exp_labels = {"saas_churn": "SaaS Churn", "openfda": "OpenFDA Drugs"}
condition_labels = {
    "a": "A — data only",
    "b": "B — data + schema",
    "c": "C — data + schema + ontology",
}

lines = ["# Full Responses\n"]

for exp in experiments:
    lines.append(f"## {exp_labels[exp]}\n")
    keys = sorted([k for k in grouped if k[0] == exp], key=lambda k: k[1])
    for key in keys:
        qid = key[1]
        question = questions[key]
        responses = grouped[key]
        lines.append(f"### {qid.upper()} — {question}\n")
        for cond in ["a", "b", "c"]:
            label = condition_labels[cond]
            response = responses.get(cond, "_(no response)_")
            lines.append(f"**{label}**\n")
            lines.append(response.strip())
            lines.append("\n")
        lines.append("---\n")

OUTPUT.write_text("\n".join(lines))
print(f"Written to {OUTPUT}")
