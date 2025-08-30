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

Holds session flags and the fracture review queue used for gating and diagnostics.  

See:  
- `runtime/examples/state_meta_locus.json`  
- `runtime/examples/state_accept_entry.json`  
- `runtime/examples/state_open_fracture.json`

Notes:  
- `latency_mode` is enforced specifically by the latency validator (`85_latency_validator.md`).  
- `mode_profile` is the higher-level envelope: it governs validator strictness, escalation gates, and micro-canary sensitivity in addition to latency ceilings.  
- In most cases, `mode_profile` and `latency_mode` will share the same value, but they are kept distinct to preserve clarity of responsibility.  

- additionalProperties: false  
- initial state:
  - accepted: false  
  - containment: false  
  - review_queue: []            # array of fractureId strings only  
  - latency_mode: standard  
  - mode_profile: standard  

- review_queue semantics:
  - Stores fractureId strings only (lightweight queue).  
  - Full entries are kept in a session-local `fracture_log` map keyed by fractureId.  
  - Fracture entries conform to `runtime/schema/fracture_entry.json`.  
  - See examples:
    - open: `runtime/examples/fracture_open.json` (invokes `move.open_fracture`)
    - review: `runtime/examples/fracture_review.json` (invokes `move.review_fracture`)
    - resolve: `runtime/examples/fracture_resolve.json` (invokes `move.close_review`)

#### Invariants

- `accepted` may transition only false → true.  
- `containment` may enable only if `len(review_queue) > 0`; auto-disable when queue becomes empty.  
- `latency_mode` must always be one of {lite, standard, strict}; default is `standard`.  

---

### ledger_buffer

A chronological, in-memory array of lightweight ledger entries recording artifacts, moves, and optional exports.  

See:  
- `runtime/examples/state_ledger_buffer.json`  
- `runtime/examples/state_record_latency_breach.json`  
- `runtime/examples/state_set_latency_mode.json`  
- `runtime/examples/state_log_latency_breach.json`  
- `runtime/examples/state_set_mode_profile.json`  
- `runtime/examples/state_record_mode_profile_change.json`  
- `runtime/examples/state_record_canary_report.json`  
- `runtime/examples/state_escalation_tier2.json`  
- `runtime/examples/state_escalation_tier3_fracture.json`  
- `runtime/examples/state_escalation_tier4_containment.json`  
- `runtime/examples/state_escalation_quota_exceeded.json`

- additionalProperties: false  
- max length: session-cap (see `90_policy.md`)  
- entries expire only at session end  

---

### fracture_log

Session-local map of fracture entries keyed by `fracture_id`.  
All entries conform to `runtime/schema/fracture_entry.json`.  
The `review_queue` stores ids only; full entries live here.  

---

## Read & Write Access (tools)

Tools interact with state only via these contracts:

| Operation          | Tool namespace            | Effect                                                         |
| ------------------ | ------------------------- | -------------------------------------------------------------- |
| Read meta_locus    | lens.locus_status         | Returns full `meta_locus` snapshot                             |
| Read latency state | lens.latency_status       | Returns current `latency_mode` and most recent breach metadata |
| Accept entry       | move.accept_entry         | Sets `accepted=true` (one-way)                                 |
| Set containment    | move.set_containment      | Sets `containment` under invariants and policy cap             |
| Set latency mode   | move.set_latency_mode     | Sets `latency_mode` under invariants                           |
| Enqueue review     | move.open_fracture        | Records entry in `fracture_log`; appends fractureId to `review_queue` |
| Mark review        | move.review_fracture      | Sets entry `status: review` in `fracture_log`                  |
| Dequeue review     | move.close_review         | Sets `status: resolved` in `fracture_log`, removes id; auto-disables containment if queue empty |
| Append ledger      | move.record_ledger        | Appends entry to `ledger_buffer`                               |
| Log latency breach | move.log_latency_breach   | Appends structured `latency_breach` entry to `ledger_buffer`   |

All write operations validate against invariants and fail-closed on violations.

---

## Behavior (latency_status lens)

