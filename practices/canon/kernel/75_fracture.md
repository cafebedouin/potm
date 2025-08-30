---
id: potm.kernel.fracture_queue.v1_6_dev
title: "75_fracture"
display_title: "Fracture — Queue Integration"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Integrates the fracture queue contract across the kernel. Defines lifecycle
  transitions and points all tools/gates to a single fracture entry schema.
author: practitioner
license: CC0-1.0
---

## Purpose

Fractures are audit artifacts created when validator/policy/latency signals
indicate a potential invariant breach. The kernel records them as structured
entries and manages their lifecycle via explicit moves. The `review_queue`
stores fractureId strings only; full entries live in a session-local
`fracture_log` map keyed by fractureId.

All queue entries conform to:
- `runtime/schema/fracture_entry.json`

Examples (invocations):
- `runtime/examples/fracture_open.json`
- `runtime/examples/fracture_review.json`
- `runtime/examples/fracture_resolve.json`

---

## Lifecycle

1) Open → entry created with `status: open`; recorded in `fracture_log` and its id appended to `meta_locus.review_queue`.  
2) Review → entry marked `status: review`.  
3) Resolved → entry marked `status: resolved` and dequeued.  

Moves (pointers):
- open: `move.open_fracture`  
- review: `move.review_fracture`  
- resolve: `move.close_review`  

---

## Failure Modes

- Invalid `fracture_id` (not string or missing) → `E_PAYLOAD`.  
- Resolve non-existent `fracture_id` → `E_INVARIANT`.  
- Queue quota exceeded (policy-bound) → `E_QUOTA`.  
- Attempt to resolve when not in `review` → `E_PRECONDITION`.  

---

## Specs

- move.open_fracture — payload/result:  
  - `runtime/spec/move.open_fracture_payload.json`  
  - `runtime/spec/move.open_fracture_result.json`
- move.review_fracture — payload/result:  
  - `runtime/spec/move.review_fracture_payload.json`  
  - `runtime/spec/move.review_fracture_result.json`
- move.close_review — payload/result:  
  - `runtime/spec/move.close_review_payload.json`  
  - `runtime/spec/move.close_review_result.json`

---

## References

- State locus & queue: `70_state.md`  
- Escalation Tier 3 trigger: `68_escalation_gates.md`  
- Escalation Tier 4: enters containment; see `76_containment_mode.md`  
- Entry schema: `runtime/schema/fracture_entry.json`  

---

## Annex & Playbooks (diagnostics)

Practitioner-facing fracture diagnostics and crosswalks live under `extended/` and `meta/`:

- Fracture Finder (protocol): `extended/diagnostics/fracture/fracture_finder.md`  
- Fracture Finder Playbook: `extended/diagnostics/fracture/fracture_finder_playbook.md`  
- Fracture Crosswalk (labels/thresholds): `extended/diagnostics/fracture/fracture_crosswalk.md`  
- Fracture Meta (taxonomy, notes): `meta/fracture_meta`  

These materials inform naming, review heuristics, and resolution patterns. They do not change kernel invariants or schemas.
