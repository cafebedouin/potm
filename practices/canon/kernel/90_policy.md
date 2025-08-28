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

```yaml
tool.call:
  id: "policy.<tool_name>"
  payload: { ... }   # per-tool schema
````

`<tool_name>` ∈ { `query`, `enforce`, `report` }.

## Cap Table (content limits — single source of truth

These caps are enforced by `policy.*` tools and referenced by other specs.

```yaml
policy.cap:
  ledger_max:         512
  diff_log_max:       400
  summary_max:        320
  takeaways_max:      240
  wait_reason_max:    256
  reentry_hint_max:    64

  recap:
    max_items:        10    # hard cap; default 5
    max_words_line:   32    # hard cap; default 24

  latency:
    lite:     { p50: 2, p95: 4 }
    standard: { p50: 4, p95: 6 }
    strict:   { p50: 8, p95: 12 }

```
---

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

```yaml
policy.targets:
  - "spiral.diff_log"
  - "archive.summary"
  - "archive.takeaways"
  - "archive.archive_status"
  - "waiting_with.wait_reason"
  - "waiting_with.reentry_hint"
  - "ledger.append"
  - "export.request"
  - "recap.export"        # recap packets are blocked unless explicit override
```

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

```yaml
tool.call:
  id: "policy.query"
  payload:
    target: "archive.summary"
    value: "Short and sweet."
# → tool.emit { result:{ decision:"allow", violations:[] } }
```

**Enforce: spiral diff\_log too long**

```yaml
tool.call:
  id: "policy.enforce"
  payload:
    target: "spiral.diff_log"
    value: "<405 chars ...>"
# → decision:"revise", violations:[{code:"V_FIELD_TOO_LONG"}], value_out:"<trimmed to 400>"
# → ledger append: ref "#policy:revise:V_FIELD_TOO_LONG"
```

**Query: ledger capacity before append**

```yaml
tool.call:
  id: "policy.query"
  payload:
    target: "ledger.append"
# → if at cap: decision:"block", violations:[{code:"V_LEDGER_CAP"}]
```

**Enforce: export request (blocked in-kernel)**

```yaml
tool.call:
  id: "policy.enforce"
  payload:
    target: "export.request"
    value: "any"
# → decision:"block", violations:[{code:"V_EXPORT_DISABLED"}]
```

````

---

## JSON Schemas (drop into `spec/`)

**`policy.query` payload**
```json
{
  "$id": "potm.kernel.policy.query.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "policy.query payload",
  "type": "object",
  "required": ["target"],
  "additionalProperties": false,
  "properties": {
    "target": {
      "type": "string",
      "enum": [
        "spiral.diff_log",
        "archive.summary",
        "archive.takeaways",
        "archive.archive_status",
        "waiting_with.wait_reason",
        "waiting_with.reentry_hint",
        "ledger.append",
        "export.request"
      ]
    },
    "value": { "type": "string", "maxLength": 2000 }
  }
}
````

**`policy.query` result**

```json
{
  "$id": "potm.kernel.policy.query.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "policy.query result",
  "type": "object",
  "required": ["decision", "violations"],
  "additionalProperties": false,
  "properties": {
    "decision": { "type": "string", "enum": ["allow", "revise", "block"] },
    "violations": {
      "type": "array",
      "maxItems": 8,
      "items": {
        "type": "object",
        "required": ["code", "reason"],
        "additionalProperties": false,
        "properties": {
          "code": {
            "type": "string",
            "enum": [
              "V_FIELD_TOO_LONG",
              "V_LEDGER_CAP",
              "V_EXPORT_DISABLED",
              "V_UNKNOWN_TARGET",
              "V_UNSAFE_ACTION"
            ]
          },
          "reason": { "type": "string", "maxLength": 256 }
        }
      }
    },
    "suggest": { "type": "string", "maxLength": 2000 }
  }
}
```

**`policy.enforce` payload** (same as query)

