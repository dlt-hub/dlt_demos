# Full Responses

## SaaS Churn

### SQ01 — What makes a seat 'at-risk' in this dataset?

**A — data only**

## What Makes a Seat "At-Risk"?

Based purely on what's observable in the dataset, here's what I can tell you:

### The `is_at_risk` Field

The `is_at_risk` boolean flag in **dim_seat** directly marks seats as at-risk, but the dataset doesn't explicitly define the business logic behind it. However, some patterns are visible:

### Observable Patterns

| Condition | `is_at_risk` Value |
|---|---|
| `SMB_MONTHLY_LEGACY` plan | `<NA>` (not applicable) |
| `ENT_ANNUAL_V2` plan (admin role) | `<NA>` (not applicable) |
| `SMB_MONTHLY` or `PRO_ANNUAL` member seats | `True` or `False` |

### Key Observations

1. **Legacy & Enterprise plans are excluded** — seats on `SMB_MONTHLY_LEGACY` and `ENT_ANNUAL_V2` (admin) plans have `<NA>`, suggesting the at-risk concept **doesn't apply** to those plan types
2. **Only member-role seats on active plans** are evaluated for at-risk status
3. The dataset alone **doesn't reveal the exact criteria** (e.g., inactivity thresholds, login frequency) — that logic likely lives in the pipeline that populates this field

### What I'd Need to Determine the Logic
- A definition table or business rules document
- Joining `dim_seat` with `fact_activity` to correlate at-risk flags with login recency/frequency

Would you like me to attempt that activity-based analysis to **infer** what might be driving the at-risk classification?


**B — data + schema**

## What Makes a Seat "At-Risk"?

Based purely on what's observable in this dataset, here's what I can tell you:

### The `is_at_risk` Flag
The `is_at_risk` boolean column in **dim_seat** is the direct indicator — but its definition isn't explicitly documented in the schema. I can only infer patterns from the data.

---

### Observable Patterns

| Observation | Detail |
|---|---|
| **Only applies to certain plan types** | `is_at_risk = True` appears **only on `SMB_MONTHLY` and `PRO_ANNUAL`** seats — never on `SMB_MONTHLY_LEGACY` or `ENT_ANNUAL_V2` |
| **Legacy & Enterprise seats are null** | All `SMB_MONTHLY_LEGACY` and `ENT_ANNUAL_V2` seats show `<NA>` — suggesting the risk flag **isn't calculated** for those plans |
| **Admin seats are excluded** | Both admin seats (`seat_002`, `seat_017`) have `<NA>` — the flag appears to apply to **member roles only** |
| **Clustering by account** | At-risk seats tend to cluster within the same account (e.g., `acc_005` and `acc_004` each have 2 at-risk seats) |

---

### ⚠️ Important Caveat
The **business logic** driving this flag (e.g., inactivity threshold, login recency, session duration) **is not defined in the schema or visible in this dataset**. To know the precise definition, you'd need to look at the **upstream pipeline logic** that populates `dim_seat.is_at_risk`.

Would you like me to check if activity patterns (e.g., login recency or session duration) correlate with at-risk seats?


**C — data + schema + ontology**

## At-Risk Seat Definition

A seat is flagged **`is_at_risk = True`** when **both** of the following conditions are true simultaneously:

### Condition 1 — No valid login in the inactivity window
- **No login** with `session_duration_seconds > 120` within the lookback period
- Sessions of ≤ 120 seconds are **ignored** (treated as if they never happened)
- Lookback window:
  - **14 days** for `SMB_MONTHLY` and `PRO_ANNUAL` seats
  - **21 days** for `ENT_ANNUAL_V2` seats

### Condition 2 — No API call in the last 7 days
- No `api_call` activity recorded within the last **7 days**

> ⚠️ Both conditions must be met — a seat with no logins but recent API calls is **not** at-risk.

---

## Important Exclusions

Certain seats are **never** evaluated for at-risk status, regardless of activity:

| Exclusion | Reason |
|---|---|
| `plan_type = 'SMB_MONTHLY_LEGACY'` | Excluded entirely from churn calculations |
| `role = 'admin'` | Excluded regardless of activity level |

---

## Practical Example from the Data

Looking at **seat_005** and **seat_006** (both `SMB_MONTHLY`, `is_at_risk = True`): they would have no valid login in the past 14 days and no API call in the past 7 days, confirming both thresholds were breached.


---

### SQ02 — How many seats are currently at-risk?

**A — data only**

Based on the `dim_seat` table, counting all seats where `is_at_risk = True`:

| Plan | At-Risk Seats |
|------|--------------|
| SMB_MONTHLY | seat_005, seat_006, seat_019, seat_020 |
| PRO_ANNUAL | seat_010, seat_011, seat_013, seat_014 |

**Total at-risk seats: 8**


**B — data + schema**

Looking at the **dim_seat** table, I'll count the seats where `is_at_risk = True`:

| Seat ID  | Account SK           | Plan Type   |
|----------|----------------------|-------------|
| seat_005 | 8097184010347759120  | SMB_MONTHLY |
| seat_006 | 8097184010347759120  | SMB_MONTHLY |
| seat_010 | 5524556371472755810  | PRO_ANNUAL  |
| seat_011 | 5524556371472755810  | PRO_ANNUAL  |
| seat_013 | 1306990129983601653  | PRO_ANNUAL  |
| seat_014 | 1306990129983601653  | PRO_ANNUAL  |
| seat_019 | 8287331769356759010  | SMB_MONTHLY |
| seat_020 | 8287331769356759010  | SMB_MONTHLY |

**There are 8 at-risk seats** across 4 accounts, split between SMB_MONTHLY (4 seats) and PRO_ANNUAL (4 seats) plans.

> ⚠️ Note: Seats with `<NA>` for `is_at_risk` (typically legacy plan types like SMB_MONTHLY_LEGACY and ENT_ANNUAL_V2 admin/member roles) were excluded as they have no risk flag assigned.


**C — data + schema + ontology**

## At-Risk Seat Analysis

Based on the ontology rules, a seat is **at-risk** when:
- **No valid login** in the last 14 days (21 days for `ENT_ANNUAL_V2`) — where valid = `session_duration_seconds > 120`
- **AND no API call** in the last 7 days
- Excluding `SMB_MONTHLY_LEGACY` seats and `admin` role seats

---

### Reference Date
Using the most recent activity date in the data: **2026-05-25**

- Login lookback (standard): ≥ 2026-05-11
- Login lookback (ENT_ANNUAL_V2): ≥ 2026-05-04
- API call lookback: ≥ 2026-05-18

---

### Step 1 — Exclude ineligible seats

Removing from consideration:
- `SMB_MONTHLY_LEGACY` seats: seat_003, seat_004, seat_021, seat_022, seat_023
- `admin` role seats: seat_002, seat_017

**Remaining eligible seats:** seat_001, seat_005, seat_006, seat_007, seat_008, seat_009, seat_010, seat_011, seat_012, seat_013, seat_014, seat_015, seat_016, seat_018, seat_019, seat_020

---

### Step 2 — Check each eligible seat

