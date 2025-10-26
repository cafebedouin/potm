Perfect — here’s a clean **`85_latency_validator.md v1.0.0`** that pulls the latency enforcement logic out of the corrupted `60_recap_validator.md` and gives it its own stable home. It follows the same kernel doc style you’ve used elsewhere.

---

````markdown
---
id: potm.kernel.latency_validator.v1_0
title: "85_latency_validator"
display_title: "Latency — Contract Validator (P1)"
type: kernel
lifecycle: canon
version: 1.0.0
status: active
stability: stable
summary: >-
  Validates adherence to latency mode contract. Ensures mode is valid,
  checks permitted checks per mode, and enforces p50/p95 ceilings
  from `policy.cap.latency`.
author: practitioner
license: CC0-1.0
---

## Overview

This validator enforces the **latency contract** across all kernel turns.

- scope: session-local only  
- side effects: logs breaches to `ledger_buffer` via `move.log_latency_breach`  
- failure mode: fail-closed (router halts dispatch on error)  

---

## Invocation (router contract)

Payload/Result schemas externalized:
- `runtime/spec/latency.validator.payload.json`
- `runtime/spec/latency.validator.result.json`

---

## Schema (`latency_validator`)

See `runtime/spec/latency.validator.payload.json`.

* `latency_mode` must be valid.
* `observed_latency` and `ceiling` must be positive numbers.
* `severity` distinguishes warning vs. error handling.
* Ceilings are resolved from `policy.cap.latency` (p95 per mode).

---

## Contract Rules

### 1. Mode validity

```pseudo
assert meta_locus.latency_mode in {lite, standard, strict}
```

If invalid →
`tool.error { code: "E_LATENCY_MODE" }`

---

### 2. Fast-path invariant

* In all modes, only these checks are always allowed:

  * `agreement.accepted`
  * `validator.stub`

* Heavy checks:

  * `lite` → forbidden → `tool.error { code: "E_LATENCY_INVARIANT" }`
  * `standard` → discouraged → `tool.warn { code: "W_LATENCY_EXTRA" }`
  * `strict` → permitted

---

### 3. Timing bounds

```pseudo
ceiling = policy.cap.latency[latency_mode].p95

if observed_latency > ceiling:
    if latency_mode == "lite":
        tool.error { code: "E_LATENCY_INVARIANT", detail: observed_latency }
        move.log_latency_breach { ts, mode: latency_mode,
                                  observed_latency, ceiling, severity:"error" }
    else:
        tool.warn { code: "W_LATENCY_BREACH", detail: observed_latency }
        move.log_latency_breach { ts, mode: latency_mode,
                                  observed_latency, ceiling, severity:"warning" }
```

---

## Ledger Invariants — Latency Breach

If a `ledger_buffer` entry has `type: latency_breach`, its `meta` must include:

```pseudo
assert mode in {lite, standard, strict}
assert is_number(observed_latency) and observed_latency > 0
assert is_number(ceiling) and ceiling > 0
assert severity in {warning, error}
```

If `observed_latency <= ceiling`:
`tool.warn { code: "W_LATENCY_FALSE_BREACH" }`

Invalid entries →
`tool.error { code: "E_LATENCY_INVARIANT", detail:"invalid breach entry" }`

Valid entries →
accepted into `ledger_buffer` via `move.log_latency_breach`.

Schema & example:  
- `runtime/spec/ledger.latency_breach.json`  
- `runtime/examples/latency_breach_ledger.json`

---

## Failure Modes (router-aligned)

| condition                             | emission code            |
| ------------------------------------- | ------------------------ |
| invalid or missing `latency_mode`     | `E_LATENCY_MODE`         |
| invariant violated in `lite` mode     | `E_LATENCY_INVARIANT`    |
| heavy check in `standard` mode        | `W_LATENCY_EXTRA`        |
| latency ceiling exceeded (warn modes) | `W_LATENCY_BREACH`       |
| false breach (≤ ceiling)              | `W_LATENCY_FALSE_BREACH` |
| invalid ledger breach entry           | `E_LATENCY_INVARIANT`    |

---

## Notes

* Ceilings are authoritative in `policy.cap.latency`.
* Severity escalates only in `lite` mode.
* Logging is mandatory for transparency; every breach must yield a ledger entry.

```

---