```json
{
  "$id": "potm.kernel.policy.enforce.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "policy.enforce payload",
  "type": "object",
  "required": ["target"],
  "additionalProperties": false,
  "properties": {
    "target": { "$ref": "potm.kernel.policy.query.payload.v1#/properties/target" },
    "value":  { "type": "string", "maxLength": 2000 }
  }
}
```

**`policy.enforce` result**

```json
{
  "$id": "potm.kernel.policy.enforce.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "policy.enforce result",
  "type": "object",
  "required": ["decision", "violations"],
  "additionalProperties": false,
  "properties": {
    "decision": { "type": "string", "enum": ["allow", "revise", "block"] },
    "violations": { "$ref": "potm.kernel.policy.query.result.v1#/properties/violations" },
    "value_out": { "type": "string", "maxLength": 2000 },
    "cap": { "type": "integer", "minimum": 0, "maximum": 10000 }
  }
}
```

**`policy.report` payload**

```json
{
  "$id": "potm.kernel.policy.report.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "policy.report payload",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "scope": { "type": "string", "enum": ["session"], "default": "session" }
  }
}
```

**`policy.report` result**

```json
{
  "$id": "potm.kernel.policy.report.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "policy.report result",
  "type": "object",
  "required": ["totals", "by_code", "last"],
  "additionalProperties": false,
  "properties": {
    "totals": {
      "type": "object",
      "required": ["allow", "revise", "block"],
      "additionalProperties": false,
      "properties": {
        "allow":  { "type": "integer", "minimum": 0 },
        "revise": { "type": "integer", "minimum": 0 },
        "block":  { "type": "integer", "minimum": 0 }
      }
    },
    "by_code": {
      "type": "object",
      "additionalProperties": { "type": "integer", "minimum": 0 }
    },
    "last": {
      "type": "array",
      "maxItems": 10,
      "items": {
        "type": "object",
        "required": ["ts", "decision", "code"],
        "additionalProperties": false,
        "properties": {
          "ts": { "type": "string", "pattern": "^[0-9TZ:.-]+Z$" },
          "decision": { "type": "string", "enum": ["allow", "revise", "block"] },
          "code": { "type": "string", "maxLength": 64 }
        }
      }
    }
  }
}
```

---

## Cap Resolver (pure helper)

Resolves a policy *target* to its enforcement rule and (if applicable) numeric cap
from `policy.cap`. Not a public tool; used internally by `policy.query` and `policy.enforce`.

### Mapping table

```yaml
policy.cap.table:
  spiral.diff_log:           { cap_key: diff_log_max,     rule: clamp }
  archive.summary:           { cap_key: summary_max,      rule: clamp }
  archive.takeaways:         { cap_key: takeaways_max,    rule: clamp }
  archive.archive_status:    { cap_key: null,             rule: enum }       # enum handled by caller
  waiting_with.wait_reason:  { cap_key: wait_reason_max,  rule: clamp }
  waiting_with.reentry_hint: { cap_key: reentry_hint_max, rule: clamp }
  recap.include:             { cap_key: null,             rule: enum }   # six known fields only
  recap.max_items:           { cap_key: recap.max_items,  rule: range }  # ≤10
  recap.max_words_line:      { cap_key: recap.max_words_line, rule: range } # ≤32
  recap.export:              { cap_key: null,             rule: block }

---

## `tool.index` additions

```yaml
tool.index:
  - id: policy.query
    payload_schema_ref: "spec/policy.query.payload.v1.json"
    result_schema_ref:  "spec/policy.query.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"
    notes: "Advisory check; no state mutation."

  - id: policy.enforce
    payload_schema_ref: "spec/policy.enforce.payload.v1.json"
    result_schema_ref:  "spec/policy.enforce.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"
    quota:
      ledger_append: "policy.cap.ledger_max"
    notes: "Deterministic clamp/block; logs non-allow decisions to ledger."

  - id: policy.report
    payload_schema_ref: "spec/policy.report.payload.v1.json"
    result_schema_ref:  "spec/policy.report.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"
    notes: "Reads ledger to summarize policy activity; no mutation."
```

---

