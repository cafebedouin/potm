---
id: potm.kernel.grace_path.v1_6_dev
title: "77_grace_path"
display_title: "Grace Path — Safe Exit from Containment"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines a graceful exit sequence from containment: reduce tension,
  provide minimal recap, and close the session safely.
author: practitioner
license: CC0-1.0
---

## Lifecycle

1) Invocation  
   - Called only when `meta_locus.containment=true`.  
   - Initiated by operator request or as part of Tier 4 resolution.  

2) Reduction  
   - Limit to containment-mode tools; produce a compact recap and next-safe-step.  

3) Exit  
   - Set `meta_locus.containment=false` via `move.set_containment` (exit).  
   - Record exit in ledger; session may end.

---

## Pointers

- Example call: `runtime/examples/containment_exit.json`  
- Ritual (practitioner-facing): `interpretative/protocols/ritual_containment.md`  
- Containment contract: `kernel/76_containment_mode.md`

---

## Failure Modes

- Invoked outside containment → `E_PRECONDITION`  
- Recursive invocation (during an active grace path) → `E_INVARIANT`  

