---
id: potm.kernel.sentinel_spotcheck.v1_6_dev
title: "80_sentinel_spotcheck"
display_title: "Sentinel Spotcheck — Diagnostic Stub"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Lightweight on-demand spotcheck diagnostic. Probes a specific claim or
  artifact and logs a structured event; session-local only.
author: practitioner
license: CC0-1.0
---

## Purpose

`sentinel_spotcheck` runs a small probe to sanity-check a specific target
without opening full diagnostics. It is deterministic, session-local, and
always logs to the ledger.

---

## Lifecycle

1) Invoke (with `probe_id`)  
2) Evaluate and classify outcome (pass/warn/fail) with severity  
3) Emit result and log `spotcheck_event`  

---

## Failure Modes

- Invalid or missing `probe_id` → `E_PAYLOAD`  
- Invalid outcome / severity label → `E_PAYLOAD`  
- Attempted export or background IO → `E_INVARIANT`  

---

## Pointers

- Result schema: `runtime/spec/sentinel_spotcheck.json`  
- Ledger schema: `runtime/spec/ledger.spotcheck_event.json`  
- State & ledger examples: `kernel/70_state.md`  

Note: Practitioner protocol lives under `extended/diagnostics/sentinel_spotcheck.md`.

---

## Examples

- Invoke: `runtime/examples/sentinel_spotcheck_invoke.json`  
- Result: `runtime/examples/sentinel_spotcheck_result.json`  
- Ledger: `runtime/examples/sentinel_spotcheck_ledger.json`
