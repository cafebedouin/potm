---
id: potm.kernel.state_min.v1_6_dev
title: "70_state_min"
display_title: "State — Minimal Session State"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal, session-local state for the microkernel. Defines `meta_locus`,
  `ledger_buffer`, and `fracture_log` with tight invariants. No background I/O;
  all reads/writes occur only through registered kernel tools.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, state, minimal]
author: practitioner
license: CC0-1.0
---

# State — Minimal Session State

## 0) Scope

- **Session-local only**; no persistence between sessions and no filesystem/network I/O. :contentReference[oaicite:0]{index=0}  
- Tools may **read/write state only via explicit kernel tools** (lenses are read-only). :contentReference[oaicite:1]{index=1}  
- The **fracture queue lives in `meta_locus.review_queue`**; full entries are stored in a `fracture_log` map. :contentReference[oaicite:2]{index=2}

---

## 1) Components

1) **meta_locus** — supervisory flags + review queue  
2) **ledger_buffer** — chronological in-memory ledger  
3) **fracture_log** — map of fracture entries keyed by `fracture_id`

> Minimality note: the microkernel **removes `mode_profile`** from `meta_locus` and keeps only `latency_mode`. (Your prior state kept both; we’re simplifying while preserving latency enforcement.) :contentReference[oaicite:3]{index=3}

---

## 2) `meta_locus` (supervisory)

**Shape (conceptual):**
```json
{
  "accepted": true,
  "containment": false,
  "review_queue": [],
  "latency_mode": "standard"
}
````

**Initial values:** `accepted:true`, `containment:false`, `review_queue:[]`, `latency_mode:"standard"`.&#x20;

**Invariants (hard):**

* `accepted` defaults **true**; `[KERNEL_EXIT]` may flip it **false**.&#x20;
* `containment` **may enable only if** `review_queue.length > 0`; it **auto-disables** when the queue becomes empty.&#x20;
* `latency_mode ∈ {lite, standard, strict}`; enforced by the latency validator and policy caps. &#x20;

**Queue semantics:** `review_queue` stores **ids only**; full entries live in `fracture_log`.&#x20;

**Containment gating:** while `containment==true`, only the containment-safe tools are allowed by the router (guardian.trigger, move.fracture, lens.refuse).&#x20;

---

## 3) `ledger_buffer` (in-memory ledger)

* An **in-memory array** of lightweight ledger entries (latency breaches, guardian events, fracture/containment transitions, etc.). &#x20;
* **Capacity** is enforced by `policy.cap.ledger_max`. When exceeded → `E_QUOTA`. &#x20;
* Canonical event schemas live under `runtime/spec/ledger.*.json` (e.g., `ledger.latency_breach.json`, `ledger.guardian_event.json`). See runtime/examples for concrete rows.

---

## 4) `fracture_log` (map)

* Session-local **map**: `{ [fracture_id]: fracture_entry }`.&#x20;
* Each entry conforms to `runtime/schema/fracture_entry.json`.&#x20;

---

## 5) Who can read/write?

| Operation                       | Tool (kernel)          | Effect on state                                                     |
| ------------------------------- | ---------------------- | ------------------------------------------------------------------- |
| Read meta\_locus / latency view | lenses (read-only)     | Snapshot only; no mutation (e.g., latency status lens).             |
| Toggle containment (hard route) | guardian.trigger(hard) | May set `containment=true` (only if queue non-empty).               |
| Open/append fracture            | move.fracture          | Append ledger row; add entry to `fracture_log`; enqueue id.         |
| Record latency breach           | latency.validator      | Append `latency_breach` ledger entry; no other mutation.            |
| General ledger append           | (none in microkernel)  | (Policy/diagnostic writers live in `extended/`; kernel is minimal.) |

> Your fuller state doc enumerated additional writers like `move.set_containment`, `move.open_fracture`, `move.review_fracture`, etc. In the **microkernel**, we limit writers to the minimal set above; richer lifecycle tools live under `extended/`.&#x20;

---

## 6) Failure modes (router-aligned)

| condition                                  | emission code           |
| ------------------------------------------ | ----------------------- |
| invalid or missing `latency_mode`          | `E_LATENCY_MODE`        |
| latency contract invariant violation       | `E_LATENCY_INVARIANT`   |
| observed latency above ceiling (warning)   | `W_LATENCY_BREACH`      |
| quota exceeded on ledger append            | `E_QUOTA`               |
| mutation attempted during containment gate | `E_CONTAINMENT_BLOCKED` |

(Aligned to your prior state/policy tables and router behavior.) &#x20;

---

## 7) JSON Schemas & examples (references)

* **Router envelope/emissions:** `runtime/spec/router_envelope.json`, `runtime/spec/router_emission.json`
* **Latency validator:** `runtime/spec/latency.validator_payload.json`, `runtime/spec/latency.validator_result.json`&#x20;
* **Ledger events:** `runtime/spec/ledger.latency_breach.json`, `runtime/spec/ledger.guardian_event.json`, `runtime/spec/ledger.fracture_event.json` (see also runtime/examples)&#x20;
* **Fracture entry:** `runtime/schema/fracture_entry.json`&#x20;
* **Examples:** `runtime/examples/state_meta_locus.json`, `state_log_latency_breach.json`, `fracture_open.json`, `fracture_open_ledger.json` &#x20;

---

## 8) Notes & exclusions (microkernel deltas)

* **Removed from kernel:** `mode_profile` and its gates/canary machinery; these live under `extended/modes/` and `extended/gates/`.&#x20;
* **Guardian + Containment:** containment is diagnostic, not punitive; it restricts routing until the fracture queue is cleared via extended tools.&#x20;
* **Export policy:** kernel state never exports; export targets (if any) are governed in `extended/policy/`.