**mode** → always returns the current value of `meta_locus.latency_mode`.  

**last_breach** →  
- `null` if no breaches recorded  
- otherwise returns the most recent `latency_breach` entry in `ledger_buffer`, including:  
  - `ts` (timestamp)  
  - `observed_latency`  
  - `ceiling`  
  - `severity` (`warning|error`)  

See:  
- `runtime/examples/state_log_latency_breach.json`

---

## Containment gating

When `meta_locus.containment=true`, only containment-mode tools are available  
(see `76_containment_mode.md`). Non-containment mutations fail-closed.  
Containment integrates with Tier 3/4 escalation and the fracture queue; review  
continues under containment until resolved or exited via grace path.

## Ledger entries (specs)

- Fracture events: `runtime/spec/ledger.fracture_event.json`  
- Containment events: `runtime/spec/ledger.containment_event.json`  
- Glyph events: `runtime/spec/ledger.glyph_event.json`  
- Guardian events: `runtime/spec/ledger.guardian_event.json`  

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
| Invalid `mode_profile` not in {lite, standard, strict} | `tool.error { code: "E_MODE_PROFILE" }`     |
| Drift (mode_profile vs latency_mode mismatch)  | `tool.error { code: "E_INVARIANT" }`        |
| Ledger empty / no breaches                     | `{ "mode": <current>, "last_breach": null }` |
| Invalid `signal` not in {schema_near_miss, unusual_latency, drift_pattern, unknown} | `tool.error { code: "E_CANARY_SIGNAL" }`   |
| Invalid `severity` not in {warning, error}                                          | `tool.error { code: "E_CANARY_SEVERITY" }` |
| Missing required field in canary.report payload                                     | `tool.error { code: "E_PAYLOAD" }`         |
| Canary ledger quota exceeded                    | `tool.error { code: "E_CANARY_QUOTA" }`      |
| Invalid `tier` not in {1,2,3,4}                 | `tool.error { code: "E_ESCALATION_TIER" }`   |
| Invalid `action` not in {none, escalate_profile, fracture_trigger, containment} | `tool.error { code: "E_ESCALATION_ACTION" }` |
| Source not in {validator, latency, canary, policy, other} | `tool.error { code: "E_ESCALATION_SOURCE" }` |
| Escalation quota exceeded (too many escalation_event entries) | `tool.error { code: "E_ESCALATION_QUOTA" }`  |
| Escalation ledger empty / no events             | { "last_source": null, "last_tier": null, "last_action": null, "mode_profile": <current>, "last_change": null, "history_count": 0 } |
| Invalid escalation record shape (schema drift)  | `tool.error { code: "E_ESCALATION_RECORD" }`  |

---

## Examples

Examples are externalized. See canonical instances in `runtime/examples/`:

- `state_meta_locus.json` — default snapshot  
- `state_accept_entry.json` — entry gate accepted  
- `fracture_open.json` — fracture created via move; queued  
- `fracture_review.json` — fracture moved to review  
- `fracture_resolve.json` — fracture resolved and dequeued  
 - `fracture_open_result.json` — confirmation of queue (status: queued)  
 - `fracture_review_result.json` — confirmation of review (status: review)  
 - `fracture_resolve_result.json` — confirmation of resolution (status: resolved)  
- `state_record_latency_breach.json` — latency breach entry  
- `state_set_latency_mode.json` — switch to lite  
- `state_log_latency_breach.json` — breach logged + lens output  
- `state_set_mode_profile.json` — profile manual override  
- `state_read_mode_profile.json` — lens output for profile  
- `state_record_mode_profile_change.json` — profile change event  
- `state_record_canary_report.json` — canary emission  
- `state_canary_status.json` — last canary status lens  
- `state_escalation_tier2.json` — Tier 2 escalation  
- `state_escalation_tier3_fracture.json` — Tier 3 escalation  
- `state_escalation_tier4_containment.json` — Tier 4 escalation  
- `state_escalation_status.json` — escalation status lens  
- `state_escalation_quota_exceeded.json` — quota exceeded case  
- `containment_invoke.json` — enter containment (move.set_containment)  
- `containment_exit.json` — exit containment (move.set_containment)  
 - `containment_enter_result.json` — confirmation of containment entry  
