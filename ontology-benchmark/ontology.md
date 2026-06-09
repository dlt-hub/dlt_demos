# Ontology: account_churn_risk

**Use cases:** seat-level churn risk identification, account-level churn scoring, plan segmentation, reactivation tracking, distinguishing recovered vs. new accounts.

**Source pipeline:** `filesystem_pipeline` (local CSV files)

---

## Entities

### Account

An organisation with a subscription plan and lifecycle status.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| account_id | text | accounts | **natural key** |
| company | text | accounts | |
| plan | text | accounts | subscription plan name |
| status | text | accounts | `'active'`, `'churned'` — set when ≥ 60% of paid seats are at-risk for 3 consecutive weeks |
| created_at | timestamp | accounts | |
| reactivated_at | timestamp | accounts | null when never reactivated |
| account_type | *derived* | — | `'active'`, `'churned'`, `'recovered'` (reactivated within 30 days), or `'new'` (reactivated after 30 days) |

An account is **churned** when ≥ 60% of its paid seats (excluding `SMB_MONTHLY_LEGACY` and `admin` seats) have been at-risk for 3 consecutive weeks. The 60% threshold and the 3-week duration must both be met.

If `reactivated_at` is not null, the account is `'recovered'` if reactivation happened within 30 days of churning, or `'new'` if it happened after 30 days. This distinction affects cohort counts — recovered accounts are not the same as new customers.

**Relationships:**
- ← `Seat.BELONGS_TO` — one Account has many Seats

---

### Seat

A licensed user slot assigned to an account.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| seat_id | text | seats | **natural key** |
| account_id | text | seats | FK → Account |
| user | text | seats | user identifier |
| plan_type | text | seats | `'SMB_MONTHLY'`, `'SMB_MONTHLY_LEGACY'`, `'PRO_ANNUAL'`, `'ENT_ANNUAL_V2'` |
| role | text | seats | `'admin'`, `'member'`, `'viewer'` |
| created_at | timestamp | seats | |
| is_at_risk | *derived* | — | boolean — see at-risk rules below |

A seat is **at-risk** when it has had no valid login in the last 14 days AND no API call in the last 7 days. Both conditions must be true — this is an AND, not an OR.

A login only counts as valid if `session_duration_seconds > 120`. Sessions of 120 seconds or less are ignored when computing login recency.

`SMB_MONTHLY_LEGACY` seats are excluded from at-risk calculation entirely — they do not appear in churn reports and do not count toward account churn scores.

`ENT_ANNUAL_V2` seats use a 21-day login inactivity window instead of 14 days. All other plan types use 14 days.

Seats with `role = 'admin'` are excluded from at-risk calculation regardless of their activity level.

**Relationships:**
- `BELONGS_TO` → Account (via `account_id`)
- ← `Activity.PERFORMED_BY` — one Seat has many Activity events

---

### Activity

A usage event tied to a seat — either a login or an API call. Union of `login_events` and `api_call_events`.

| Attribute | Type | Source | Notes |
|---|---|---|---|
| event_id | text | login_events, api_call_events | **natural key** (unique per source table) |
| seat_id | text | login_events, api_call_events | FK → Seat |
| timestamp | timestamp | login_events, api_call_events | |
| activity_type | *derived* | — | `'login'` or `'api_call'` — derived from source table at transformation time |
| session_duration_seconds | bigint | login_events only | null for api_call rows |
| endpoint | text | api_call_events only | null for login rows |
| status_code | bigint | api_call_events only | null for login rows |

Login events with `session_duration_seconds ≤ 120` are present in the raw data but do not count as valid activity. They must be filtered out before computing login recency for at-risk scoring.

**Relationships:**
- `PERFORMED_BY` → Seat (via `seat_id`)

---

## Relationship summary

```
Account
  └── has many Seats       (Seat.account_id → Account.account_id)
        └── has many Activities  (Activity.seat_id → Seat.seat_id)
```

---

## Assumptions & exclusions

1. `login_events` and `api_call_events` are unioned into a single `Activity` entity — rows are additive, no overlap by `event_id`.
2. `activity_type` is not a source column — derived from which source table contributed the row.
3. `reactivated_at` is null for accounts that have never reactivated.

**Excluded tables:** `_dlt_loads`, `_dlt_version`, `_dlt_pipeline_state` — dlt internals, no business relevance.
