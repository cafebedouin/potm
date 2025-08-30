---
id: potm.kernel.closure.v1_6_dev
title: "80_closure"
display_title: "Closure Tools"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines P1 closure tools for session-level cycle operations: spiral (drift vs evolution),
  archive (final snapshot), and waiting_with (active containment). Tools are deterministic,
  session-local, and never export; any export is adapter-side and policy-gated.
author: practitioner
license: CC0-1.0
---

## Overview

Closure tools package or gate ongoing threads at the **session** level.

Provided tools (registered in `tool.index`):
- `closure.spiral`
- `closure.archive`
- `closure.waiting_with`

All are invoked via `tool.call`, read/write only session state (`70_state.md`),
and emit structured results or `tool.error` with router-aligned codes.

- scope: session-local only  
- I/O: none (no filesystem/network)  
- determinism: true (pure function of state + payload)  
- failure mode: fail-closed  

---

## Invocation

`tool.call` with `id: "closure.<tool_name>"` and payload matching schema.  

`<tool_name>` ∈ { `spiral`, `archive`, `waiting_with` }.  

> Envelope errors & unknown tools are handled by the router (`E_NAMESPACE` / `E_TOOL` / `E_PAYLOAD`).  

---

## Tool Schemas & Behavior

### 1) `closure.spiral` — drift vs evolution summary

- **Payload schema**: defined in `runtime/schema/closure_spiral.json`  
- **Result**: emits `diff_log` string (≤ `policy.cap.diff_log_max`, 400 chars)  

See:  
- `runtime/examples/closure_spiral_invoke.json`  
- `runtime/examples/closure_spiral_result.json`

Ledger: `closure_event`
- Schema: `runtime/spec/ledger.closure_event.json`
- Example: `runtime/examples/closure_spiral_ledger.json`

---

### 2) `closure.archive` — final snapshot of a cycle

- **Preconditions**: `len(meta_locus.review_queue) == 0` (else `E_PRECONDITION`)  
- **Payload schema**: `runtime/schema/closure_archive.json`  
- **Result**: may include `summary`, `takeaways`, `archive_status`  

See:  
- `runtime/examples/closure_archive_invoke.json`  
- `runtime/examples/closure_archive_result.json`

Ledger: `closure_event`
- Schema: `runtime/spec/ledger.closure_event.json`
- Example: `runtime/examples/closure_archive_ledger.json`

---

### 3) `closure.waiting_with` — active containment for unresolved tensions

- **Preconditions**: `len(meta_locus.review_queue) > 0`  
- Sets `meta_locus.containment = true`; auto-clears via `70_state.md` when queue empties.  
- **Payload schema**: `runtime/schema/closure_waiting_with.json`  

See:  
- `runtime/examples/closure_waiting_with_invoke.json`  
- `runtime/examples/closure_waiting_with_result.json`

Ledger: `closure_event`
- Schema: `runtime/spec/ledger.closure_event.json`
- Example: `runtime/examples/closure_waiting_with_ledger.json`

---

## Data Annexes (read-only, optional)

* `ANNEX:FRACTURE_TAXONOMY_MINI` (P1-MIN; improves spiral wording)  

Ledger: `closure_event`
- Schema: `runtime/spec/ledger.closure_event.json`
- Example: `runtime/examples/closure_archive_ledger.json`

* Fracture Taxonomy (master): `extended/diagnostics/fracture/fracture_taxonomy_master_table.md`  
* `ANNEX:FRACTURE_CROSSWALK` (optional)  
* `ANNEX:FRACTURE_META_UNITY` (optional)  

> Annexes refine labels only; absence must not change tool behavior.  

---

## Failure Modes (router-aligned)

| condition                               | emission code    |
| --------------------------------------- | ---------------- |
| payload fails schema                    | `E_PAYLOAD`      |
| open fractures on `closure.archive`     | `E_PRECONDITION` |
| `waiting_with` without open fracture    | `E_PRECONDITION` |
| ledger buffer full during ledger append | `E_QUOTA`        |

---

## Versioning & Change Log

* **1.6.0-dev**: Initial P1 spec for `closure.spiral`, `closure.archive`, `closure.waiting_with`; router-aligned errors; state-gated preconditions; policy-gated caps; idempotent outputs.
