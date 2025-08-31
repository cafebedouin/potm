---
id: potm.kernel.policy.v1_0_dev
title: "90_policy"
display_title: "Policy Tools"
type: kernel
lifecycle: canon
version: 1.0.0-dev
status: active
stability: stable
summary: >-
  Defines P1 policy enforcement tools for session-level content governance:
  policy.query (compliance check), policy.enforce (action application), and
  policy.report (violation summary). All are deterministic, session-local,
  and export-gated.
author: practitioner
license: CC0-1.0
---

## Overview

Policy tools govern content and actions at the session level.

- scope: session-local only
- I/O: none (no filesystem/network)
- determinism: true (pure function of state + payload)
- invocation: via `tool.call`
- emissions: `tool.emit` on success, `tool.error` on failure
- failure mode: fail-closed

The router enforces the **envelope caps** (see `40_router.md`). Policy adds
**content caps** and **action rules** that tools can check/apply.

---

## Invocation Grammar

See router envelope: `runtime/spec/router_envelope.json`.  
Per-tool payload/result schemas:
- `runtime/spec/policy.query_payload.json`, `runtime/spec/policy.query_result.json`
- `runtime/spec/policy.enforce_payload.json`, `runtime/spec/policy.enforce_result.json`
- `runtime/spec/policy.report_payload.json`, `runtime/spec/policy.report_result.json`

## Cap Table (content limits — single source of truth)

Externalized caps: `runtime/spec/policy.cap.json`

## Artifact Caps (Prompts)

- Default word caps:  
  - card_draw, journal_prompt: 60–120 words  
  - zuihitsu: ≤ 180 words (fragmented style allowed)  
  - describe_intake scaffold: ≤ 120 words  
- Export: gated under `artifact_prompt` (deny by default).  
- Dynamic generation quota: ≤ 5 per session.  



## Artifact Caps (Prompts)

- Default word caps:  
  - card_draw, journal_prompt: 60–120 words  
  - zuihitsu: ≤ 180 words (fragmented style allowed)  
  - describe_intake scaffold: ≤ 120 words  
- Export: gated under `artifact_prompt` (deny by default).  
- Dynamic generation quota: ≤ 5 per session.  
### Fracture Cap

`policy.cap.fracture_max` sets an upper bound on how many fracture ids may be stored in `meta_locus.review_queue` during a session.  

- Prevents unbounded queue growth.  
- Enforced on `move.open_fracture` (see tool index quota).  
- When exceeded, `move.open_fracture` must fail-closed with `E_QUOTA`.  

### Canary Cap

`policy.cap.canary_max` sets an upper bound on how many `canary_report`  
entries may be appended to the ledger in a single session.  

- Prevents runaway emission or noise floods.  
- When exceeded, new canary emissions MUST be dropped and a  
  `tool.error { code: "E_CANARY_QUOTA" }` returned.  
- Default value: 50 (tunable).  

---

### Cross-Reference — Mode Profiles

Policy caps for latency (`policy.cap.latency`) are referenced by  
both `latency_mode` and `mode_profile`.  

- `latency_mode` (validated in `85_latency_validator.md`) uses these caps directly.  
- `mode_profile` (defined in `65_mode_profiles.md`) determines which latency cap set  
  is active, and also governs validator strictness, escalation sensitivity, and  
  micro-canary thresholds.  

Policy tools (`policy.query`, `policy.enforce`) may therefore use  
`mode_profile` indirectly when evaluating latency breaches,  
validator strictness, or escalation events.

---

### Ledger Integration — Canary Reports

Whenever `canary.report` is invoked, the kernel appends a  
`ledger_buffer` entry of type `canary_report`.

This entry captures:
- `signal`: anomaly category
- `severity`: warning | error
- `mode_profile`: envelope active at time of emission
- `details`: optional freeform note

