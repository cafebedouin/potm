---
id: potm.kernel.latency_validator_min.v1_6_dev
title: "85_latency_validator_min"
display_title: "Latency Validator — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  The only validator resident in the microkernel. Runs before any tool
  execution, checks observed latency against policy ceilings, emits
  warnings/errors, and appends latency_breach events to the ledger.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, validator, latency]
author: practitioner
license: CC0-1.0
---

# Latency Validator — Minimal Contract

## 0) Scope

- Runs **first** in router dispatch order.  
- Purely session-local; does not call network.  
- Consumes `meta_locus.latency_mode` and `observed_latency_ms` from the
  router envelope.  
- Writes at most one ledger event (`ledger.latency_breach.json`).  
- Emits either:
  - `E_LATENCY_MODE` if `latency_mode` invalid,  
  - `E_LATENCY_INVARIANT` if p95 ceiling breached,  
  - `W_LATENCY_BREACH` if p50 ceiling breached but under p95.  
- On error, router halts execution. On warning, router continues.

---

## 1) Inputs

**Envelope fields (subset of `runtime/spec/router_envelope.json`):**

```json
{
  "observed_latency_ms": 4800,
  "meta": { "latency_mode": "standard" }
}
````

**Schemas:**

* `runtime/spec/latency.validator_payload.json`
* `runtime/spec/latency.validator_result.json`

---

## 2) Policy reference

**File:** `runtime/spec/policy.cap.json` (and table variant `policy.cap.table.json`)

Minimal required field:

```json
{
  "cap": {
    "latency": {
      "lite":     { "p50_ms": 2000, "p95_ms": 4000 },
      "standard": { "p50_ms": 4000, "p95_ms": 6000 },
      "strict":   { "p50_ms": 8000, "p95_ms": 12000 }
    },
    "ledger_max": 512
  }
}
```

---

## 3) Behavior

1. **Check mode.**
   If `latency_mode ∉ {lite, standard, strict}` → emit `E_LATENCY_MODE`.

2. **Compare observed latency.**

   * If `observed_latency_ms ≤ p50_ms` → success (no emission).
   * If `p50_ms < observed_latency_ms ≤ p95_ms` → emit `W_LATENCY_BREACH`.
   * If `observed_latency_ms > p95_ms` → emit `E_LATENCY_INVARIANT` and halt.

3. **Ledger.**

   * For `warn` or `error`, append an entry to `ledger.latency_breach.json`.
   * Examples: see `runtime/examples/latency_breach_ledger.json`,
     `state_log_latency_breach.json`.

---

## 4) Result schema

**Reference:** `runtime/spec/latency.validator.result.json`

Example result (warning):

```json
{
  "status": "warn",
  "mode": "standard",
  "observed_ms": 5200,
  "p50_ms": 4000,
  "p95_ms": 6000,
  "code": "W_LATENCY_BREACH"
}
```

---

## 5) Error / Warning codes

| code                  | description                                     |
| --------------------- | ----------------------------------------------- |
| `E_LATENCY_MODE`      | Invalid `latency_mode` in meta\_locus           |
| `E_LATENCY_INVARIANT` | Observed latency > p95 ceiling (hard stop)      |
| `W_LATENCY_BREACH`    | Observed latency > p50 ceiling (warn, continue) |

---

## 6) Annex

* **Schemas:**

  * `runtime/spec/latency.validator_payload.json`
  * `runtime/spec/latency.validator_result.json`
* **Policy caps:** `runtime/spec/policy.cap.json`
* **Ledger schema:** `runtime/spec/ledger.latency_breach.json`
* **Examples:** `runtime/examples/latency_breach_ledger.json`, `runtime/examples/state_log_latency_breach.json`

