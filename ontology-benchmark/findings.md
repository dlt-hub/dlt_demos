# Benchmark Findings

## What We Built

A controlled experiment to test whether adding an **ontology** to an LLM's context improves its ability to answer questions about business data — compared to giving it just the raw data, or the data plus a schema.

### Three conditions

| Condition | What the LLM gets |
|---|---|
| A | Table data only (no schema, no ontology) |
| B | Table data + bare CDM schema (column names and types, no rule references) |
| C | Table data + bare CDM schema + ontology.md (all business rules in prose) |

### Two experiments

**Experiment 1: SaaS churn** — a fictional SaaS company with proprietary business rules the LLM cannot know from training data. 7 rules deliberately designed to contradict LLM intuitions (e.g. "at-risk" requires BOTH no login for 14 days AND no API calls for 7 days — not OR; a 45-second session doesn't count; legacy seats excluded entirely; enterprise plans have a LONGER window, not shorter).

**Experiment 2: OpenFDA drugs** — public FDA adverse event data. Domain is well-known to LLMs from training. Some questions target genuine pipeline-specific artifacts (COALESCE logic, LABEL_QUERY_ALIAS, inclusion filter).

---

## Scores

### SaaS churn (10 questions)

> ✅ correct · ⚠️ right answer, wrong/incomplete reasoning · ❌ wrong answer

| Question | A | B | C | Notes |
|---|---|---|---|---|
| sq01 — What makes a seat at-risk? | ❌ | ❌ | ✅ | A/B: "logic lives in the pipeline, can't determine thresholds" |
| sq02 — How many seats at-risk? | ✅ | ✅ | ✅ | Readable from data directly |
| sq03 — Does 45-second login count? | ✅ | ✅ | ✅ | `is_valid_login=False` visible in data |
| sq04 — 55% at-risk seats = churned? | ⚠️ | ⚠️ | ✅ | A/B say "no" but reason from `status=active`, not the 60% threshold |
| sq05 — Above threshold 2 weeks = churned? | ⚠️ | ⚠️ | ✅ | A/B say "no" but reason from `status=active`, not the 3-week rule |
| sq06 — Legacy seats in churn report? | ⚠️ | ⚠️ | ✅ | A/B say "probably not" (hedged inference); C: definitively excluded by rule |
| sq07 — ENT_ANNUAL_V2 at-risk window? | ❌ | ❌ | ✅ | A/B: "can't determine from data"; C: 21-day window |
| sq08 — Resubscribe after 45 days = ? | ❌ | ❌ | ✅ | A/B say "recovered"; correct is "new" (>30 days = new customer) |
| sq09 — Admin seats affect churn score? | ✅ | ✅ | ✅ | NULL visible in data |
| sq10 — acc_008: 3 legacy + 2 standard at-risk = churned? | ❌ | ❌ | ✅ | A/B confused by account mapping; C correctly excludes legacy from denominator |

**SaaS: A = 3/10, B = 3/10, C = 10/10** (⚠️ counted as wrong — right answer for the wrong reason is unreliable) — [full responses](responses.md#saas-churn)

#### Short answers — SaaS churn

| Question | A answered | B answered | C answered |
|---|---|---|---|
| sq01 — What makes a seat at-risk? | Sees `is_at_risk` flag and some null patterns, but says "logic lives in the pipeline, can't determine thresholds" | Same as A — observes plan/role patterns, says "business logic not in schema" | **Both** conditions must hold: no valid login (>120s) in 14 days (21 for ENT), **AND** no API call in 7 days |
| sq02 — How many at-risk? | 8 seats | 8 seats | 8 seats |
| sq03 — Does 45-second login count? | No — infers from `is_valid_login=False` in the data | No — same data inference | No — ontology explicitly states sessions ≤120s are ignored |
| sq04 — 55% at-risk = churned? ⚠️ | **No** (correct) — but reasons only that `at-risk ≠ churned`, unaware 60% threshold exists. Would also say "no" to 65%, getting that wrong | **No** (correct) — same reasoning | No — **55% < 60% threshold**, first condition not met |
| sq05 — Above threshold 2 weeks = churned? ⚠️ | **No** (correct) — reasons from `status=active`, no knowledge of 3-week rule. Ask about 4 weeks and it would still say no | **No** (correct) — same; calls it a "leading indicator" | No — 66.7% clears 60%, but **2 weeks < 3 consecutive weeks required** |
| sq06 — Legacy seats in churn report? ⚠️ | **No** (correct direction) — infers from `<NA>` values; hedges with "recommend excluding" | Same hedge | Definitively no — **explicitly excluded by rule**, don't count toward denominator at all |
| sq07 — ENT_ANNUAL_V2 inactivity window? | "Cannot determine — no at-risk ENT example in data" | Same — "not derivable from schema" | **21 days** (vs. 14 for other plans), same 7-day API rule applies |
| sq08 — Resubscribe 45 days later = ? | `recovered` — sees acc_007 in data and infers reactivation = recovered | `recovered` — same inference, "gap length doesn't change classification" | `new` — **>30 days since churn → new customer**, not recovered |
| sq09 — Admin seats affect churn score? | No — infers from `is_at_risk=<NA>` for admins in data | No — same data inference | No — **explicitly excluded** from at-risk calculation and churn denominator |
| sq10 — acc_008: 3 legacy + 2 standard at-risk = churned? | Confused — can't match account to seats, redirects to acc_007 | Same confusion | Not yet confirmed — correctly excludes legacy seats (denominator = 2), 2/2 = 100% > 60%, but no 3-week duration evidence |

---

### OpenFDA (10 questions)

| Question | A | B | C | Notes |
|---|---|---|---|---|
| fq01 — Ozempic serious events | ✅ | ✅ | ✅ | Training knowledge |
| fq02 — What is "serious"? | ✅ | ✅ | ✅ | Training knowledge |
| fq03 — Why generic_name = ASPIRIN? | ✅ | ✅ | ✅ | A/B guessed plausibly; C cited LABEL_QUERY_ALIAS exactly |
| fq04 — Tylenol indications | ❌ | ✅ | ✅ | A didn't flag IV formulation issue |
| fq05 — Aspirin warnings | ✅ | ✅ | ✅ | Data readable |
| fq06 — Botox reported names | ✅ | ✅ | ✅ | Data readable |
| fq07 — Why ENBREL not in name variants? | ✅ | ✅ | ✅ | A/B gave co-medication reasoning; C cited inclusion filter rule |
| fq08 — Which field determines warnings source? | ❌ | ❌ | ✅ | A/B: "no such field"; C: COALESCE logic |
| fq09 — Which drugs have warnings? | ✅ | ✅ | ✅ | Data readable |
| fq10 — Why IV indications for acetaminophen? | ✅ | ✅ | ✅ | A/B guessed correctly; C cited pipeline reason |

**OpenFDA: A = 8/10, B = 9/10, C = 10/10** — [full responses](responses.md#openfda-drugs)

#### Short answers — OpenFDA

| Question | A answered | B answered | C answered |
|---|---|---|---|
| fq01 — Ozempic serious events | 5,186 | 5,186 | 5,186 |
| fq02 — What is "serious"? | FDA FAERS definition from training (death, hospitalization, etc.) — notes "not in schema" | Same — correct but hedged | Correct + explicitly flags that "serious ≠ severe" using ontology definition |
| fq03 — Why generic_name = ASPIRIN? | FDA labeling convention, genericized trademark in US — plausible training guess | Same reasoning | Cites LABEL_QUERY_ALIAS: OpenFDA doesn't index by IUPAC name, pipeline queries "aspirin" |
| fq04 — Tylenol indications | Lists pain/fever from data, misses IV formulation context entirely | Lists same but notes "based on injectable formulation" | Correct + flags this as a documented data gap — OTC label not captured |
| fq05 — Aspirin warnings | Bleeding, hepatic/renal, dipyridamole — readable from data | Same | Same + notes LABEL_QUERY_ALIAS context |
| fq06 — Botox reported names | Lists all 107 variants | Lists variants | Lists variants + explains inclusion filter rule |
| fq07 — ENBREL in reports but not name variants? | Co-medication on multi-drug report, not a canonical drug — correct | Same reasoning | Cites inclusion filter: ENBREL fails "contains semaglutide" AND brand-name allowlist |
| fq08 — Which field determines warnings source? | "No such field in schema" | "No such field in schema" | `COALESCE(warnings_and_cautions, warnings)` — branching is data-driven, not by drug identity |
| fq09 — Which drugs have warnings? | All 5 | All 5 | All 5 + explains Rx (warnings_and_cautions) vs OTC (warnings) sourcing |
| fq10 — Why IV indications for acetaminophen? | Pipeline artifact — one label selected from many, IV formulation picked | Same | "First record returned by OpenFDA wins" — specifically Caldolor/Ofirmev; documented semantic gap |

---

## Key Findings

### Finding 1: In an unknown domain, ontology is the difference between 30% and 100%

For SaaS churn, condition A and B both score 3/10. The schema alone (B) adds nothing over raw data. The LLM can observe patterns in the data (it can see `is_at_risk = NULL` for legacy seats) but cannot explain or correctly apply the rules behind them without the ontology.

Only condition C gets the rule-dependent questions right — because those rules genuinely don't exist anywhere else.

### Finding 2: Schema alone almost never helps

B scored the same as A on SaaS (3/10) and only 1 point better on OpenFDA (9 vs 8). Column names and types tell the LLM what exists, but not what it means or how to interpret it. The ontology's prose is what carries the logic.

### Finding 3: A right answer for the wrong reason is a reliability risk, not a pass

On sq04, sq05, and sq06, conditions A and B gave the correct surface answer ("no, not churned" / "probably not") — but for the wrong reason. They reasoned from `status=active` or from observing null patterns, with no knowledge of the actual rules.

This is more dangerous than a wrong answer. If you asked "is an account at 63% at-risk for 2 weeks churned?" — A and B would still say no, because they'd apply the same `at-risk ≠ churned` logic. They'd be wrong. If you asked "should a seat that's been inactive for 16 days on ENT_ANNUAL_V2 be at-risk?" — A and B would likely say yes (14-day intuition), missing the 21-day ENT window. The apparent correctness on nearby questions gives false confidence about their reliability on edge cases.

Condition C's answers are grounded in the actual rules, so they generalize correctly to edge cases. A and B's answers are accidents of the specific question phrasing.

### Finding 4: When condition A answers correctly in OpenFDA, it's using training knowledge, not your data

Condition A has no schema and no ontology. When it gets FDA questions right, it isn't reading your data — it's reciting what it learned during training. That's dangerous: if your data diverged from public knowledge (different counts, pipeline-specific artifacts, custom definitions), condition A would give the training-data answer and sound confident doing it.

Condition C is the only one grounded in your actual data and rules. The correctness is traceable.

### Finding 5: Even in well-known domains, ontologies catch gaps that nothing else does

OpenFDA is a public domain the LLM knows well — yet condition A failed on fq04 (IV formulation issue) and fq08 (COALESCE branching). These are genuine pipeline-specific modeling decisions that can't be inferred from training data or column names. The ontology is the only place they live.

### Finding 6: The previous experiment (experiment-2) got 10/10 for both conditions — for the wrong reason

In the first run of this benchmark (using only OpenFDA data), both A and B scored 10/10. We initially attributed this to medical domain knowledge. The real explanation: the CDM schema was richly annotated with rule references inline (e.g. the FDA statutory definition of "serious" was written into the column note for `serious_event_count`). Condition A was given a clean schema in this second experiment — confirming that when the schema is truly bare, condition A drops to 8/10 and the ontology's value reappears.

---

## Why the Results Make Sense

The value of an ontology is **inversely proportional to how much the LLM already knows about your domain**.

- Public medical data → LLM already knows most of it → small gap
- Proprietary business rules → LLM knows nothing → large gap

The SaaS churn rules were specifically designed to contradict LLM intuitions — "enterprise = stricter" (wrong, ENT gets 21 days not 14), "any login counts" (wrong, needs >120s), "majority at-risk = churned" (wrong, 60% AND 3 weeks). Every question where the intuition fires incorrectly, condition A fails. Every question where the ontology corrects it, condition C succeeds.

---

## What This Means for Data Teams

1. **If you document nothing**: an ontology in LLM context will dramatically improve retrieval accuracy for any proprietary domain.

2. **If your schema is already richly annotated**: the ontology's value is front-loaded into the modeling process itself — the LLM inherits it through the schema. But this is fragile: if someone strips the annotations, you lose the grounding.

3. **Schema alone is not enough**: column names don't carry business rules. `is_at_risk boolean` tells you a field exists. It doesn't tell you it requires 14 days AND 7 days, that sessions under 120 seconds don't count, or that legacy seats aren't even in scope.

4. **Condition A correctness is a trap**: a model that gets the right answer for the wrong reason (training knowledge vs. your data) will fail silently when your data diverges from public knowledge.

---

## Experiment Design Notes

- Model: claude-sonnet-4-6
- 10 questions per experiment × 3 conditions = 60 total API calls
- 15-second sleep between questions to respect rate limits
- SaaS data: synthetic, generated with `generate_data.py`, 8 accounts / 23 seats / 42 activity rows
- OpenFDA data: real, from the experiment-2 warehouse (canonical_drugs CDM)
- Schema for conditions B and C: stripped CDM (`CDM_bare.dbml`) with no rule references in column notes
- Ontology for condition C: `ontology.md` with all business rules embedded in entity descriptions as prose
