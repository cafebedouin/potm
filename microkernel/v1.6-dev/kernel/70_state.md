---
id: potm.kernel.state.v1_6_dev
title: "70_state"
display_title: "State — Session State & Locus"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines the session-local state model, including `meta_locus` and the in-
  memory ledger buffer. All state is deterministic, in-memory, and read/write
  via explicit kernel moves.
author: practitioner
license: CC0-1.0
---

## Overview

Session state is purely in-memory and scoped to the current session.  
The kernel treats state as an explicit contract: tools may read or write  
only via defined lenses or moves. No background I/O or filesystem writes.

- scope: session-local only  
- I/O: none  
- determinism: true (state is a pure function of moves)  
- failure mode: fail-closed (invalid updates are rejected)  

---

## State Components

1. meta_locus  
2. ledger_buffer  

### meta_locus

Holds session flags and review queue used for gating and diagnostics.

```yaml
meta_locus:
  accepted:      true|false       # has entry gate been accepted?
  # derived (normative): fracture_active := (len(review_queue) > 0)
  # MUST NOT be stored; any read computes it from `review_queue`.
  containment:    true|false      # is containment mode enabled?
  review_queue:   []              # array of fracture ids pending review
```

- additionalProperties: false  
- initial state:  
  accepted: false  
  containment: false  
  review_queue: []  

#### Invariants

- `accepted` may transition only false → true   # exit ends the session; kernel does not flip it back
- `containment` may enable only if `len(review_queue) > 0`; auto-disable when queue becomes empty

### ledger_buffer

A chronological, in-memory array of lightweight ledger entries  
recording artifacts, moves, and optional exports.

```yaml
ledger_buffer:
  - entry_id: "<uuid>"
    ts: "2025-08-26T15:04:05Z"
    type:  "move|artifact|export"
    ref:   "<artifact_ref|null>"
    meta?:                         # optional metadata
      tool_call: { id: "...", payload: { ... } }
```

- additionalProperties: false  
- max length: session-cap (see `90_policy.md`)  
- entries expire only at session end  

---

## Read & Write Access (tools)

Tools interact with state only via these contracts:

| Operation        | Tool namespace     | Effect                                |
| ---------------- | ------------------ | ------------------------------------- |
| Read meta_locus  | lens.locus_status     | Returns full `meta_locus` snapshot          |
| Accept entry     | move.accept_entry     | Sets `accepted=true` (one-way)              |
| Set containment  | move.set_containment  | Sets `containment` under invariants         |
| Enqueue review   | move.open_fracture    | Adds id to `review_queue` (dedup)           |
| Dequeue review   | move.close_review     | Removes id; if queue empty → containment=F  |
| Append ledger    | move.record_ledger    | Appends entry to `ledger_buffer`            |

All write operations validate against invariants and fail-closed on violations.

---

## Failure Modes (errors)

| Condition                               | Emission                                     |
| --------------------------------------- | -------------------------------------------- |
| Attempt to reset `accepted` true → false| `tool.error { code: "E_INVARIANT" }`        |
| Enable `containment` when queue empty   | `tool.error { code: "E_PRECONDITION" }`      |
| Invalid `review_queue` item type        | `tool.error { code: "E_INVARIANT" }`         |
| Ledger append when buffer full          | `tool.error { code: "E_QUOTA" }`             |

---

## Examples

**1) Entry gate accepted**  
 ```yaml
tool.call:
  id: "move.accept_entry"
  payload: {}
 # → meta_locus.accepted == true
````

**2) Opening a fracture**

```yaml
tool.call:
  id: "move.open_fracture"
  payload: { fracture_id: "F1234" }
# → review_queue:["F1234"]; containment unchanged
```

**3) Recording a ledger entry**

```yaml
tool.call:
  id: "move.record_ledger"
  payload:
    entry_id: "uuid-abc"
    ts: "2025-08-26T15:10:00Z"
    type: "artifact"
    ref:  "#inline:artifact123"
```
---

## Notes & References

* Entry gate and gating logic: `10_entry_gate.md`  
* Moves & lenses: `30_lenses.md`, `35_micromoves.md`  
* Policy & quota: `90_policy.md`  
* Recap spec (reads state): `50_recap_spec.md`  
---
