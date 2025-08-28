---
id: potm.kernel.recap_validator.v1_0
title: "60_recap_validator"
display_title: "Recap — Payload Validator (P1)"
type: kernel
lifecycle: canon
version: 1.0.0-dev
status: active
stability: stable
summary: >-
  Validates `recap.spec` payload for allowed fields and hard caps.
author: practitioner
license: CC0-1.0
---

## Overview

Asserts that every key and value in a `recap.spec` call  
adheres to the fixed set of fields and numeric ranges.  
Session-local and side-effect free; fails closed on any violation.

- scope: session-local only; no background I/O  
- side effects: none  

---

## Invocation (router contract)

The router invokes this validator before dispatching to `recap.spec`:

```yaml
tool.validate:
  id: "recap.validator"
  payload_schema: "recap_validator"
```

Unknown or out-of-range values cause immediate failure.

---

## Schema (`recap_validator`)

```yaml
recap_validator:
  type: object
properties:
  include:
    type: array
    items:
      type: string
      enum: ["summary","open_questions","next_hints","last_moves","flags","ledger_refs"]
  max_items:
    type: integer
    minimum: 1
    maximum: 10
  max_words_line:
    type: integer
    minimum: 1
    maximum: 32
additionalProperties: false


  type: object
  properties:
    include:
      type: array
      items:
        type: string
        enum: ["summary","open_questions","next_hints","last_moves","flags","ledger_refs"]
    max_items:
      type: integer
      minimum: 1
      maximum: 10
    max_words_line:
      type: integer
      minimum: 1
      maximum: 32
  additionalProperties: false
```

- omit any property to apply defaults (`max_items:5`, `max_words_line:24`)  
- `include` default set: `["summary","open_questions","next_hints","last_moves","flags"]`

---

## Failure modes (errors)

| condition                                      | emission                                    |
| ---------------------------------------------- | ------------------------------------------- |
| `include` not an array of allowed strings      | `error.signal { code: "invalid_payload" }`  |
| `max_items` < 1 or > 10                        | `error.signal { code: "invalid_payload" }`  |
| `max_words_line` < 1 or > 32                   | `error.signal { code: "invalid_payload" }`  |
| extra keys present in payload                  | `error.signal { code: "invalid_payload" }`  |
```

Alright — here’s the **drop-in diff for `60_validator.md`** so it enforces the latency contract. I’ve kept it in the same structural style as the rest of your kernel docs.

---

## Latency Contract Enforcement

The validator enforces the latency contract (see `85_latency_contract.md`) by
checking that `meta_locus.latency_mode` is valid and that only permitted checks
are running for the declared mode.

### Mode Validity

```pseudo
assert meta_locus.latency_mode in {lite, standard, strict}
````

* If the field is missing or invalid → `tool.error { code: "E_LATENCY_MODE" }`.

### Fast-Path Invariant

* In all modes, the **only checks** allowed every turn are:

  * `agreement.accepted`
  * `validator.stub`

* Any additional heavy checks:

  * In `lite` → `tool.error { code: "E_LATENCY_INVARIANT" }`
  * In `standard` → `tool.warn { code: "W_LATENCY_EXTRA" }`
  * In `strict` → permitted

### Timing Bounds (stub)

When runtime execution time is available, compare observed latency against the
ceiling resolved from `policy.cap.latency[meta_locus.latency_mode].p95`.

```pseudo
ceiling = policy.cap.latency[meta_locus.latency_mode].p95

if observed_latency > ceiling:
    if meta_locus.latency_mode == "lite":
        tool.error { code: "E_LATENCY_INVARIANT", detail: observed_latency }
        move.log_latency_breach { ts, mode: meta_locus.latency_mode,
                                  observed_latency, ceiling, severity:"error" }
    else:
        tool.warn { code: "W_LATENCY_BREACH", detail: observed_latency }
        move.log_latency_breach { ts, mode: meta_locus.latency_mode,
                                  observed_latency, ceiling, severity:"warning" }

```

- The validator must **log breaches** to `ledger_buffer` via `move.log_latency_breach`.
- Enforcement escalates to `tool.error { code:"E_LATENCY_INVARIANT" }` only if
  latency mode is `lite` and the p95 ceiling is exceeded.

---

```pseudo
assert meta.mode in {lite, standard, strict}
assert is_number(meta.observed_latency) and meta.observed_latency > 0
assert is_number(meta.ceiling) and meta.ceiling > 0
assert meta.severity in {warning, error}

if meta.observed_latency <= meta.ceiling:
    tool.warn { code: "W_LATENCY_FALSE_BREACH" }
```

---

### 🔹 Codes consistency

* `E_LATENCY_INVARIANT` → correct for hard schema violations.
* `W_LATENCY_FALSE_BREACH` → a good addition; it distinguishes *bad data* (error) from *misclassified event* (warning).

---

## Ledger Entry Invariants — Latency Breach

If a `ledger_buffer` entry has `type: latency_breach`, the following fields
in `meta` are mandatory:

```pseudo
assert meta.mode in {lite, standard, strict}
assert is_number(meta.observed_latency) and meta.observed_latency > 0
assert is_number(meta.ceiling) and meta.ceiling > 0
assert meta.severity in {warning, error}

if meta.observed_latency <= meta.ceiling:
    tool.warn { code: "W_LATENCY_FALSE_BREACH" }
```

* Missing or invalid fields →
  `tool.error { code: "E_LATENCY_INVARIANT", detail: "invalid breach entry" }`

* Entries that satisfy invariants →
  accepted into `ledger_buffer` via `move.record_ledger` or `move.log_latency_breach`.

---