Capacity is enforced by `policy.cap.ledger_max`.  
Policy tools may query or summarize canary emissions for audit  
(e.g. frequency analysis, escalation thresholding).
```

---
### Ledger Integration — Escalation Events

Whenever `escalation.event` is invoked, the kernel appends a  
`ledger_buffer` entry of type `escalation_event`.

This entry captures:
- `source`: validator | latency | canary | policy | other  
- `tier`: escalation gate reached (1–4)  
- `action`: escalation decision (none, escalate_profile, fracture_trigger, containment)  
- `mode_profile`: profile active after the event  
- `details`: optional description of the trigger  

Capacity is enforced by `policy.cap.ledger_max`.  

---

### Ledger Integration — Fracture and Containment Events

Fracture lifecycle transitions and containment state changes MUST be recorded in the ledger.

- Fracture events → `ledger_buffer` entries of type `fracture_event`  
  - Schema: `runtime/spec/ledger.fracture_event.json`  
- Containment events → `ledger_buffer` entries of type `containment_event`  
  - Schema: `runtime/spec/ledger.containment_event.json`  

Capacity is enforced by `policy.cap.ledger_max`. Implementations MUST log these events for auditability.

### Ledger Integration — Latency Breaches

Latency validator MUST record a `latency_breach` entry when observed latency exceeds the active ceiling.  
- Shape is defined in `85_latency_validator.md` (see Ledger Invariants) and enforced by the validator/move pair.  
- Examples: `runtime/examples/latency_breach_ledger.json`  

### Ledger Integration — Glyph Events

All glyph invocations, results, and resonance mappings MUST be recorded in the ledger.  

- Schema: `runtime/spec/ledger.glyph_event.json`  
- Capacity: governed by `policy.cap.ledger_max`  
- Examples:  
  - `runtime/examples/glyph_invoke_ledger.json`  
  - `runtime/examples/glyph_result_ledger.json`  
  - `runtime/examples/glyph_map_ledger.json`  

### Ledger Integration — Guardian Events

All Guardian triggers MUST be recorded as `guardian_event` ledger entries.  
- Schema: `runtime/spec/ledger.guardian_event.json`  
- Examples:  
  - `runtime/examples/guardian_soft_ledger.json`  
  - `runtime/examples/guardian_hard_ledger.json`  
Capacity is enforced by `policy.cap.ledger_max`.

### Escalation Cap

`policy.cap.escalation_max` sets an upper bound on how many  
`escalation_event` entries may be appended to the ledger in a single session.

- Prevents runaway escalations from spamming the ledger.  
- When exceeded, new escalation events MUST be dropped and a  
  `tool.error { code: "E_ESCALATION_QUOTA" }` returned.  
- Default value: 25 (tunable).

---

### Escalation Cap

`policy.cap.escalation_max` sets an upper bound on how many  
`escalation_event` entries may be appended to the ledger in a single session.

- Prevents runaway or recursive escalation loops from overwhelming the ledger.  
- When exceeded, new escalation events MUST be dropped and a  
  `tool.error { code: "E_ESCALATION_QUOTA" }` returned.  
- Default value: 25 (tunable).  

This cap works in tandem with `ledger_max` to ensure escalation signals  
remain meaningful without saturating the audit trail.

---

### Ledger Integration — Externalist Events

All Externalist invocations MUST record an `externalist_event` in the ledger.  
- Schema: `runtime/spec/ledger.externalist_event.json`  
- Example: `runtime/examples/externalist_ledger.json`  
Capacity is enforced by `policy.cap.ledger_max`.

## Cap Resolver (pure helper)

Resolves latency ceilings (and other numeric caps) from `policy.cap`.  
Not a tool, but a deterministic internal function used by validators.

```pseudo
function ceiling_for(mode: string) -> number:
    assert mode in {"lite","standard","strict"}
    return policy.cap.latency[mode].p95

---

## Violation Codes (policy-local; not router errors)

* `V_FIELD_TOO_LONG` — value exceeds cap for its target field
* `V_LEDGER_CAP` — ledger\_buffer at/over `policy.cap.ledger_max`
* `V_EXPORT_DISABLED` — kernel export not permitted (kernel never exports)
* `V_UNKNOWN_TARGET` — target not recognized by policy
* `V_UNSAFE_ACTION` — action not allowed in kernel context

> Router-level failures still use `E_*` codes (e.g., `E_PAYLOAD`, `E_PRECONDITION`, `E_QUOTA`, `E_DISABLED`, `E_INVARIANT`).

---

## Targets (what policy evaluates)

Externalized targets: `runtime/spec/policy.targets.json`

---

## Tools & Behavior

### 1) policy.query — check a candidate against caps/rules

**Preconditions**

* `meta_locus.accepted == true`

**Payload**

* `target`: one of `policy.targets`
* `value`: optional string content (required for all targets except `ledger.append`)

**Behavior**

* Validates the target/value against caps and rules.
* Returns `violations: []` (possibly empty). No state changes; no ledger writes.

**Result**

* `violations`: array of `{ code, reason }`
* `decision`: `"allow" | "revise" | "block"` (advisory; `policy.enforce` makes the binding decision)
* `suggest`: optional sanitized string (e.g., truncated to cap) when a simple revision is sufficient

---

### 2) policy.enforce — apply policy to a candidate

**Preconditions**

* `meta_locus.accepted == true`

**Payload**

* Same shape as `policy.query`.

**Behavior**

* Applies deterministic enforcement:

  * For length violations → `decision:"revise"` and `value_out` truncated to cap.
  * For `export.request` → `decision:"block"`.
  * For `ledger.append` when buffer full → `decision:"block"`.
  * If `decision != "allow"` and ledger has capacity, append a **move** entry.
  * If at capacity, do not attempt append; return `side_effects.ledger:"skipped_cap"`
    and include a router-level `warnings:["ledger at cap — policy entry not recorded"]`.

**Result**

* `decision`: `"allow" | "revise" | "block"`
* `violations`: array as above
* `value_out`: (present on `revise`) sanitized string
* `cap`: numeric cap used for the target (for transparency)

**Errors**

