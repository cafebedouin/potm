---
$id: potm.kernel.micromoves_min.v1
title: "micromoves_min"
display_title: "Micromoves — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal micromove set for the microkernel. Write-light, schema-bound actions
  that enforce routing hygiene and safe escalation. Only the three moves below
  are registered in the kernel; all others live in extended/.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, micromoves, minimal]
author: practitioner
license: CC0-1.0
---

# Micromoves — Minimal Contract

**Scope.** Only `move.align_scan`, `move.drift_check`, and `move.fracture`
are available in the kernel. All payloads/results MUST conform to the JSON
Schemas referenced below (`additionalProperties:false` enforced).

**Side-effects.**
- `align_scan`, `drift_check`: *read-only* (no state mutation).
- `fracture`: may write **ledger** and **fracture queue** (open a fracture),
  and may flip `meta_locus.containment=true` when invoked via guardian.hard.

**Router order.** Latency validator runs *before* any move. Unknown ids fail closed.

---

## Catalog (minimal)

| id              | purpose                                              | payload schema                                   | result schema                                    |
|-----------------|------------------------------------------------------|--------------------------------------------------|--------------------------------------------------|
| move.align_scan | Check request → beacons/router fit; emit guidance    | `runtime/spec/move.align_scan_payload.json`      | `runtime/spec/move.align_scan_result.json`       |
| move.drift_check| Detect likely context/protocol drift (lightweight)   | `runtime/spec/move.drift_check_payload.json`     | `runtime/spec/move.drift_check_result.json`      |
| move.fracture   | Open/record a fracture and enqueue for review        | `runtime/spec/move.fracture_payload.json`        | `runtime/spec/move.fracture_result.json`         |

> If any baseline schema is broader than desired, add overlays under
> `runtime/spec/min/…` and point the tool index at those instead.

---

## Semantics

### `move.align_scan`
- **Intent.** Quick structural fit check: envelope, namespace, beacon touchpoints.
- **Inputs (payload).** See schema; typical fields include a short `question`
  and an optional `context_hint`.
- **Outputs (result).** A compact list of notes (`fit`, `risk`, `next_hint`).
- **Invariants.** No mutation; purely advisory. Emits nothing to ledger.

### `move.drift_check`
- **Intent.** Cheap drift heuristic (e.g., mismatch between user ask and
  current `meta_locus` or kernel scope).
- **Inputs/Outputs.** As per schemas; may return `status: ok|watch|drift`.
- **Invariants.** No mutation; purely advisory. Router/guardian may *read* its
  result to decide on soft warnings.

### `move.fracture`
- **Intent.** Open a new fracture record when a kernel invariant or beacon is
  violated (or credibly threatened), enqueue for later review/repair.
- **Inputs.** Minimal description (`reason`, `beacon_ref`, optional `evidence`).
- **Outputs.** `fracture_id`, `queued: true`, and a ledger emission.
- **Side-effects.** Append `ledger.fracture_event`; enqueue fracture; if invoked
  by `guardian.trigger(level:"hard")`, set `meta_locus.containment=true`.

---

## Failure modes (common)

| condition                 | emission code   |
|--------------------------|-----------------|
| Invalid payload          | `E_PAYLOAD`     |
| Unknown move id          | `E_NAMESPACE`   |
| Forbidden mutation       | `E_INVARIANT`   |

---

## Registration (tool index)

Register only these three ids in `runtime/spec/tool.index.json` under `move.*`.
Point each entry’s `payload_schema`/`result_schema` to the paths in the table
above (or to `runtime/spec/min/...` if you add overlays).

> All other moves currently in `runtime/spec` (e.g., `move.contrast`,
> `move.quick_ref`, `move.zone_check`, `move.sandbox`, `move.open_fracture`,
> `move.set_*`, etc.) should be *unregistered from kernel* and re-registered
> under `extended/` packages.

---

## Annex

- Beacons (for `beacon_ref` in `move.fracture`): `kernel/20_beacons.md`
- Guardian trigger contract: `potm.kernel.guardian.trigger.payload.v1`,
  `potm.kernel.guardian.trigger.result.v1`
- Latency validator: `potm.kernel.latency.validator.payload.v1`,
  `potm.kernel.latency.validator.result.v1`
