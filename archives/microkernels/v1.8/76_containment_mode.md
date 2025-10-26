---
id: potm.kernel.containment_mode.v1_6_dev
title: "76_containment_mode"
display_title: "Containment — Restricted Operation"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines behavior when `meta_locus.containment=true`. Only containment-mode
  tools are allowed; all other mutations fail-closed. Exit via grace path or
  abort conditions.
author: practitioner
license: CC0-1.0
---

## Purpose

When containment is enabled (`state.meta_locus.containment=true`), the kernel
enters a restricted operating envelope to prevent further drift or harm while
allowing safe resolution. This mode is deterministic, session-local, and
bounded by policy quotas.

---

## Lifecycle

1) Entry  
   - Activated by escalation Tier 4 or explicit operator call.  
   - Set via `move.set_containment` (enter).  

2) Restricted Operation  
   - Allowed: containment-mode tools only (see Tools).  
   - Disallowed: non-containment mutations (fail `E_INVARIANT`).  

3) Exit  
   - Grace Path (preferred): `77_grace_path.md`  
   - Abort (exceptional): `runtime/spec/containment.abort_payload.json` → result confirms abort.  
   - Exit sets `meta_locus.containment=false`.

---

## Tools (Allow-list in containment)

- `move.set_containment` — enter/exit containment (quota-bound; policy.cap.containment_max).  
- `containment.abort` — abort under strict conditions:  
  - Payload: `runtime/spec/containment.abort_payload.json`  
  - Result:  `runtime/spec/containment.abort_result.json`  
- `recap.spec` — read-only recap (export still gated).  
- Selected lenses — read-only diagnostics (policy and router caps still apply).

---

## Failure Modes (router-aligned)

| condition                                        | emission code   |
|--------------------------------------------------|-----------------|
| Attempt to mutate outside containment tools      | `E_INVARIANT`   |
| Quota exceeded (containment activations)         | `E_QUOTA`       |
| Invalid abort condition (unknown reason)         | `E_PAYLOAD`     |
| Exit attempted when not in containment           | `E_PRECONDITION`|

---

## Pointers

- Abort schemas:  
  - `runtime/spec/containment.abort_payload.json`  
  - `runtime/spec/containment.abort_result.json`
- Grace path contract: `kernel/77_grace_path.md`  
- Practitioner ritual: `interpretative/protocols/ritual_containment.md`
 - Ledger entry schema: `runtime/spec/ledger.containment_event.json`

---

## Notes

- All moves must log to the ledger buffer per normal conventions.  
- Export remains disabled by default (policy-guarded).  
- Containment entry is recorded with timestamp and source.
