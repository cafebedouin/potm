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
  containment:   true|false       # is containment mode enabled?
  review_queue:  []               # array of fracture ids pending review
  latency_mode:  lite|standard|strict  # current latency contract mode
  # derived (normative): fracture_active := (len(review_queue) > 0)
  # MUST NOT be stored; any read computes it from `review_queue`.
```

- additionalProperties: false  
- initial state:

  accepted: false
  containment: false
  review_queue: []
  latency_mode: standard   # default

#### Invariants

- `accepted` may transition only false → true.
- `containment` may enable only if `len(review_queue) > 0`; auto-disable when queue becomes empty.
- `latency_mode` must always be one of {lite, standard, strict}; default is `standard`.

### ledger_buffer

A chronological, in-memory array of lightweight ledger entries  
recording artifacts, moves, and optional exports.

```yaml
ledger_buffer:
  - entry_id: "<uuid>"
    ts: "2025-08-26T15:04:05Z"
    type: "move|artifact|export|latency_breach"
    ref: "<artifact_ref|null>"    # always allowed, often null for breach
    meta?:                        # optional metadata, depends on type
      tool_call?: { id: "...", payload: { ... } }     # for move records
      mode?: "lite|standard|strict"                   # for latency_breach
      observed_latency?: 5.3                          # in seconds
      ceiling?: 4.0                                   # in seconds
      severity?: "warning|error"                      # for latency_breach
```

- additionalProperties: false  
- max length: session-cap (see `90_policy.md`)  
- entries expire only at session end  

---

## Read & Write Access (tools)

Tools interact with state only via these contracts:

| Operation          | Tool namespace            | Effect                                                         |
| ------------------ | ------------------------- | -------------------------------------------------------------- |
| Read meta_locus    | lens.locus_status         | Returns full `meta_locus` snapshot                             |
| Read latency state | lens.latency_status       | Returns current `latency_mode` and most recent breach metadata |
| Accept entry       | move.accept_entry         | Sets `accepted=true` (one-way)                                 |
| Set containment    | move.set_containment      | Sets `containment` under invariants                            |
| Set latency mode   | move.set_latency_mode     | Sets `latency_mode` under invariants                           |
| Enqueue review     | move.open_fracture        | Adds id to `review_queue`                                      |
| Dequeue review     | move.close_review         | Removes id; auto-disables containment if queue empty           |
| Append ledger      | move.record_ledger        | Appends entry to `ledger_buffer`                               |
| Log latency breach | move.log_latency_breach   | Appends structured `latency_breach` entry to `ledger_buffer`   |

All write operations validate against invariants and fail-closed on violations.

## Behavior (latency_status lens)

**mode** → always returns the current value of `meta_locus.latency_mode`.  

**last_breach** →  
- `null` if no breaches recorded  
- otherwise returns the most recent `latency_breach` entry in `ledger_buffer`, including:  
  - `ts` (timestamp)  
  - `observed_latency`  
  - `ceiling`  
  - `severity` (`warning|error`)  

This lens does not modify state. Pure read.

---

## Failure Modes (errors)

| Condition                                      | Emission                                     |
| ---------------------------------------------- | -------------------------------------------- |
| Attempt to reset `accepted` true → false       | `tool.error { code: "E_INVARIANT" }`        |
| Enable `containment` when queue empty          | `tool.error { code: "E_PRECONDITION" }`      |
| Invalid `review_queue` item type               | `tool.error { code: "E_INVARIANT" }`         |
| Ledger append when buffer full                 | `tool.error { code: "E_QUOTA" }`             |
| Invalid `mode` not in {lite, standard, strict} | `tool.error { code: "E_LATENCY_MODE" }`      |
| Negative or non-numeric latency                | `tool.error { code: "E_PAYLOAD" }`           |
| Severity not in {warning, error}               | `tool.error { code: "E_LATENCY_INVARIANT" }` |
| `latency_mode` missing/invalid                 | `tool.error { code: "E_LATENCY_MODE" }`      |
| Ledger empty / no breaches                     | `{ "mode": <current>, "last_breach": null }` |

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
    entry_id: "<uuid>"
    ts: "2025-08-28T15:04:05Z"
    type: "latency_breach"
    ref: null
    meta:
      mode: "lite|standard|strict"
      observed_latency: 5.3   # in seconds
      ceiling: 4.0            # in seconds
      severity: "warning|error"
# → ledger_buffer += { type: "latency_breach", meta:{...} }
```

**4) Set latency mode***

```yaml
tool.call:
  id: "move.set_latency_mode"
  payload: { mode: "lite" }
# → meta_locus.latency_mode == "lite"
```

**5) Log latency breach**

```yaml
tool.call:
  id: "lens.latency_status"
  payload: {}
# → { "mode": "standard",
#      "last_breach": {
#         "ts": "2025-08-28T15:15:00Z",
#         "observed_latency": 7.1,
#         "ceiling": 6.0,
#         "severity": "warning"
#       } }
# → ledger_buffer += { type: "latency_breach", meta:{...} }
```

---

## Notes & References

* Entry gate and gating logic: `10_entry_gate.md`  
* Moves & lenses: `30_lenses.md`, `35_micromoves.md`  
* Policy & quota: `90_policy.md`  
* Recap spec (reads state): `50_recap_spec.md`  
---
