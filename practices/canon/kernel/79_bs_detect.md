---
id: potm.kernel.bs_detect.v1_6_dev
title: "79_bs_detect"
display_title: "BS-Detect — Diagnostic Stub"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Session-local diagnostic that classifies likely BS patterns and routes to
  fracture review when warranted. Always logs to the ledger.
author: practitioner
license: CC0-1.0
---

## Purpose

`bs_detect` scans recent emissions for telltale patterns (confident claims with
low support, rhetoric over structure, sliding definitions). It is a diagnostic
overlay: it does not decide; it emits a result and logs an event for audit.

---

## Lifecycle

1) Invoke (session-local)  
2) Classify pattern and propose fracture_id when appropriate  
3) Emit result and log `bs_detect_event`  

---

## Failure Modes

- Missing `fracture_id` on fail classification → `E_PAYLOAD`  
- Invalid classification label → `E_PAYLOAD`  
- Recursive invocation without new evidence → `E_INVARIANT`  

---

## Pointers

- Result schema: `runtime/spec/bs_detect_result.json`  
- Ledger schema: `runtime/spec/ledger.bs_detect_event.json`  
- State & ledger examples: `kernel/70_state.md`  

Note: Practitioner protocol lives under `extended/diagnostics/bs_detect.md`.

---

## Examples

- Invoke: `runtime/examples/bs_detect_invoke.json`  
- Result: `runtime/examples/bs_detect_result.json`  
- Ledger: `runtime/examples/bs_detect_ledger.json`
