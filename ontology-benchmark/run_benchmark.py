"""LLM retrieval benchmark — data only vs schema vs schema+ontology.

Three conditions per question, run across two experiments:
  A: table data only (no schema, no ontology)
  B: table data + bare CDM schema (no rule references)
  C: table data + bare CDM schema + ontology.md

Experiments:
  1. saas_churn  — account_churn_risk CDM (experiment-4)
  2. openfda     — canonical_drugs CDM (experiment-2)

Results saved to benchmark/results.json with null score fields for manual scoring.

Usage:
    uv run python benchmark/run_benchmark.py
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import dlt
import duckdb

MODEL = "claude-sonnet-4-6"

ROOT_E4 = Path(__file__).resolve().parent.parent
ROOT_E2 = ROOT_E4.parent / "experiment 2" / "my-workspace"

RESULTS_FILE = Path(__file__).resolve().parent / "results.json"

# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------

SAAS_QUESTIONS = [
    {"id": "sq01", "question": "What makes a seat 'at-risk' in this dataset?"},
    {"id": "sq02", "question": "How many seats are currently at-risk?"},
    {"id": "sq03", "question": "Does a 45-second login session reset the at-risk clock for a seat?"},
    {"id": "sq04", "question": "An account has 55% of its seats at-risk. Is it churned?"},
    {"id": "sq05", "question": "Account acc_004 has been above the at-risk threshold for 2 weeks. Is it churned?"},
    {"id": "sq06", "question": "Should SMB_MONTHLY_LEGACY seats appear in the weekly churn report?"},
    {"id": "sq07", "question": "When does an ENT_ANNUAL_V2 seat become at-risk due to login inactivity?"},
    {"id": "sq08", "question": "If an account churns and resubscribes 45 days later, how should it be classified?"},
    {"id": "sq09", "question": "Do admin seats affect an account's churn score?"},
    {"id": "sq10", "question": "Account acc_008 has 3 SMB_MONTHLY_LEGACY seats and 2 standard seats, both standard seats at-risk. Is it churned?"},
]

OPENFDA_QUESTIONS = [
    {"id": "fq01", "question": "How many serious adverse events have been reported for Ozempic?"},
    {"id": "fq02", "question": "What is a 'serious' adverse event in this dataset?"},
    {"id": "fq03", "question": "Why does acetylsalicylic acid show generic_name = 'ASPIRIN' in this dataset?"},
    {"id": "fq04", "question": "What are the approved indications for Tylenol?"},
    {"id": "fq05", "question": "What warnings exist for acetylsalicylic acid?"},
    {"id": "fq06", "question": "What names have been used to report Botox in adverse event records?"},
    {"id": "fq07", "question": "Why might a drug like ENBREL appear in semaglutide adverse event reports but not in the name variants table?"},
    {"id": "fq08", "question": "Which field in this dataset determines whether a drug's warnings come from warnings_and_cautions vs warnings?"},
    {"id": "fq09", "question": "Which drugs have label warnings in this dataset, and which do not?"},
    {"id": "fq10", "question": "The approved_indications for acetaminophen describe an IV injection product. Why?"},
]


# ---------------------------------------------------------------------------
# SaaS churn data loader
# ---------------------------------------------------------------------------

def load_saas_data() -> dict[str, str]:
    db_path = ROOT_E4 / ".dlt" / "data" / "dev" / "filesystem_pipeline.duckdb"
    con = duckdb.connect(str(db_path), read_only=True)

    accounts_md = con.execute("""
        SELECT source_id, company, plan, status, account_type, reactivated_at
        FROM account_churn_risk.dim_account
    """).df().to_markdown(index=False)

    seats_md = con.execute("""
        SELECT source_id, account_sk, plan_type, role, is_at_risk
        FROM account_churn_risk.dim_seat
    """).df().to_markdown(index=False)

    activity_md = con.execute("""
        SELECT seat_sk, activity_type, occurred_at, session_duration_seconds, is_valid_login
        FROM account_churn_risk.fact_activity
    """).df().to_markdown(index=False)

    con.close()

    return {
        "dim_account": accounts_md,
        "dim_seat": seats_md,
        "fact_activity": activity_md,
    }


def load_openfda_data() -> dict[str, str]:
    db_path = ROOT_E2 / ".dlt" / "data" / "dev" / "warehouse.duckdb"
    con = duckdb.connect(str(db_path), read_only=True)

    dim_drug_df = con.execute("""
        SELECT canonical_drug_id, generic_name, active_ingredient,
               LEFT(approved_indications, 300) || CASE WHEN LENGTH(approved_indications) > 300 THEN '…' ELSE '' END AS approved_indications,
               LEFT(warnings, 300) || CASE WHEN LENGTH(warnings) > 300 THEN '…' ELSE '' END AS warnings,
               total_event_count, serious_event_count
        FROM canonical_drugs.dim_drug
    """).df()
    dim_drug_md = dim_drug_df.to_markdown(index=False)

    PRIORITY_NAMES = {
        "ozempic", "wegovy", "rybelsus", "tylenol", "paracetamol",
        "apap", "adderall", "aspirin", "bayer aspirin", "botox",
    }
    MAX_PER_DRUG = 50
    variants_df = con.execute("""
        SELECT canonical_drug_id, reported_name
        FROM canonical_drugs.dim_drug_name_variants
    """).df()
    con.close()

    grouped_raw = (
        variants_df.groupby("canonical_drug_id")["reported_name"]
        .apply(lambda s: sorted(s.tolist()))
        .to_dict()
    )
    grouped_compact = {}
    for drug, names in grouped_raw.items():
        priority = [n for n in names if n.lower() in PRIORITY_NAMES]
        others = [n for n in names if n.lower() not in PRIORITY_NAMES]
        selected = priority + others[: MAX_PER_DRUG - len(priority)]
        grouped_compact[drug] = {
            "total_variant_count": len(names),
            "sample_variants": selected,
        }
    variants_json = json.dumps(grouped_compact, indent=2)

    return {
        "dim_drug": dim_drug_md,
        "dim_drug_name_variants": variants_json,
    }


# ---------------------------------------------------------------------------
# System prompt builders
# ---------------------------------------------------------------------------

def build_saas_prompt(data: dict, cdm: str | None, ontology: str | None) -> str:
    parts = ["You are answering questions about a SaaS company's customer data.", ""]
    parts += ["## dim_account", data["dim_account"], ""]
    parts += ["## dim_seat", data["dim_seat"], ""]
    parts += ["## fact_activity", data["fact_activity"], ""]
    if cdm:
        parts += ["## Schema (CDM)", cdm, ""]
    if ontology:
        parts += ["## Ontology (modeling decisions and business rules)", ontology, ""]
    return "\n".join(parts)


def build_openfda_prompt(data: dict, cdm: str | None, ontology: str | None) -> str:
    parts = ["You are answering questions about a drug adverse events dataset.", ""]
    parts += ["## dim_drug (one row per canonical drug)", data["dim_drug"], ""]
    parts += ["## dim_drug_name_variants (reported name variants grouped by canonical drug)", data["dim_drug_name_variants"], ""]
    if cdm:
        parts += ["## Schema (CDM)", cdm, ""]
    if ontology:
        parts += ["## Ontology (modeling decisions and semantic rules)", ontology, ""]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_question(client: anthropic.Anthropic, system: str, question: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    return message.content[0].text


def run_experiment(
    client: anthropic.Anthropic,
    experiment_id: str,
    questions: list[dict],
    prompts: dict[str, str],
    run_at: str,
) -> list[dict]:
    results = []
    conditions = ["a", "b", "c"]

    for q in questions:
        for condition in conditions:
            label = f"  [{experiment_id}] {q['id']} condition {condition.upper()} ..."
            print(label, end="", flush=True)
            resp = run_question(client, prompts[condition], q["question"])
            print(" done")
            results.append({
                "experiment": experiment_id,
                "question_id": q["id"],
                "question": q["question"],
                "condition": condition,
                "model": MODEL,
                "run_at": run_at,
                "response": resp,
                "score": None,
            })
        # Stay within rate limits — sleep between questions
        if q["id"] != questions[-1]["id"]:
            time.sleep(15)

    return results


def main() -> None:
    # Load schema files
    saas_cdm_bare = (ROOT_E4 / ".schema" / "account_churn_risk" / "CDM_bare.dbml").read_text()
    saas_cdm_full = (ROOT_E4 / ".schema" / "account_churn_risk" / "CDM.dbml").read_text()
    saas_ontology = (ROOT_E4 / ".schema" / "account_churn_risk" / "ontology.md").read_text()

    openfda_cdm_bare = (ROOT_E2 / ".schema" / "canonical_drugs" / "CDM_bare.dbml").read_text()
    openfda_cdm_full = (ROOT_E2 / ".schema" / "canonical_drugs" / "CDM.dbml").read_text()
    openfda_ontology = (ROOT_E2 / ".schema" / "canonical_drugs" / "ontology.md").read_text()

    # Load table data
    print("Loading SaaS churn data...")
    saas_data = load_saas_data()
    print("Loading OpenFDA data...")
    openfda_data = load_openfda_data()

    # Build system prompts — 3 conditions per experiment
    saas_prompts = {
        "a": build_saas_prompt(saas_data, cdm=None, ontology=None),
        "b": build_saas_prompt(saas_data, cdm=saas_cdm_bare, ontology=None),
        "c": build_saas_prompt(saas_data, cdm=saas_cdm_bare, ontology=saas_ontology),
    }
    openfda_prompts = {
        "a": build_openfda_prompt(openfda_data, cdm=None, ontology=None),
        "b": build_openfda_prompt(openfda_data, cdm=openfda_cdm_bare, ontology=None),
        "c": build_openfda_prompt(openfda_data, cdm=openfda_cdm_bare, ontology=openfda_ontology),
    }

    client = anthropic.Anthropic(api_key=dlt.secrets["anthropic_api_key"])
    run_at = datetime.now(timezone.utc).isoformat()

    all_results = []

    print("\nRunning SaaS churn experiment...")
    all_results += run_experiment(client, "saas_churn", SAAS_QUESTIONS, saas_prompts, run_at)

    print("\nRunning OpenFDA experiment...")
    all_results += run_experiment(client, "openfda", OPENFDA_QUESTIONS, openfda_prompts, run_at)

    RESULTS_FILE.write_text(json.dumps(all_results, indent=2))
    print(f"\nSaved {len(all_results)} results to {RESULTS_FILE}")
    print(f"  saas_churn: {len(SAAS_QUESTIONS) * 3} results (10 questions × 3 conditions)")
    print(f"  openfda:    {len(OPENFDA_QUESTIONS) * 3} results (10 questions × 3 conditions)")


if __name__ == "__main__":
    main()