- `containment_exit_result.json` — confirmation of containment exit  

### Glyph Examples

- `glyph_invoke.json` — invoke a glyph  
- `glyph_result.json` — glyph result payload  
- `glyph_invoke_ledger.json` — ledger entry for glyph invoke  
- `glyph_result_ledger.json` — ledger entry for glyph result  
- `glyph_map_ledger.json` — ledger entry for resonance mapping  

### Lens Examples

- `lens_fracture_status.json` — snapshot of fracture queue & containment flag  

### Ledger Examples

- `fracture_open_ledger.json` — ledger entry for fracture open  
- `fracture_review_ledger.json` — ledger entry for fracture review  
- `fracture_resolve_ledger.json` — ledger entry for fracture resolve  
- `containment_enter_ledger.json` — ledger entry for containment enter  
- `containment_exit_ledger.json` — ledger entry for containment exit  
- `containment_abort_ledger.json` — ledger entry for containment abort  
 - `latency_breach_ledger.json` — ledger entry for latency breach  
 - `escalation_tier2_ledger.json` — ledger entry for Tier 2 escalation  
- `escalation_tier4_ledger.json` — ledger entry for Tier 4 escalation  

### Externalist Examples

- `externalist_invoke.json` — externalist invoke (diagnostic overlay)  
- `externalist_result.json` — externalist result with reframed question  
- `externalist_ledger.json` — ledger entry for externalist event  

### Guardian Examples

- `guardian_trigger_soft.json` — soft guardian trigger  
- `guardian_trigger_hard.json` — hard guardian trigger  
- `guardian_trigger_result.json` — result confirmation  
- `guardian_soft_ledger.json` — ledger entry for soft trigger  
- `guardian_hard_ledger.json` — ledger entry for hard trigger  

## Externalist moves (specs)

- externalist.invoke —  
  - payload: `runtime/spec/externalist.invoke_payload.json`  
  - result:  `runtime/spec/externalist.result.json`

---

## Fracture resources (diagnostics)

For practitioner diagnostics and review heuristics, see:  
- `extended/diagnostics/fracture/fracture_finder.md`  
- `extended/diagnostics/fracture/fracture_finder_playbook.md`  
- `extended/diagnostics/fracture/fracture_crosswalk.md`  
- `meta/fracture_meta`  

## Fracture moves (specs)

- move.open_fracture —  
  - payload: `runtime/spec/move.open_fracture_payload.json`  
  - result:  `runtime/spec/move.open_fracture_result.json`
- move.review_fracture —  
  - payload: `runtime/spec/move.review_fracture_payload.json`  
  - result:  `runtime/spec/move.review_fracture_result.json`
- move.close_review —  
  - payload: `runtime/spec/move.close_review_payload.json`  
  - result:  `runtime/spec/move.close_review_result.json`

## Containment moves (specs)

- move.set_containment —  
  - payload: `runtime/spec/move.set_containment_payload.json`  
  - result:  `runtime/spec/move.set_containment_result.json`
- containment.abort —  
  - payload: `runtime/spec/containment.abort_payload.json`  
  - result:  `runtime/spec/containment.abort_result.json`

---

### 🔑 Notes for practitioners

* `move.set_mode_profile` changes `meta_locus.mode_profile`, records timestamp + source.  
* `lens.mode_profile_status` is **read-only** — safe to call any time.  
* Default on entry is `"standard"` unless overridden in the handshake.  

---

## Notes & References

* Entry gate and gating logic: `10_entry_gate.md`  
* Moves & lenses: `30_lenses.md`, `35_micromoves.md`  
* Policy & quota: `90_policy.md`  
* Recap spec (reads state): `50_recap_spec.md`  
---
-## Glyph moves (specs)

- glyph.invoke —  
  - payload: `runtime/spec/glyph.invoke_payload.json`  
  - result:  `runtime/spec/glyph.result.json`