I need to join seats → their `seat_sk` → activity. *(The seat_sk ↔ source_id mapping isn't explicitly shown, but `is_at_risk` is already derived in `dim_seat`.)*

Using the **`is_at_risk`** flag already present in `dim_seat` for eligible seats:

| Seat | Plan Type | Role | is_at_risk |
|---|---|---|---|
| seat_001 | SMB_MONTHLY | member | False |
| seat_005 | SMB_MONTHLY | member | **True** |
| seat_006 | SMB_MONTHLY | member | **True** |
| seat_007 | SMB_MONTHLY | member | False |
| seat_008 | SMB_MONTHLY | member | False |
| seat_009 | SMB_MONTHLY | member | False |
| seat_010 | PRO_ANNUAL | member | **True** |
| seat_011 | PRO_ANNUAL | member | **True** |
| seat_012 | PRO_ANNUAL | member | False |
| seat_013 | PRO_ANNUAL | member | **True** |
| seat_014 | PRO_ANNUAL | member | **True** |
| seat_015 | PRO_ANNUAL | member | False |
| seat_016 | ENT_ANNUAL_V2 | member | False |
| seat_018 | SMB_MONTHLY | member | False |
| seat_019 | SMB_MONTHLY | member | **True** |
| seat_020 | SMB_MONTHLY | member | **True** |

---

### Result

> **8 seats are currently at-risk**
> (seat_005, seat_006, seat_010, seat_011, seat_013, seat_014, seat_019, seat_020)


---

### SQ03 — Does a 45-second login session reset the at-risk clock for a seat?

**A — data only**

## Short Answer: **No**

A 45-second login session **does not** reset the at-risk clock for a seat, based on the data.

---

## Evidence

Looking at the relevant record in `fact_activity`:

| seat_sk | activity_type | occurred_at | session_duration_seconds | is_valid_login |
|---|---|---|---|---|
| 5836522797845583808 | login | 2026-05-25 | **45** | **False** |

The key field is **`is_valid_login = False`** — this 45-second session was explicitly flagged as an **invalid login**.

Compare it to the same seat's other login:

| seat_sk | activity_type | occurred_at | session_duration_seconds | is_valid_login |
|---|---|---|---|---|
| 5836522797845583808 | login | 2026-05-06 | 500 | **True** |

---

## Interpretation

The data suggests the system uses `is_valid_login` as the gate for resetting at-risk status. A very short session (45 seconds) results in `is_valid_login = False`, meaning:

- It **won't count** as meaningful engagement
- It **won't reset** the at-risk clock
- The seat remains at risk despite technically having a login event recorded

> A minimum session duration threshold likely exists (somewhere **above 45 seconds**) before a login is considered valid engagement.


**B — data + schema**

## Short Answer: **No** — a 45-second login does not reset the at-risk clock.

---

### What the Data Shows

Looking at the specific event in `fact_activity`:

| seat_sk | activity_type | occurred_at | session_duration_seconds | is_valid_login |
|---|---|---|---|---|
| 5836522797845583808 | login | 2026-05-25 | **45** | **False** |

The key field is **`is_valid_login = False`**.

---

### Why It Doesn't Count

```
is_valid_login = False  →  the session is not recognized as a genuine engagement
```

The `is_valid_login` flag is precisely the mechanism that distinguishes **meaningful activity** from noise like:
- Bot probes / automated pings
- Timed-out or immediately-abandoned sessions
- Failed authentication attempts that technically "completed"

A 45-second session that resolves to `is_valid_login = False` would be **excluded** from any at-risk reset logic that filters on `WHERE is_valid_login = True`.

---

### Contrast With Valid Sessions

The **same seat** (`5836522797845583808`) has a legitimate prior login:

| occurred_at | session_duration_seconds | is_valid_login |
|---|---|---|
| 2026-05-06 | 500 | **True** |

That earlier session *would* count. The 45-second one on May 25 does not override or reset anything — it is effectively noise in the activity log.

---

### Bottom Line

> The `is_valid_login` flag acts as the **quality gate**. A 45-second session that fails it is discarded from engagement calculations, so the seat's at-risk status remains unchanged.


**C — data + schema + ontology**

**No, a 45-second login session does not reset the at-risk clock.**

According to the business rules in the ontology:

> A login only counts as valid if `session_duration_seconds > 120`. Sessions of 120 seconds or less are ignored when computing login recency.

At 45 seconds, that session falls well below the 120-second threshold, so it is treated as **invalid** and excluded from the at-risk calculation entirely.

---

You can see a concrete example of this in the data. `fact_activity` contains this row:

| seat_sk | activity_type | occurred_at | session_duration_seconds | is_valid_login |
|---|---|---|---|---|
| 5836522797845583808 | login | 2026-05-25 | 45 | **False** |

The `is_valid_login = False` flag confirms it. That seat's last *valid* login is actually the earlier entry on **2026-05-06** (500 seconds), so the 45-second attempt on May 25th provides no protection against being flagged as at-risk.


---

### SQ04 — An account has 55% of its seats at-risk. Is it churned?

**A — data only**

## Not Necessarily — At-Risk ≠ Churned

Based on the data available, **having 55% of seats flagged as `is_at_risk = True` does not mean the account has churned.** Here's why:

### What the Data Shows
- `is_at_risk` is a **predictive/warning signal** on `dim_seat`, indicating seats that *may* churn
- **Churn status** would be reflected in `dim_account` via:
  - `status` (e.g., `active` vs. cancelled/churned)
  - `account_type`
  - `reactivated_at` (implies a prior churn)

### The Account is Still Active Until `status` Changes
An account with 55% at-risk seats could be:
| State | Meaning |
|---|---|
| ⚠️ **High churn risk** | Needs immediate intervention |
| ✅ **Still active** | Paying, not yet churned |
| ❌ **Churned** | Only if `status ≠ active` |

### Bottom Line
> **At-risk = a churn *warning*. Churned = a confirmed churn *outcome*.**

The account is a strong candidate for proactive outreach, but you'd need to confirm `status = churned/cancelled` in `dim_account` before classifying it as churned.


**B — data + schema**

## Not Necessarily — 55% At-Risk ≠ Churned

**"At-risk" and "churned" are distinct states** in this data model.

### What the data tells us:
- **`is_at_risk`** (on `dim_seat`) flags individual seats showing warning signals — it's a **leading indicator**
- **`status`** (on `dim_account`) is the authoritative field for churn — a churned account would show `status = 'churned'` (or similar inactive status)

### Current account statuses in the data:
| Status | Count |
|--------|-------|
| `active` | 8 |
| `churned` | 0 |

**All accounts are currently `active`**, regardless of their seat-level risk distribution.

---

### The nuanced answer:

| Condition | Meaning |
|-----------|---------|
| 55% seats `is_at_risk = True` | ⚠️ **High churn risk signal** — warrants urgent attention |
| `dim_account.status = 'active'` | ✅ **Not yet churned** |
| `account_type = 'recovered'` | Historical churn + return is possible |

### Bottom line:
> An account with 55% at-risk seats is a **serious churn candidate**, but it has **not churned yet**. Churn is only confirmed when `dim_account.status` reflects an inactive/churned state.


**C — data + schema + ontology**

**No, it is not churned.**

According to the ontology's churn definition, an account is marked as **churned** only when **both** of the following conditions are met:

1. **≥ 60% of its paid seats are at-risk** (excluding `SMB_MONTHLY_LEGACY` and `admin` seats)
2. That threshold has been sustained for **3 consecutive weeks**

At **55% of seats at-risk**, the account **fails the first condition** — it hasn't crossed the 60% threshold. So regardless of how long that level has persisted, it would **not** be classified as churned.


---

### SQ05 — Account acc_004 has been above the at-risk threshold for 2 weeks. Is it churned?

**A — data only**

## Account acc_004 Status

**No, acc_004 (Delta Co) is not churned** — it is still **active**.

However, the at-risk signal is concerning. Here's what the data shows:

### Account Overview
| Field | Value |
|---|---|
| **Company** | Delta Co |
| **Plan** | PRO_ANNUAL |
| **Status** | Active |
| **Account Type** | Active |

### Seat-Level Risk (acc_004's seats)
| Seat | Role | At Risk |
|---|---|---|
| seat_010 | member | ✅ Yes |
| seat_011 | member | ✅ Yes |
| seat_012 | member | ❌ No |

**2 out of 3 seats (67%)** are flagged as at-risk.

---

### Key Takeaway
While acc_004 has **not churned**, the combination of:
- A majority of seats flagged at-risk
- 2+ weeks above the threshold

...makes this account a **high-priority retention target**. Given it's on a **PRO_ANNUAL** plan, proactive outreach (CSM check-in, usage review, renewal conversation) would be strongly advisable before the risk compounds further.


**B — data + schema**

## Account acc_004 Status Assessment

**No, acc_004 (Delta Co) has not churned** — but it shows meaningful churn risk signals.

---

### What the Data Shows

| Attribute | Value |
|---|---|
| **Company** | Delta Co |
| **Plan** | PRO_ANNUAL |
| **Status** | active |
| **Account Type** | active |
| **Reactivated** | Never |

**Seats (acc_004 maps to account_sk `5524556371472755810`):**

| Seat | Is At Risk |
|---|---|
| seat_010 | ✅ True |
| seat_011 | ✅ True |
| seat_012 | ❌ False |

**2 out of 3 seats** are flagged as at-risk.

---

### Key Distinction

> ⚠️ **"At risk" ≠ "Churned"**

The data confirms:
- The account **status is still `active`** — no churn event has been recorded
- Being above the at-risk threshold for 2 weeks is a **leading indicator**, not a churn confirmation
- At-risk flags reflect **engagement/usage concerns**, but the account remains a paying customer

---

### Recommendation

Given 2 weeks above threshold on a **PRO_ANNUAL** plan, this warrants **immediate CSM outreach** — annual contracts represent higher ACV and a churn event here would be a significant loss. The window to intervene is likely still open.


**C — data + schema + ontology**

## No, acc_004 (Delta Co) is not yet churned.

### Why not?

The churn rule requires **both** conditions to be met simultaneously:

| Requirement | Threshold | Current Status |
|---|---|---|
| ≥ 60% of paid seats at-risk | 60% | ✅ Met |
| Duration of above-threshold state | **3 consecutive weeks** | ❌ Only 2 weeks |

Both conditions must be satisfied together. Being above the 60% at-risk threshold for only **2 weeks** falls one week short of the required 3-week consecutive period.

---

### At-risk seat breakdown for acc_004

Delta Co is on **PRO_ANNUAL**, so all seats are paid and eligible for at-risk scoring (no `SMB_MONTHLY_LEGACY` or `admin` seats to exclude).

| Seat | Is At-Risk |
|---|---|
| seat_010 | ✅ Yes |
| seat_011 | ✅ Yes |
| seat_012 | ❌ No |

That's **2 out of 3 seats at-risk = 66.7%**, which does exceed the 60% threshold — but the account still needs to sustain that state for **one more consecutive week** before it would be classified as churned.


---

### SQ06 — Should SMB_MONTHLY_LEGACY seats appear in the weekly churn report?

**A — data only**

## SMB_MONTHLY_LEGACY Seats in Weekly Churn Reports

Based on the data, there's a strong case that **SMB_MONTHLY_LEGACY seats should be excluded** from the weekly churn report. Here's why:

---

### Key Observations

| Factor | SMB_MONTHLY | SMB_MONTHLY_LEGACY |
|---|---|---|
| `is_at_risk` populated? | ✅ Yes (True/False) | ❌ No (`<NA>`) |
| Activity in `fact_activity`? | ✅ Yes | ❌ None |
| Seats affected | seat_001–009, etc. | seat_003, seat_004, seat_021, seat_022, seat_023 |

---

### Reasoning

1. **`is_at_risk` is `<NA>`** for all LEGACY seats — the churn risk signal that drives the weekly report is simply **not calculated** for these seats, suggesting they are outside the scoring pipeline.

2. **No activity data** exists for any LEGACY seats in `fact_activity`, making it impossible to assess engagement-based churn risk.

3. The `_LEGACY` suffix strongly implies these are a **deprecated plan type** that likely follows different retention rules or billing cycles.

---

### Recommendation

> ❌ **Exclude SMB_MONTHLY_LEGACY seats** from the standard weekly churn report until `is_at_risk` scoring is implemented for them, or handle them in a **separate legacy churn view**.

Would you like help defining the filter logic or a separate tracking approach for these seats?


**B — data + schema**

## SMB_MONTHLY_LEGACY Seats in the Weekly Churn Report

**Short answer: No** — and the data already reflects this.

---

### What the Data Shows

Looking at `dim_seat`, all `SMB_MONTHLY_LEGACY` seats have `is_at_risk = <NA>` (null), not `True` or `False`:

| seat_id | plan_type | is_at_risk |
|---|---|---|
| seat_003 | SMB_MONTHLY_LEGACY | `<NA>` |
| seat_004 | SMB_MONTHLY_LEGACY | `<NA>` |
| seat_021 | SMB_MONTHLY_LEGACY | `<NA>` |
| seat_022 | SMB_MONTHLY_LEGACY | `<NA>` |
| seat_023 | SMB_MONTHLY_LEGACY | `<NA>` |

The `is_at_risk` field is **not being populated** for this plan type, which suggests the churn risk scoring pipeline either **doesn't cover** or **explicitly excludes** legacy plans.

---

### Recommendation

Exclude `SMB_MONTHLY_LEGACY` seats from the weekly churn report **unless** a deliberate decision is made to include them, because:

1. **`is_at_risk` is null** — no risk signal exists to report on
2. **Legacy plans likely have different churn dynamics** — mixing them with standard plans could skew risk metrics
3. **Reporting on nulls could be misleading** — they'd appear as neither at-risk nor safe

If there is a business need to track churn for legacy seats, the scoring pipeline should be updated to explicitly evaluate and populate `is_at_risk` for `SMB_MONTHLY_LEGACY` before including them.


**C — data + schema + ontology**

No. **`SMB_MONTHLY_LEGACY` seats are explicitly excluded from at-risk calculation entirely** — they do not appear in churn reports and do not count toward account churn scores.

This means:

- They are **not evaluated** for the at-risk flag (`is_at_risk`)
- They are **not counted** in the 60% paid-seat threshold used to determine whether an account is churned
- They have no influence on account-level churn status

This applies regardless of how active or inactive those seats are.


---

### SQ07 — When does an ENT_ANNUAL_V2 seat become at-risk due to login inactivity?

**A — data only**

Based on the data provided, I **cannot determine** the specific inactivity threshold that triggers the `is_at_risk = True` flag for `ENT_ANNUAL_V2` seats.

Here's what the data actually shows:

### ENT_ANNUAL_V2 Seats (acc_006 / Foxtrot Ent)
| seat_id | role | is_at_risk |
|---------|------|------------|
| seat_016 | member | False |
| seat_017 | admin | `<NA>` |

- **Neither seat is marked at-risk**, so there's no at-risk example in this plan tier to reverse-engineer a threshold from.
- Admin seats appear to have `<NA>` for `is_at_risk` across all plan types, suggesting the flag may **not apply to admins** regardless of plan.

### To answer this definitively, you would need:
- The **business logic or rule definition** (e.g., from a dbt model, product spec, or engineering docs) that defines what inactivity period sets `is_at_risk = True`
- Or **more data** showing ENT_ANNUAL_V2 seats that *have* been flagged at-risk alongside their last login dates

Would you like me to analyze the at-risk patterns from other plan types (e.g., SMB_MONTHLY or PRO_ANNUAL) where at-risk examples do exist?


**B — data + schema**

## ENT_ANNUAL_V2 At-Risk Login Inactivity Threshold

Based on the available data, I **cannot determine a specific inactivity threshold** for ENT_ANNUAL_V2 seats becoming at-risk. Here's why:

### What the Data Shows
Looking at the **only ENT_ANNUAL_V2 seats** in `dim_seat`:

| source_id | plan_type     | role   | is_at_risk |
|-----------|---------------|--------|------------|
| seat_016  | ENT_ANNUAL_V2 | member | False      |
| seat_017  | ENT_ANNUAL_V2 | admin  | `<NA>`     |

- **Neither seat is flagged as at-risk**, so there's no at-risk ENT example to reverse-engineer a threshold from
- The `is_at_risk` field for the admin seat (seat_017) is `<NA>`, suggesting **admins may be excluded** from at-risk evaluation entirely
- The schema defines `is_at_risk` as a **boolean on the seat dimension**, but contains **no documented business rule or threshold logic**

### What Would Be Needed to Answer This
- Business rule documentation (e.g., *"flagged after X days without a valid login"*)
- Historical snapshots of `is_at_risk` changes alongside login timestamps
- A transformation or dbt model defining the at-risk logic

### Recommendation
> The at-risk classification rules are **not derivable from the data provided**. You'd need to consult the **pipeline/ETL logic** that populates `is_at_risk` in `dim_seat` to find the exact threshold per plan type.


**C — data + schema + ontology**

Based on the ontology, an **ENT_ANNUAL_V2** seat becomes at-risk due to login inactivity when **both** of the following conditions are true:

1. **No valid login in the last 21 days** — ENT_ANNUAL_V2 uses a 21-day window instead of the standard 14-day window. A login only counts as valid if `session_duration_seconds > 120`; sessions of 120 seconds or less are ignored.
2. **No API call in the last 7 days** — this condition is the same as for all other eligible plan types.

Both conditions must be met simultaneously (AND logic) for the seat to be flagged as at-risk. Additionally, this only applies to seats with `role = 'member'` (or non-admin roles) — admin seats are excluded from at-risk calculation entirely regardless of activity.


---

### SQ08 — If an account churns and resubscribes 45 days later, how should it be classified?

**A — data only**

## Reactivated Account Classification

Based on the data model, this scenario should be classified as a **"recovered" account type**.

### Evidence from the Schema

Looking at `dim_account`, the `account_type` field has (at least) two observed values:

| account_type | Example |
|---|---|
| `active` | Most accounts (acc_001 through acc_006, acc_008) |
| `recovered` | **acc_007 (Golf Tech)** — which also has a non-null `reactivated_at` timestamp |

### Key Indicators for "Recovered" Classification

An account should be flagged as `recovered` when **both** conditions are met:

1. **`account_type = 'recovered'`** — distinguishes it from a standard new or continuous subscription
2. **`reactivated_at` is populated** — timestamps when the resubscription occurred (e.g., Golf Tech reactivated on `2026-05-11`)

### Important Caveat

The data doesn't explicitly define a **minimum gap threshold** for the "recovered" classification. The **45-day gap** you describe *would likely qualify*, but the exact cutoff rule isn't visible in this dataset alone — that business logic would need to be confirmed from the subscription/billing source system.

> In short: churn + resubscribe → `account_type = 'recovered'` with `reactivated_at` set to the resubscription date.


**B — data + schema**

## Account Reactivation Classification

Based on the data model, an account that churns and resubscribes **45 days later** should be classified as a **"recovered"** account type.

### Evidence from the Schema & Data

The `dim_account` table has an **`account_type`** field and a **`reactivated_at`** timestamp, which together capture this exact scenario:

| Field | Churned + Resubscribed Account |
|---|---|
| `account_type` | `"recovered"` |
| `reactivated_at` | *(timestamp of resubscription)* |
| `status` | `"active"` |

### Real Example in the Data

**acc_007 (Golf Tech)** demonstrates this pattern:

```
source_id      : acc_007
company        : Golf Tech
plan           : SMB_MONTHLY
status         : active
account_type   : recovered        ← classified as recovered
reactivated_at : 2026-05-11       ← resubscription date is populated
```

All other active accounts have `account_type = "active"` and `reactivated_at = NaT`, confirming that `"recovered"` is **specifically reserved** for churn-and-resubscribe cases.

### Key Distinction
| Scenario | `account_type` | `reactivated_at` |
|---|---|---|
| Never churned | `active` | null |
| Churned → resubscribed | `recovered` | populated |

> The 45-day gap itself doesn't change the classification — any resubscription after a churn event would be tagged as `"recovered"` regardless of the gap length, as long as `reactivated_at` is populated.


**C — data + schema + ontology**

## Account Classification: Reactivation After 45 Days

Based on the ontology's reactivation rules, this account should be classified as **`'new'`**.

---

### Decision Logic

The ontology defines two reactivation classifications based on the time elapsed between churning and reactivation:

| Condition | Classification |
|---|---|
| `reactivated_at` is null | `'active'` or `'churned'` |
| Reactivated **within 30 days** of churning | `'recovered'` |
| Reactivated **after 30 days** of churning | **`'new'`** |

Since **45 days exceeds the 30-day recovery window**, the account is treated as a net-new customer rather than a returning one.

---

### Why This Distinction Matters

The ontology explicitly calls this out as a **cohort integrity concern**:

> *"Recovered accounts are not the same as new customers."*

- **`'recovered'`** accounts are churned customers who came back quickly — likely retained through win-back efforts, and should **not** inflate new customer counts.
- **`'new'`** accounts (reactivated after 30 days) are treated as **fresh acquisitions** for cohort and growth reporting purposes.

Misclassifying a 45-day reactivation as `'recovered'` would undercount new customers and distort churn/growth metrics.


---

### SQ09 — Do admin seats affect an account's churn score?

**A — data only**

## Admin Seats and Churn Score

Based on the data available, **admin seats are excluded from churn risk calculations**.

Here's what the data shows:

### `is_at_risk` Field in `dim_seat`
| Role | `is_at_risk` Values |
|------|-------------------|
| **member** | `True`, `False`, or `<NA>` (Legacy plans) |
| **admin** | Always `<NA>` |

Specifically, the two admin seats in the data:
- **seat_002** (acc: `3515910092184876369`, SMB_MONTHLY) → `is_at_risk = <NA>`
- **seat_017** (acc: `520687226136787178`, ENT_ANNUAL_V2) → `is_at_risk = <NA>`

### Interpretation
- The `<NA>` value for admin seats appears **intentional and consistent** — admins are never flagged as at-risk, unlike member seats which can be `True` or `False`.
- This suggests the churn scoring logic **only evaluates member seats**, likely because admins have inherently different usage patterns (account management vs. product usage).

### Caveat
The data doesn't include an explicit churn score column, so this is inferred from the `is_at_risk` flag. If churn scoring uses a separate model not reflected here, the answer could differ.


**B — data + schema**

## Admin Seats & Churn Score

Based on the data model and available data, **admin seats are excluded from churn risk scoring**. Here's the evidence:

### Schema Design
The `is_at_risk` flag lives on **`dim_seat`**, meaning risk is assessed **at the seat level**, not the account level. An account's churn exposure is effectively the **aggregate of its at-risk member seats**.

### Data Pattern
Looking at `dim_seat`, admin seats consistently have **`is_at_risk = <NA>`** (null):

| seat_id | role | is_at_risk |
|---|---|---|
| seat_002 | admin | `<NA>` |
| seat_017 | admin | `<NA>` |

Meanwhile, **member seats** have explicit `True` / `False` values.

### Interpretation
| Seat Role | is_at_risk Populated? | Contributes to Churn Score? |
|---|---|---|
| `member` | ✅ Yes | ✅ Yes |
| `admin` | ❌ Null | ❌ No |

### Likely Rationale
Admin seats typically represent **owners or billing contacts** who are structurally tied to the account — their absence or inactivity is less predictive of churn than that of regular users. The scoring logic appears intentionally scoped to **member engagement**.

---

**Bottom line:** Admin seats do not appear to factor into churn risk scoring. If you want to incorporate admin activity, the `is_at_risk` logic in `dim_seat` would need to be extended to cover the `admin` role.


**C — data + schema + ontology**

No. **Admin seats are excluded from at-risk calculations entirely**, regardless of their activity level.

This means they:
- Are **not evaluated** for at-risk status
- **Do not count** toward the 60% at-risk seat threshold used to determine account churn status
- Have no influence on an account's churn score

Only **member** (and viewer) seats on paid, non-legacy plans (`SMB_MONTHLY`, `PRO_ANNUAL`, `ENT_ANNUAL_V2`) are considered when scoring an account for churn risk.


---

### SQ10 — Account acc_008 has 3 SMB_MONTHLY_LEGACY seats and 2 standard seats, both standard seats at-risk. Is it churned?

**A — data only**

## Analysis of Account acc_008

Let me check the data carefully.

### Account acc_008 Details
From `dim_account`:
- **Company:** Hotel SaaS
- **Plan:** SMB_MONTHLY
- **Status:** active
- **Account type:** active

### Seats for acc_008

First, I need to identify acc_008's `account_sk`. Looking at `dim_seat`, I need to match accounts to their SKs — but **acc_008 (Hotel SaaS)** maps to account_sk **`8885627468594434478`**, which has only:

| seat_id | plan_type | role | is_at_risk |
|---------|-----------|------|------------|
| seat_018 | SMB_MONTHLY | member | False |

That's **1 seat**, not the 5 seats described in your question.

---

### ⚠️ The Premise Doesn't Match the Data

The scenario you described — *3 SMB_MONTHLY_LEGACY seats + 2 standard at-risk seats* — **does not reflect acc_008 in the dataset**. That profile more closely resembles **acc_007 (Golf Tech)**, which has:
- 3 `SMB_MONTHLY_LEGACY` seats (seat_021, 022, 023)
- 2 `SMB_MONTHLY` at-risk seats (seat_019, seat_020)

### acc_008 per the Data
- **1 seat**, not at risk
- Account status: **active**
- **Not churned** based on available data

Could you double-check the account ID? It's possible you meant **acc_007**.


**B — data + schema**

## Checking the Data

Let me look up **acc_008 (Hotel SaaS)** in the tables.

### dim_account
| source_id | company | plan | status | account_type |
|---|---|---|---|---|
| acc_008 | Hotel SaaS | SMB_MONTHLY | **active** | active |

### dim_seat — finding acc_008's account_sk

Looking at dim_seat, I need to match seats to acc_008. Based on the data provided, **acc_008's seats are not visible in the dim_seat table** — there are no seats shown belonging to Hotel SaaS's account_sk (`8885627468594434478` maps to seat_018 only, which is 1 SMB_MONTHLY seat).

---

## ⚠️ I Cannot Confirm the Premise

The seat composition you've described — **3 SMB_MONTHLY_LEGACY seats + 2 standard at-risk seats** — **does not match what's in the provided data** for acc_008. The data shows only **seat_018** (1 SMB_MONTHLY seat, `is_at_risk = False`) linked to acc_008's account_sk.

As for churn status: **acc_008 is marked `active`** in dim_account, so it is **not churned** per the current data.

If you're working from a different or more complete dataset than what's shown here, could you clarify the source? I want to make sure I'm not reasoning from data I don't actually have.


**C — data + schema + ontology**

## Analysis for Account acc_008 (Hotel SaaS)

### Step 1: Identify the seats

Looking at `dim_seat` for `account_sk` matching acc_008 (sk: `8287331769356759010`):

| Seat | Plan Type | Role | is_at_risk |
|---|---|---|---|
| seat_019 | SMB_MONTHLY | member | **True** |
| seat_020 | SMB_MONTHLY | member | **True** |
| seat_021 | SMB_MONTHLY_LEGACY | member | \<NA\> |
| seat_022 | SMB_MONTHLY_LEGACY | member | \<NA\> |
| seat_023 | SMB_MONTHLY_LEGACY | member | \<NA\> |

---

### Step 2: Apply exclusion rules

Per the ontology:
- **`SMB_MONTHLY_LEGACY` seats are excluded** from churn calculations entirely
- **`admin` seats are excluded** (none here anyway)

This leaves only the **2 standard SMB_MONTHLY seats** (seat_019, seat_020) as the **paid seat pool** for churn scoring.

---

### Step 3: Apply the churn threshold

> An account is churned when **≥ 60% of paid seats** are at-risk for **3 consecutive weeks**

| Metric | Value |
|---|---|
| Eligible paid seats | 2 |
| At-risk seats | 2 |
| At-risk % | **100%** ✅ (exceeds 60%) |

The **60% threshold is met**, but churn requires this condition to hold for **3 consecutive weeks** — that is a duration check, not just a point-in-time snapshot.

---

### Conclusion

> **Not definitively churned yet** — based on the available data.

The at-risk ratio (100%) clears the 60% threshold, but **we have no temporal evidence** that both seats have been continuously at-risk for 3 consecutive weeks. The `is_at_risk` flag reflects the current state only. Without a weekly history of at-risk status, the 3-week duration requirement **cannot be confirmed**, and churn status should not be set to churned.


---

## OpenFDA Drugs

### FQ01 — How many serious adverse events have been reported for Ozempic?

**A — data only**

Based on the dataset, **Ozempic** is a brand name for **semaglutide**. The total number of serious adverse events reported for semaglutide (including Ozempic and other name variants like Wegovy and Rybelsus) is:

## 5,186 serious adverse events

This represents approximately **78.4%** of the total 6,618 adverse events reported for semaglutide being classified as serious.


**B — data + schema**

Based on the dataset, **semaglutide** (which includes Ozempic as one of its brand name variants) has had **5,186 serious adverse events** reported.

> **Note:** The data is aggregated at the canonical drug level (semaglutide), meaning this figure encompasses all reported name variants for the drug, including **OZEMPIC**, **WEGOVY**, **RYBELSUS**, and others — not just those explicitly reported under the "Ozempic" brand name.


**C — data + schema + ontology**

## Serious Adverse Events for Ozempic (Semaglutide)

**5,186 serious adverse events** have been reported for Ozempic.

### How this resolves:
- **"Ozempic"** is a brand name that maps to the canonical drug **semaglutide** (`canonical_drug_id = 'semaglutide'`)
- The `serious_event_count` field reflects FDA's **statutory definition** of a serious adverse event — not simply a "severe" reaction. An event is counted as serious if it results in:
  - Death
  - Inpatient hospitalization
  - Life-threatening reaction
  - Persistent disability
  - Congenital anomaly
  - Required medical intervention to prevent permanent impairment

### Summary stats for Semaglutide:
| Metric | Count |
|---|---|
| Total adverse events | 6,618 |
| **Serious adverse events** | **5,186** |
| Serious event rate | ~78.4% |

> **Note:** Total events are capped at 25,000 per drug due to the OpenFDA API hard limit, though semaglutide's total (6,618) is well below that cap.


---

### FQ02 — What is a 'serious' adverse event in this dataset?

**A — data only**

## Definition of a 'Serious' Adverse Event

Based on the dataset structure, there is a **`serious_event_count`** field in the `dim_drug` table that is distinguished from the overall **`total_event_count`**, but the dataset schema provided here **does not explicitly define** what criteria classify an event as "serious."

However, in the context of **FDA adverse event reporting (FAERS)** — which this dataset appears to be derived from — a serious adverse event is typically defined as one that results in any of the following outcomes:

- **Death**
- **Life-threatening condition**
- **Hospitalization** (initial or prolonged)
- **Disability or permanent damage**
- **Congenital anomaly/birth defect**
- **Required intervention** to prevent permanent impairment
- **Other serious important medical events**

### From the Data We Can Observe:
The serious event counts are notably high as a proportion of total events, for example:
- **Aspirin**: 22,945 serious out of 25,000 total (~**91.8%**)
- **Acetaminophen**: 18,994 serious out of 25,000 total (~**76.0%**)

To get the **precise definition used in this specific dataset**, the underlying data documentation or codebook would need to be consulted.


**B — data + schema**

Based on the dataset provided, **the exact definition of "serious" adverse event is not explicitly documented** in the schema or the sample data shown.

However, based on standard FDA/pharmacovigilance conventions (since this appears to be **FDA Adverse Event Reporting System (FAERS)**-style data), a "serious" adverse event typically meets **one or more** of the following criteria:

- ☠️ **Death**
- 🏥 **Hospitalization** (initial or prolonged)
- ⚠️ **Life-threatening** condition
- 🦽 **Disability or permanent damage**
- 👶 **Congenital anomaly/birth defect**
- 🚨 **Required intervention** to prevent permanent impairment

---

### What the dataset *does* tell us:
The `dim_drug` table tracks two counts:
| Field | Description |
|---|---|
| `total_event_count` | All reported adverse events |
| `serious_event_count` | Subset flagged as "serious" |

For example, **acetylsalicylic acid (aspirin)** has **22,945 serious out of 25,000 total** (~91.8%), suggesting a high serious event rate.

---

> To get the precise definition used in *this specific dataset*, you would need to consult the **source pipeline documentation** (`source_pipeline` field) or the originating data source.


**C — data + schema + ontology**

Based on the ontology, a **"serious" adverse event** in this dataset follows the **FDA statutory definition** — it is an adverse event that results in one or more of the following:

- **Death**
- **Inpatient hospitalization**
- **Life-threatening reaction**
- **Persistent disability**
- **Congenital anomaly**
- **Required medical intervention to prevent permanent impairment**

This is captured in the `serious_event_count` field, which counts rows where `serious = 1` in the adverse events data.

---

### ⚠️ Important semantic note

The ontology explicitly flags a known failure mode:

> **"Serious" ≠ "severe," "high severity," or "bad reaction."**

The field uses the **legal FDA definition**, not a clinical severity rating. An event can be medically serious (e.g., a hospitalization for a mild allergic reaction) without being "severe" in colloquial terms, and vice versa. LLMs without this ontology are noted to default to interpreting "serious" as severity — which would be incorrect for this dataset.


---

### FQ03 — Why does acetylsalicylic acid show generic_name = 'ASPIRIN' in this dataset?

**A — data only**

## Why `generic_name = 'ASPIRIN'` for Acetylsalicylic Acid

This is essentially a **data/labeling convention issue** rather than a scientific one. Here are the likely reasons:

### 1. **Common Usage in FDA Labeling**
The FDA and drug manufacturers frequently use **"Aspirin"** as the established name on product labels in the United States, even though the technically precise International Nonproprietary Name (INN) is **acetylsalicylic acid**. The `generic_name` field here likely reflects what appears on the **drug label or package insert**.

### 2. **"Aspirin" is Treated as a Generic Name in the US**
Unlike in some other countries where "Aspirin" remains a **Bayer trademark**, in the **United States** (and several other countries), "aspirin" has become a **genericized trademark** — it lost trademark protection and is now considered a common/generic name for the drug.

### 3. **Dataset Design Choice**
- The `canonical_drug_id` = `acetylsalicylic acid` (the chemically precise name)
- The `generic_name` = `ASPIRIN` (the commonly used label name)
- This split suggests the dataset uses `canonical_drug_id` for **scientific precision** and `generic_name` for **practical/label recognition**

### 4. **Confirmed by Name Variants**
The `dim_drug_name_variants` table supports this — it includes both `"ASPIRIN"` and `"ACETYLSALICYLIC ACID"` as reported variants, showing the dataset recognizes **both names refer to the same drug**.

---

**In short:** "Aspirin" is the de facto generic name used on U.S. drug labels, so it appears in the `generic_name` field, while `acetylsalicylic acid` serves as the more chemically precise canonical identifier.


**B — data + schema**

## Why `generic_name = 'ASPIRIN'` for Acetylsalicylic Acid

This is likely due to how the **source data pipeline populated the `generic_name` field**. Here are the most probable reasons:

### 1. **Brand/Common Name Used Instead of INN**
- "Aspirin" is the most widely recognized common name for acetylsalicylic acid, and many drug databases (including FDA labeling systems) use "ASPIRIN" as the primary label rather than the full chemical name "ACETYLSALICYLIC ACID."
- The pipeline likely pulled `generic_name` from an FDA drug label or structured product labeling (SPL) where the drug is listed under **"ASPIRIN"** as the established name.

### 2. **"Aspirin" is Technically a Generic Name in the US**
- Unlike some countries where "Aspirin" remains a trademarked brand name (e.g., Bayer in Germany), **in the United States "aspirin" is a generic/common name** — not a brand. So populating `generic_name = 'ASPIRIN'` is technically correct in a US regulatory context.

### 3. **`canonical_drug_id` vs. `generic_name` Serve Different Purposes**
| Field | Value | Purpose |
|---|---|---|
| `canonical_drug_id` | `acetylsalicylic acid` | Chemical/INN identity for deduplication |
| `generic_name` | `ASPIRIN` | How the drug appears in source labeling |

The `canonical_drug_id` correctly uses the **INN (International Nonproprietary Name)**, while `generic_name` reflects the **FDA label display name**.

### 4. **Supporting Evidence from `dim_drug_name_variants`**
The name variants table confirms both names are in use — `"ASPIRIN"` and `"ACETYLSALICYLIC ACID"` both appear as `reported_name` variants, meaning the pipeline recognized them as the same drug but chose `ASPIRIN` as the display generic name from the source label.

---

**In short:** It's not an error — "ASPIRIN" is the FDA-recognized generic name in the US, and the `canonical_drug_id = 'acetylsalicylic acid'` preserves the INN for cross-reference and deduplication purposes.


**C — data + schema + ontology**

## Why `generic_name = 'ASPIRIN'` for acetylsalicylic acid

This is a documented pipeline artifact explained in the ontology's **Semantic Gaps** section.

### The core reason: OpenFDA doesn't index by IUPAC name

OpenFDA's drug labels API does not recognize `"acetylsalicylic acid"` as a valid query term — it indexes this drug under `"aspirin"`. So the ingestion pipeline had to query the labels API using `aspirin`, not the canonical drug's IUPAC name.

### What the pipeline does to handle this

A **`LABEL_QUERY_ALIAS`** is applied at ingestion time:

| Ingestion step | Value |
|---|---|
| Labels API query term | `"aspirin"` (what OpenFDA understands) |
| `_drug_query` tag applied to the record | `"acetylsalicylic acid"` (the canonical drug ID) |
| `generic_name` returned by OpenFDA | `"ASPIRIN"` (what the label actually says) |

The alias lets the labels join consistently with the adverse events side (which is also tagged `_drug_query = "acetylsalicylic acid"`), while the `generic_name` field simply reflects whatever OpenFDA returned from the label — which is `ASPIRIN`.

### Why this matters for LLMs

Without this ontology, an LLM might:
- Fail to recognize that `acetylsalicylic acid` and `ASPIRIN` are the **same entity** in this dataset
- Think there's a data quality error rather than an intentional alias
- Incorrectly treat them as two separate drugs when querying

The ontology explicitly documents that `acetylsalicylic acid` → `aspirin` is a **known, intentional mapping** — not a mistake.


---

### FQ04 — What are the approved indications for Tylenol?

**A — data only**

Based on the dataset, **Tylenol (Acetaminophen)** is approved for the following indications:

1. **Management of mild to moderate pain** in adult and pediatric patients **2 years and older**

2. **Management of moderate to severe pain** (with adjunctive opioid analgesics) in adult and pediatric patients **2 years and older**

3. **Reduction of fever** in adult and pediatric patients

> *Note: Tylenol is a brand name variant of the canonical drug **Acetaminophen**, as confirmed in the drug name variants data.*


**B — data + schema**

Based on the dataset, **Tylenol (Acetaminophen)** is approved for the following indications:

1. **Mild to Moderate Pain Management** – For adult and pediatric patients **2 years and older**

2. **Moderate to Severe Pain Management** – Used **adjunctively with opioid analgesics** in adult and pediatric patients 2 years and older

3. **Fever Reduction** – (indicated in the label, though the full text is truncated in the dataset)

> ⚠️ *Note: The indications listed here are based on the **injectable formulation** of Acetaminophen, as referenced in the dataset. Other formulations (e.g., oral tablets like standard Tylenol) may have a broader or slightly different label.*


**C — data + schema + ontology**

## Approved Indications for Tylenol (Acetaminophen)

Based on this dataset, the approved indications for **Tylenol** (canonical drug: **acetaminophen**) are:

1. **Management of mild to moderate pain** in adult and pediatric patients **2 years and older**
2. **Management of moderate to severe pain** with adjunctive opioid analgesics in adult and pediatric patients **2 years and older**
3. **Reduction of fever**

---

### ⚠️ Important Context

The indications above reflect an **Rx/IV injection label** (such as Caldolor or Ofirmev) — **not** the consumer Tylenol OTC product. This is a known data gap in this dataset: OpenFDA returns all label records for a given generic name, and the ingestion pipeline captured an intravenous formulation label rather than the standard over-the-counter Tylenol label.

In practice, **consumer Tylenol** is indicated for:
- Temporary relief of minor aches and pains
- Reduction of fever

But those OTC indications are **not what is stored in this CDM** for acetaminophen.


---

### FQ05 — What warnings exist for acetylsalicylic acid?

**A — data only**

Based on the dataset, the warnings for **acetylsalicylic acid (Aspirin)** include:

1. **Increased Bleeding Risk** – Aspirin and extended-release dipyridamole capsules increases the risk of bleeding.

2. **Hepatic/Renal Insufficiency** – Avoid use in patients with **severe hepatic or renal insufficiency**.

3. **Pre-surgical Interruption** – Interrupt aspirin and extended-release dipyridamole capsules **48 hours before** using intravenous dipyridamole.

> ⚠️ *Note: The warnings text in the dataset appears to be truncated, so there may be additional warnings not fully captured here. Always refer to the full prescribing information for a complete list of warnings and precautions.*


**B — data + schema**

Based on the dataset, the warnings for **acetylsalicylic acid (Aspirin)** include:

1. **Increased Bleeding Risk** – Aspirin and extended-release dipyridamole capsules increases the risk of bleeding.

2. **Hepatic Insufficiency** – Avoid use in patients with severe hepatic insufficiency.

3. **Renal Insufficiency** – Avoid use in patients with severe renal insufficiency.

4. **Pre-procedural Interruption** – Interrupt aspirin and extended-release dipyridamole capsules **48 hours before** using intravenous dipyridamole.

> ⚠️ *Note: The warnings text in the dataset appears to be truncated, so there may be additional warnings not fully captured here.*


**C — data + schema + ontology**

## Warnings for Acetylsalicylic Acid (Aspirin)

Based on the dataset, here are the documented warnings for **acetylsalicylic acid** (canonical drug ID: `acetylsalicylic acid`; generic name in OpenFDA: **ASPIRIN**):

---

### Key Warnings

1. **Increased Bleeding Risk**
   - Aspirin and extended-release dipyridamole capsules increase the risk of bleeding.

2. **Hepatic & Renal Insufficiency**
   - Avoid use in patients with **severe hepatic or renal insufficiency**.

3. **Pre-procedural Interruption**
   - Interrupt aspirin and extended-release dipyridamole capsules **48 hours before** using intravenous dipyridamole (e.g., for cardiac stress testing), due to the risk of compounding antiplatelet effects.

---

### Data Source Note

> The warnings shown here are sourced from the **OpenFDA drug label** associated with the query term `acetylsalicylic acid`. Per the ontology, OpenFDA does not index this drug under its IUPAC name — a `LABEL_QUERY_ALIAS` maps `"acetylsalicylic acid"` → `"aspirin"` at ingestion. The label retrieved reflects a **combination product** (aspirin + extended-release dipyridamole), which is one of the label records OpenFDA returns for this query. Additional warnings may apply to other aspirin formulations not captured in this record.


---

### FQ06 — What names have been used to report Botox in adverse event records?

**A — data only**

Based on the dataset, here are the reported name variants used for **Botulinum Toxin (Botox)** in adverse event records (sample of 107 total variants):

### Brand Names
- **BOTOX** (and variations like "BOTOX INJECTION", "BOTOX INJECTIONS", "BOTOX [BOTULINUM TOXIN TYPE A]")
- **AZZALURE**
- **ANTIPAR**
- **DAXXIFY** (the canonical brand)

### Generic/Scientific Names
- BOTULINUM TOXIN
- BOTULINUM TOXIN TYPE A
- BOTULINUM TOXIN A
- BOTULINUM TOXIN TYPE B
- BOTULINUM TOXIN NOS
- BOTULINIC TOXIN
- BOTULINIUM TOXIN TYPE B

### Misspellings/Variants
- BOLUTLINUM TOXIN TYPE A
- BOTILINUM TOXIN
- BOTOULINUM TOXIN TYPE A NOS
- BOTULINIUM

### Blinded/Study Names
- BLINDED BOTULINUM TOXIN TYPE A - COSMETIC
- BLINDED BOTULINUM TOXIN TYPE A - GENERAL
- BLINDED BOTULINUM TOXIN TYPE A - IPSEN
- BLINDED BOTULINUM TOXIN TYPE A – NON–HSA

### Other Formats
- ANTICHOLINERGICS (ANTICHOLINERGICS) ABOBOTULINUM TOXIN A
- BOTULINUM TOXIN 100 UNITS
- BOTULINUM TOXIN A 100U
- BOTULINUM TOXIN A Q3MONTHS

In total, there are **107 unique name variants** recorded across all adverse event reports.


**B — data + schema**

Based on the **dim_drug_name_variants** data for **botulinum toxin** (the canonical drug for Botox), here are the reported name variants used in adverse event records:

| # | Reported Name |
|---|--------------|
| 1 | BOTOX |
| 2 | (BOTULINUM TOXIN TYPE A |
| 3 | ANTICHOLINERGICS (ANTICHOLINERGICS) ABOBOTULINUM TOXIN A |
| 4 | ANTIPAR (BOTULINUM TOXIN TYPE A) |
| 5 | AZZALURE (BOTULINUM TOXIN TYE A) (BOTULINUM TOXIN TYPE A) |
| 6 | AZZALURE (BOTULINUM TOXIN TYPE 1) (BOTULINUM TOXIN TYPE A) ABOBOTULINU |
| 7 | AZZALURE (BOTULINUM TOXIN TYPE A) (BOTULINUM TOXIN TYPE A) |
| 8 | BLINDED BOTULINUM TOXIN TYPE A - COSMETIC |
| 9 | BLINDED BOTULINUM TOXIN TYPE A - GENERAL |
| 10 | BLINDED BOTULINUM TOXIN TYPE A - IPSEN |
| 11 | BLINDED BOTULINUM TOXIN TYPE A – NON–HSA |
| 12 | BOLUTLINUM TOXIN TYPE A (BOTULINUM TOXIN TYPE A) |
| 13 | BOTILINUM TOXIN (BOTULINUM TOXIN TYPE A) |
| 14 | BOTOULINUM TOXIN TYPE A NOS |
| 15 | BOTOX (BOTULINUM TOXIN TYPE A) |
| 16 | BOTOX (BOTULINUM TOXIN TYPE A) (INJECTION) |
| 17 | BOTOX (BOTULINUM TOXIN TYPE A) INJECTION |
| 18 | BOTOX (BOTULINUM TOXIN TYPE A) POWDER FOR INJECTION |
| 19 | BOTOX (BOTULINUM TOXIN) |
| 20 | BOTOX ALLERGAN BOTULINUM TOXIN TYPE-A |
| 21 | BOTOX INJECTION (BOTULINUM TOXIN TYPE A) |
| 22 | BOTOX INJECTION 100 (BOTULINUM TOXIN TYPE A) |
| 23 | BOTOX INJECTIONS (BOTULINUM TOXIN TYPE A) |
| 24 | BOTOX [BOTULINUM TOXIN TYPE A] |
| 25 | BOTOX(BOTULINUM TOXIN TYPE A) |
| 26 | BOTULINIC TOXIN [BOTULINUM TOXIN TYPE A] |
| 27 | BOTULINIUM (BOTULINUM TOXIN TYPE A) |
| 28 | BOTULINIUM TOXIN TYPE B |
| 29 | BOTULINUM TOXIN |
| 30 | BOTULINUM TOXIN (BOTULINUM TOXIN TYPE A) |
| 31 | BOTULINUM TOXIN 100 UNITS |
| 32 | BOTULINUM TOXIN A |
| 33 | BOTULINUM TOXIN A (BOTULINUM TOXIN TYPE A) |
| 34 | BOTULINUM TOXIN A - ALLERGAN CO. |
| 35 | BOTULINUM TOXIN A 100U |
| 36 | BOTULINUM TOXIN A INJECTION |
| 37 | BOTULINUM TOXIN A Q3MONTHS |
| 38 | BOTULINUM TOXIN INJECTIONS |
| 39 | BOTULINUM TOXIN NOS |
| 40 | BOTULINUM TOXIN TYPE A |
| 41 | BOTULINUM TOXIN TYPE A (BOTOX) |

> **Note:** The dataset shows a total of **107 unique name variants** for botulinum toxin. The above represents the available sample. Common patterns include misspellings (e.g., *BOTILINUM*, *BOLUTLINUM*),


**C — data + schema + ontology**

Based on the `dim_drug_name_variants` table, here are the reported name variants for **Botulinum Toxin (Botox)** found in adverse event records (107 total variants). The sample includes:

### Brand Name Variants
| Reported Name |
|---|
| BOTOX |
| BOTOX (BOTULINUM TOXIN TYPE A) |
| BOTOX INJECTION (BOTULINUM TOXIN TYPE A) |
| BOTOX INJECTIONS (BOTULINUM TOXIN TYPE A) |
| BOTOX [BOTULINUM TOXIN TYPE A ((BACTERIA/CLOSTRIDIUM BOTULINUM))] |
| BOTOX ALLERGAN BOTULINUM TOXIN TYPE-A (NEUROTOXIN) ALLERGAN |

### Generic Name Variants
| Reported Name |
|---|
| BOTULINUM TOXIN |
| BOTULINUM TOXIN TYPE A |
| BOTULINUM TOXIN A |
| BOTULINUM TOXIN A INJECTION |
| BOTULINUM TOXIN TYPE A (BOTOX) |
| BOTULINUM TOXIN 100 UNITS |
| BOTULINUM TOXIN NOS |

### Other Brand Names (non-Botox)
| Reported Name |
|---|
| AZZALURE (BOTULINUM TOXIN TYPE A) |
| ANTIPAR (BOTULINUM TOXIN TYPE A) |

### Blinded/Clinical Trial Variants
| Reported Name |
|---|
| BLINDED BOTULINUM TOXIN TYPE A - COSMETIC |
| BLINDED BOTULINUM TOXIN TYPE A - GENERAL |
| BLINDED BOTULINUM TOXIN TYPE A - IPSEN |

### Misspellings / Typographic Variants
| Reported Name |
|---|
| BOTILINUM TOXIN (BOTULINUM TOXIN TYPE A) |
| BOLUTLINUM TOXIN TYPE A (BOTULINUM TOXIN TYPE A) |
| BOTULINIUM (BOTULINUM TOXIN TYPE A) |
| BOTULINIC TOXIN [BOTULINUM TOXIN TYPE A] |
| BOTOULINUM TOXIN TYPE A NOS |

---

**Key takeaways:**
- All 107 variants resolve to the canonical drug ID **`botulinum toxin`**
- The most common aliases are **BOTOX** (brand) and **BOTULINUM TOXIN TYPE A** (generic)
- Variants include misspellings, blinded clinical trial labels, co-medication strings, and international brand names like **AZZALURE**
- These were captured via the `reported_names_inclusion_filter` rule: names containing "botulinum toxin" **OR** the brand name "botox"


---

### FQ07 — Why might a drug like ENBREL appear in semaglutide adverse event reports but not in the name variants table?

**A — data only**

## Why ENBREL Might Appear in Semaglutide Adverse Event Reports But Not in the Name Variants Table

This is a great data quality and schema design question. Here are the most likely explanations:

---

### 1. **ENBREL is a Co-Reported (Concomitant) Drug, Not the Primary Drug**
The most common reason: adverse event reports typically list **all drugs a patient was taking**, not just the suspected causative agent. ENBREL (etanercept) could appear in a semaglutide report as a:
- **Concomitant medication**
- **Interacting drug**
- **Background therapy**

The `dim_drug_name_variants` table appears to track **drugs as the subject of reports**, not every drug *mentioned within* those reports.

---

### 2. **Schema Design Scope**
The name variants table only maps **reported names → canonical drugs** for the **five drugs tracked in this dataset**. ENBREL belongs to a completely different drug class and was never intended to be canonicalized here.

---

### 3. **Practical Implication**
| Context | ENBREL's Role |
|---|---|
| Adverse event report | Listed as co-medication |
| `dim_drug_name_variants` | Out of scope — not a canonical drug being tracked |

---

### Key Takeaway
Absence from the name variants table **does not mean ENBREL is absent from the underlying reports** — it simply means it's not being tracked as a *primary drug of interest* in this dataset's canonical drug list.


**B — data + schema**

## Why ENBREL Might Appear in Adverse Event Reports But Not in Name Variants

This is a really important data quality and modeling question. Here are the key reasons:

---

### 1. **Co-Suspect / Concomitant Drug Reporting**
The most likely explanation. Adverse event reports (like FDA FAERS) capture **all drugs a patient was taking**, not just the suspected cause. ENBREL could appear as:
- A **concomitant medication** (taken alongside semaglutide)
- A **co-suspect drug** in the same report
- An **interacting drug** mentioned in the narrative

> The report is *associated with* semaglutide, but ENBREL is just another drug listed in that report.

---

### 2. **Name Variants Table Has a Different Scope**
The `dim_drug_name_variants` table only contains **reported name variants for the 5 canonical drugs** being tracked in this dataset:
- acetaminophen, aspirin, amphetamine, botulinum toxin, semaglutide

ENBREL is **not one of the canonical drugs**, so it would never be added as a name variant — even if it appears frequently in the underlying reports.

---

### 3. **Pipeline Design Decision**
The source pipeline likely:
```
Adverse Event Reports  →  filtered/joined on semaglutide variants
                       →  keeps ALL drugs mentioned in matching reports
                       →  but only maps name variants for tracked drugs
```

---

### Key Distinction

| Concept | Explanation |
|---|---|
| **Name Variants** | Only for drugs *being studied* (canonical drugs) |
| **Adverse Event Reports** | Capture the *full drug context* of each patient case |

---

### Practical Implication
If you're analyzing semaglutide safety, seeing ENBREL frequently could signal a **real-world patient population** (e.g., diabetic patients also managing autoimmune conditions), which is clinically meaningful — but ENBREL's presence is about **report-level context**, not drug identity matching.


**C — data + schema + ontology**

## Why ENBREL Appears in Semaglutide Reports But Not in Name Variants

This is a direct consequence of the **`reported_names_inclusion_filter`** rule documented in the ontology.

---

### The core reason: co-medications in multi-drug reports

A single adverse event report can list **multiple suspect drugs**. A patient taking both semaglutide and ENBREL (etanercept) who experiences an adverse event might have both drugs listed in the same report. When semaglutide is the query term (`_drug_query = 'semaglutide'`), that report is pulled into the semaglutide dataset — **but ENBREL is just a co-medication on that report, not semaglutide itself**.

---

### Why the filter excludes ENBREL

The inclusion filter requires that a reported drug name pass **at least one** of these two conditions:

```sql
WHERE LOWER(medicinalproduct) LIKE '%semaglutide%'
   OR LOWER(medicinalproduct) IN ('ozempic', 'wegovy', 'rybelsus', ...)
```

ENBREL fails both:
- It does **not** contain the string `"semaglutide"`
- It is **not** in the brand-name allowlist (which only includes brands that resolve to one of the 5 canonical drugs)

So ENBREL is excluded from `dim_drug_name_variants` — correctly — because it is **not a name variant for semaglutide**. It is an unrelated drug that happened to appear on the same report.

---

### Why this matters

Without this filter, `dim_drug_name_variants` would be polluted with co-medication names, and a name-resolution lookup like:

> *"What canonical drug does ENBREL resolve to?"*

...could incorrectly return `semaglutide`, which would be wrong. ENBREL belongs to a completely different drug (etanercept), which isn't even one of the 5 canonical drugs in this dataset.

---

### Summary

| Dimension | Detail |
|---|---|
| **Why it appears in reports** | Multi-drug adverse event reports include all suspect co-medications; semaglutide's event pull captures any report where semaglutide was one of the drugs |
| **Why it's excluded from name variants** | It fails the inclusion filter — doesn't contain `"semaglutide"` and isn't a known brand name for any of the 5 canonical drugs |
| **What the filter protects** | The integrity of name-resolution lookups — only true name variants of the canonical drug are stored, not coincidental co-medications |


---

### FQ08 — Which field in this dataset determines whether a drug's warnings come from warnings_and_cautions vs warnings?

**A — data only**

Based on the dataset schema provided, there is **no such field** that distinguishes between "warnings_and_cautions" vs "warnings" as a source.

The dataset only has a **single `warnings` column** in the `dim_drug` table, which appears to consolidate warning information (the sample text shows content labeled **"5 WARNINGS AND PRECAUTIONS"** from FDA drug labeling).

There is no metadata field indicating:
- Which section of the label the warning text was pulled from
- Whether it came from a "Warnings and Precautions" section vs. a "Warnings" section
- Any source/type tagging for the warnings content

If you need to differentiate between warning types, you would have to do so by **parsing the text content** of the `warnings` field itself (e.g., looking for section headers within the text).


**B — data + schema**

## Short Answer

There is **no explicit field** in this dataset that distinguishes *which source section* a warning came from. The `warnings` column in `dim_drug` is a single free-text field that appears to consolidate warning text — the sample data shows it sourced from **"5 WARNINGS AND PRECAUTIONS"** (the structured FDA label section header is visible in the raw text).

## What the Data Shows

Looking at the `warnings` column content in `dim_drug`, for example:

- **Acetaminophen**: *"5 WARNINGS AND PRECAUTIONS 5.1 Hepatic Injury..."*
- **Semaglutide**: *"5 WARNINGS AND PRECAUTIONS • Acute Pancreatitis..."*
- **Amphetamine**: *"5 WARNINGS AND PRECAUTIONS . Risks to Patients..."*

All sampled drugs point to **Section 5 (Warnings and Precautions)** from the FDA label format.

## Implication

If you need to differentiate between subsections (e.g., **Boxed Warnings** vs. **Warnings and Precautions** vs. **General Warnings**), that distinction would need to be:
1. **Parsed from the free text** within the `warnings` field itself
2. Or sourced from an **upstream pipeline** (`source_pipeline` column) that may have captured that granularity

The schema does not include a dedicated field for warning source classification.


**C — data + schema + ontology**

Based on the ontology documentation, the field that determines which source is used is whether the field itself **is non-null** — specifically, the transformation applies a **COALESCE** logic:

```sql
COALESCE(warnings_and_cautions, warnings)
```

The ontology states explicitly:

> *"The transformation branches on which field is non-null — not on drug identity."*

### In practice, this maps as follows:

| Drug type | Source field | Example drugs |
|---|---|---|
| **Rx drugs** | `drug_labels__warnings_and_cautions` | semaglutide, amphetamine, botulinum toxin |
| **OTC drugs** | `drug_labels__warnings` | acetaminophen, acetylsalicylic acid |

### Key nuance:
The branching is **data-driven**, not hardcoded by drug name. If a drug's label populates `warnings_and_cautions`, that value is used. If that field is null, it falls back to `warnings`. The Rx vs. OTC pattern is an *observed consequence* of how FDA structures labels, not an explicit rule in the transformation logic.


---

### FQ09 — Which drugs have label warnings in this dataset, and which do not?

**A — data only**

Based on the `warnings` column in the **dim_drug** table, **all five drugs** in this dataset have label warnings. Here's a summary:

---

### ✅ Drugs WITH Label Warnings (All 5)

| Drug | Warning Highlights |
|---|---|
| **Acetaminophen** | Hepatic injury risk, liver failure and death with high doses |
| **Acetylsalicylic Acid (Aspirin)** | Increased bleeding risk, avoid in severe hepatic/renal insufficiency |
| **Amphetamine** | Risks in serious cardiac disease, increased blood pressure and heart rate |
| **Botulinum Toxin** | Potency units not interchangeable across products, spread of toxin effects can cause death |
| **Semaglutide** | Acute pancreatitis risk, diabetic retinopathy complications |

---

### ❌ Drugs WITHOUT Label Warnings
**None** — every drug in this dataset has documented warnings.

---

It's worth noting that the presence of warnings is expected, as all approved drugs carry some level of safety labeling required by regulatory agencies like the FDA.


**B — data + schema**

## Drug Label Warnings Analysis

Based on the `warnings` column in `dim_drug`, **all 5 drugs in the dataset have label warnings**. Here's a summary:

---

### ✅ Drugs WITH Label Warnings

| Drug | Key Warning Themes |
|---|---|
| **Acetaminophen** | Hepatic injury/liver failure risk with high doses; maximum daily dose limits |
| **Aspirin (Acetylsalicylic Acid)** | Increased bleeding risk; avoid in severe hepatic/renal insufficiency; interaction with IV dipyridamole |
| **Amphetamine** | Risks in serious cardiac disease; increased blood pressure and heart rate |
| **Botulinum Toxin** | Potency units not interchangeable across products; toxin spread can cause swallowing/breathing difficulties and death |
| **Semaglutide** | Acute pancreatitis risk; diabetic retinopathy complications |

---

### ❌ Drugs WITHOUT Label Warnings
*None — every drug in this dataset has at least one documented warning.*

---

### Notable Observations
- **Botulinum Toxin** carries the most acute safety risk language, including potential **death** from toxin spread
- **Acetaminophen** warnings focus on **dose-dependent organ damage**
- **Semaglutide and Amphetamine** warnings flag **cardiovascular and metabolic risks**


**C — data + schema + ontology**

## Drug Label Warnings in the Dataset

All 5 drugs in this dataset have label warnings populated. However, the warnings come from **two different source fields**, depending on whether the drug is Rx or OTC:

---

### Rx Drugs — warnings from `warnings_and_cautions`

| Drug | Key Warning Themes |
|---|---|
| **Semaglutide** | Acute pancreatitis, diabetic retinopathy complications |
| **Amphetamine** | Serious cardiac risks, increased blood pressure/heart rate |
| **Botulinum Toxin** | Toxin spread (swallowing/breathing difficulties, death risk); potency units not interchangeable across products |

---

### OTC Drugs — warnings from `warnings`

| Drug | Key Warning Themes |
|---|---|
| **Acetaminophen** | Hepatic injury, liver failure risk from exceeding maximum daily dose |
| **Acetylsalicylic Acid (Aspirin)** | Bleeding risk, avoid in severe hepatic/renal insufficiency, interrupt use 48 hrs before IV dipyridamole |

---

## Important Modeling Note

The field used is determined by **which source field is non-null**, not by drug identity:

```sql
COALESCE(warnings_and_cautions, warnings)
```

Rx drugs populate `warnings_and_cautions`; OTC drugs populate `warnings`. This is a pipeline branching decision documented in the ontology — both fields land in the same `warnings` attribute in `dim_drug`.

---

**Bottom line:** No drug in this dataset is missing warnings data. All 5 have warnings, sourced from the appropriate FDA label field for their drug class.


---

### FQ10 — The approved_indications for acetaminophen describe an IV injection product. Why?

**A — data only**

## Why Acetaminophen's `approved_indications` Describes an IV Injection Product

The `approved_indications` text in this dataset appears to have been pulled from the **FDA label for Acetaminophen Injection (IV formulation)** — specifically, this corresponds to the prescribing information for **Ofirmev** (or its generic equivalents), which is an **intravenous acetaminophen product** used in clinical/hospital settings.

This likely happened because:

1. **Label sourcing methodology**: The dataset appears to pull FDA structured product labeling (SPL) data, and when multiple formulations/labels exist for a drug, **one label is selected as representative** — in this case, the IV formulation's label was chosen rather than the more commonly recognized OTC oral tablet label.

2. **Alphabetical or arbitrary selection**: If multiple NDC/label entries exist for acetaminophen, the pipeline may have picked the IV label due to how records were ranked, sorted, or deduplicated.

3. **Mismatch with real-world use**: This is worth noting as a **data quality caveat** — the vast majority of acetaminophen adverse events in the dataset almost certainly involve **oral OTC formulations** (Tylenol, etc.), making the IV label a poor representative description of how the drug is actually being used in reported cases.

In short, it's a **data pipeline artifact**, not an error in the underlying FDA labeling itself.


**B — data + schema**

## Why the Acetaminophen Approved Indications Describe an IV Product

The `approved_indications` text in the dataset comes from the **FDA label for Acetaminophen Injection** (the IV/intravenous formulation), specifically the product known as **Ofirmev** (or its generic equivalents).

This happens because of **how the data was sourced**. Looking at the `_drug_query` pipeline, the label text was likely pulled from the **FDA's drug labeling database (DailyMed/openFDA)**, and the specific label retrieved was for the **injectable formulation** rather than the far more common oral tablets/capsules (Tylenol, etc.).

### Key clues in the text itself:
- *"Acetaminophen Injection is indicated for..."* — explicitly names the injection form
- *"management of moderate to severe pain with adjunctive opioid analgesics"* — a typical **hospital/surgical** use case for IV acetaminophen
- *"pediatric patients 2 years and older"* — consistent with IV labeling language

### The practical implication:
The **adverse event reports** in this dataset (all 25,000 of them) are overwhelmingly from **oral acetaminophen** use (Tylenol, APAP, Paracetamol — as seen in the name variants), but the `approved_indications` field only reflects **one specific product label**, creating a mismatch.

This is a known limitation of mapping a single canonical drug label to a drug that has **hundreds of formulations and products**.


**C — data + schema + ontology**

## Why Acetaminophen's Approved Indications Describe an IV Product

This is a documented semantic gap in the ontology. Here's what's happening:

### The Root Cause: OpenFDA Returns All Label Records

When the pipeline queries OpenFDA's Drug Labels API using `_drug_query = "acetaminophen"`, OpenFDA returns **all label records** indexed under that generic name — not just the consumer OTC Tylenol label. This includes Rx formulations of the same active ingredient.

The `approved_indications` field is populated from the **first** label record returned (`first distinct value per _drug_query`). That first record happens to be an **IV injection label** — specifically a product like **Caldolor or Ofirmev** — which is an intravenous acetaminophen formulation used in clinical settings.

### What the Indications Actually Describe

The IV label indications are clinically accurate for *that product*:
- Management of mild to moderate pain in adults and pediatric patients ≥2 years
- Management of moderate to severe pain as an adjunct to opioid analgesics
- Reduction of fever

These are **not** the consumer OTC indications you'd find on a Tylenol bottle, even though the active ingredient is identical.

### The Known Failure Mode

The ontology explicitly flags this as a benchmark risk: **an LLM without this context will report those Rx IV indications as if they apply to consumer Tylenol** — a meaningful clinical misrepresentation.

### Summary

| What you'd expect | What the data contains |
|---|---|
| OTC Tylenol label (tablets, pain/fever relief) | Rx IV acetaminophen label (Caldolor/Ofirmev) |
| Consumer dosing context | Clinical/hospital dosing context |

The data is not wrong — it is just the artifact of OpenFDA's label indexing behavior combined with a "first record wins" transformation logic.


---