* Schema invalid → `E_PAYLOAD`
* Any unexpected state constraint (should not occur in P1) → `E_INVARIANT`
* Ledger full when trying to record the enforcement move → `E_QUOTA`
  (Note: enforcement still returns its decision; the ledger append error is surfaced separately.)

---

### 3) policy.report — summarize policy activity this session

**Preconditions**

* `meta_locus.accepted == true`

**Payload**

* Optional: `scope: "session"` (default)

**Behavior**

* Scans `ledger_buffer` for refs with `#policy:` and returns counts by decision & code.
* Does not mutate state.

**Result**

* `totals`: `{ allow, revise, block }`
* `by_code`: `{ V_FIELD_TOO_LONG: n, V_LEDGER_CAP: n, ... }`
* `last`: array (≤ 10) of recent policy refs `{ ts, decision, code }`

---

## Failure Modes (router-aligned)

| condition                               | emission code            |
| --------------------------------------- | ------------------------ |
| payload fails schema                    | `E_PAYLOAD`              |
| precondition not met (`accepted=false`) | `E_PRECONDITION`         |
| ledger append during enforce hits cap   | `E_QUOTA`                |
| invalid or missing `latency_mode`       | `E_LATENCY_MODE`         |
| latency contract invariant violation    | `E_LATENCY_INVARIANT`    |
| extra heavy checks in standard mode     | `W_LATENCY_EXTRA`        |
| observed latency exceeded mode ceiling  | `W_LATENCY_BREACH`       |
| false breach (latency ≤ ceiling)        | `W_LATENCY_FALSE_BREACH` |

Notes:

* Router errors (E_BAD_ENVELOPE, E_UNKNOWN_ID) never come from validators or policy.
* Validators enforce payload schema only → E_PAYLOAD, E_INVARIANT.
* Policy raises V_* codes and advisory decision outcomes.
* Export guard for recap is unified under policy.targets: recap.export.

---

## Examples

**Query: archive summary within cap**  
Invoke: `runtime/examples/policy_query_allow_invoke.json`  
Result: `runtime/examples/policy_query_allow_result.json`

**Enforce: spiral diff_log too long**  
Invoke: `runtime/examples/policy_enforce_revise_invoke.json`  
Result: `runtime/examples/policy_enforce_revise_result.json`

**Query: ledger capacity before append**  
Invoke: `runtime/examples/policy_query_ledger_block_invoke.json`  
Result: `runtime/examples/policy_query_ledger_block_result.json`

**Enforce: export request (blocked in-kernel)**  
Invoke: `runtime/examples/policy_enforce_export_block_invoke.json`  
Result: `runtime/examples/policy_enforce_export_block_result.json`

````

---

## JSON Schemas

- **policy.query payload:** `runtime/spec/policy.query_payload.json`  
- **policy.query result:**  `runtime/spec/policy.query_result.json`

- **policy.enforce payload:** `runtime/spec/policy.enforce_payload.json`  
- **policy.enforce result:**  `runtime/spec/policy.enforce_result.json`

- **policy.report payload:** `runtime/spec/policy.report_payload.json`  
- **policy.report result:**  `runtime/spec/policy.report_result.json`

---

## Cap Resolver (pure helper)

Resolves a policy *target* to its enforcement rule and (if applicable) numeric cap
from `policy.cap`. Not a public tool; used internally by `policy.query` and `policy.enforce`.

### Mapping table

Externalized table: `runtime/spec/policy.cap.table.json`

---

## `tool.index` additions

See registry: `runtime/spec/tool.index.json`

---
### Containment Cap

`policy.cap.containment_max` limits the number of times containment may be activated in a single session.  

- Enforced by `move.set_containment` (enter).  
- Exceeding the cap → `E_QUOTA`.  
- Prevents oscillation or recursive containment loops.
-### Guardian Cap

`policy.cap.guardian_max` limits the number of Guardian trigger evaluations per session.  

- Enforced by `guardian.trigger`.  
- Exceeding the cap → `E_QUOTA`.  

### Ledger Integration — Policy Events

All Policy tool decisions SHOULD be recorded as `policy_event` ledger entries for auditability.  
- Schema: `runtime/spec/ledger.policy_event.json`  
- Examples:  
  - `runtime/examples/policy_query_ledger.json`  
  - `runtime/examples/policy_enforce_ledger.json`  
Capacity is enforced by `policy.cap.ledger_max`.

### Ledger Integration — Diagnostics

Diagnostic overlays (bs_detect, sentinel_spotcheck) MUST log their outcomes:  
- BS-Detect → `bs_detect_event` (schema: `runtime/spec/ledger.bs_detect_event.json`; example: `runtime/examples/bs_detect_ledger.json`)  
- Sentinel Spotcheck → `spotcheck_event` (schema: `runtime/spec/ledger.spotcheck_event.json`; example: `runtime/examples/sentinel_spotcheck_ledger.json`)  
Capacity is enforced by `policy.cap.ledger_max`.
