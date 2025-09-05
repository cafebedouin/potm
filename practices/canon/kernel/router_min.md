---
id: potm.kernel.router_min.v1
title: "router_min"
display_title: "Router — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal, allow-listed router for the microkernel. Validates the envelope,
  enforces namespace allow-list, runs the latency validator first, validates
  payloads against registered schemas, and emits typed results/errors. No
  hidden I/O. Unknown tools fail-closed.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, router, minimal]
author: practitioner
license: CC0-1.0
---

# Router — Minimal Contract

## 0) Scope & invariants

- **Allow-listed namespaces (kernel only):**
  - `menu.*`   → `surface`
  - `lens.*`   → `define`, `check`, `trace`, `refuse`
  - `move.*`   → `align_scan`, `drift_check`, `fracture`
  - `guardian.*` → `trigger`
- **Not routed in kernel:** `closure.*`, `recap.*`, `externalist.*`, `policy.*`, `glyph.*`,
  `mode_profile.*`, `sentinel.*` (these belong in `extended/`).
- **No implicit tools.** Only ids present in the **tool index** are callable.
- **No external I/O.** All effects are session-local; kernel does not call the network.
- **Fail-closed.** Unknown namespace/id → error; invalid payload → error; containment may block.
- Before emitting adapter-defined menu surfaces, call:
  `tool.validate: potm.runtime.menu.surface_validator.v1`

---

## 1) Wire format

- **Envelope validation:** `potm.kernel.router.envelope.v1`
- **Emission (success) format:** `potm.kernel.router.emission.v1`
- **Emission (error) format:** `potm.kernel.router.error.v1`

The router accepts only properly-typed envelopes and always returns a typed emission.

---

## 2) Dispatch order (hard invariant)

1. **Validate envelope** against `potm.kernel.router.envelope.v1`.
2. **Parse tool id** → `(namespace, name)` and check against **allow-list**.
3. **Idempotency check:**
   - Require `request_id` (from envelope).
   - Canonicalization: use JSON Canonicalization Scheme (JCS) to ensure deterministic digests.
   - If `(request_id, digest)` seen → return cached emission.
   - If `request_id` reuse with different `digest` → error `E_IDEMPOTENCY`.
4. If tool == "menu.surface":
   - Route to `potm.adapter.entry_menu.v1_6_dev`.
   - Validate output against `potm.runtime.menu.surface_validator.v1`.
   - On success:
     - Emit `ledger.glyph_event{ event:"menu_invoked" }`.
   - On mismatch:
     - Emit error `E_SURFACE_VIOLATION`.
     - Emit `ledger.guardian_event{ event:"surface_mismatch", details:"entry menu drift" }`.
     - Block emission (fail-closed).
5. **Containment gate (read-only):**
   - If `meta_locus.containment==true`, allow only:
     - `guardian.trigger` (any level),
     - `move.fracture` (close or append),
     - `lens.refuse`.
   - Otherwise emit `E_CONTAINMENT_BLOCKED`.
6. **Latency validator (first validator):**
   - Invoke with `potm.kernel.latency.validator.payload.v1`,
     receive `potm.kernel.latency.validator.result.v1`.
   - If result `error` → emit `E_LATENCY_INVARIANT` and halt.
   - If result `warn` → attach `W_LATENCY_BREACH` to emission context.
7. **Lookup tool** in `runtime/spec/tool.index.json`:
   - Must map `id` → `{payload_schema, result_schema}` file refs.
   - If missing → `E_TOOL_NOT_FOUND`.
8. **Validate payload** against tool’s `payload_schema`.
   - On failure → `E_PAYLOAD`.
9. **Execute tool** (pure or declared side-effects only).
   - **No network / external I/O** in kernel tools.
10. **Validate result** against tool’s `result_schema`.
11. **Emit** `router_emission.json` with `result`, plus any attached warnings.

---

## 3) Registration (tool index)

**File:** `runtime/spec/tool.index.json` (`id`: `potm.kernel.tool.index.v1`)

Register **only** these ids for the kernel:

```json
{
  "tools": [
    { "id": "lens.define",  "payload_schema": "runtime/spec/min/lens.define.min.v1.json",  "result_schema": "runtime/spec/router_emission.json#/$defs/lens.define.result" },
    { "id": "lens.check",   "payload_schema": "runtime/spec/min/lens.check.min.v1.json",   "result_schema": "runtime/spec/router_emission.json#/$defs/lens.check.result" },
    { "id": "lens.trace",   "payload_schema": "runtime/spec/min/lens.trace.min.v1.json",   "result_schema": "runtime/spec/router_emission.json#/$defs/lens.trace.result" },
    { "id": "lens.refuse",  "payload_schema": "runtime/spec/min/lens.refuse.min.v1.json",  "result_schema": "runtime/spec/router_emission.json#/$defs/lens.refuse.result" },
    { "id": "move.align_scan", "payload_schema": "potm.kernel.move.align_scan.payload.v1", "result_schema": "potm.kernel.move.align_scan.result.v1" },
    { "id": "move.drift_check","payload_schema": "potm.kernel.move.drift_check.payload.v1","result_schema": "potm.kernel.move.drift_check.result.v1" },
    { "id": "move.fracture",   "payload_schema": "potm.kernel.move.fracture.payload.v1",   "result_schema": "potm.kernel.move.fracture.result.v1" },
    { "id": "guardian.trigger","payload_schema": "potm.kernel.guardian.trigger.payload.v1","result_schema": "potm.kernel.guardian.trigger.result.v1" }
  ]
}
````

> Notes:
>
> * Lenses point to your **min overlays** under `runtime/schema/min/…`.
> * Moves + guardian already have payload/result schemas living under `runtime/spec/…`.
> * If you prefer, you can also define per-lens result subschemas in `router_emission.json` (`$defs`) as shown above; otherwise point to standalone result schemas if/when you add them.

---

## 4) Error & warning codes

| code                    | when it fires                                        |
| ----------------------- | ---------------------------------------------------- |
| `E_NAMESPACE`           | Namespace not in allow-list                          |
| `E_TOOL_NOT_FOUND`      | Id not present in tool index                         |
| `E_PAYLOAD`             | Payload fails JSON Schema validation                 |
| `E_RESULT`              | Result fails JSON Schema validation                  |
| `E_IDEMPOTENCY`         | Reused `request_id` with different payload digest    |
| `E_CONTAINMENT_BLOCKED` | Tool not permitted while in containment              |
| `E_LATENCY_INVARIANT`   | Latency validator reports hard breach                |
| `W_LATENCY_BREACH`      | Latency validator reports soft breach (warning only) |
| `E_SURFACE_VIOLATION`   | Menu output did not match adapter + validator       |
| `E_AGREEMENT_DRIFT`     | Acceptance not bound at boot (only prompted later) |


All errors/warnings are emitted using `router_error.json` / `router_emission.json`.

---

## 5) Security & side-effects

* **Pure by default.** Lenses are read-only.
* **Limited writers:** `move.fracture` may append to `ledger.fracture_event` and
  enqueue a fracture; `guardian.trigger(level:"hard")` may set
  `meta_locus.containment=true`. No other mutation in kernel tools.
  * `menu.surface` may emit `ledger.glyph_event{ event:"menu_invoked" }`.
* On violation, it may emit `ledger.guardian_event{ event:"surface_mismatch" }`.

* **No export.** Kernel does not expose export targets; see `policy.targets.json` in `extended/` if needed.

---

## 6) Pseudocode (reference)

```pseudo
function route(envelope):
  assert validate(envelope, "potm.kernel.router.envelope.v1")

  (ns, name) = split(envelope.id)
  if ns not in {"lens","move","guardian"}: return err(E_NAMESPACE)

  rid = require(envelope.request_id)
  dg  = sha256(canonical(envelope.id, envelope.payload))
  if cache.has(rid):
    if cache.get(rid).digest != dg: return err(E_IDEMPOTENCY)
    else return cache.get(rid).emission

  if state.meta_locus.containment:
    if not allowed_in_containment(envelope.id):
      return err(E_CONTAINMENT_BLOCKED)

  lat = call("latency.validator", observed_latency=envelope.observed_latency_ms)
  if lat.error: return err(E_LATENCY_INVARIANT)
  warn_if(lat.warn, W_LATENCY_BREACH)

  spec = tool_index.lookup(envelope.id)
  if not spec: return err(E_TOOL_NOT_FOUND)

  assert validate(envelope.payload, spec.payload_schema)

  result = execute(envelope.id, envelope.payload, state)

  assert validate(result, spec.result_schema)

  emission = wrap_success(result, warnings)
  cache.store(rid, digest=dg, emission)
  return emission
```

---

## 7) Containment allow-list

While `meta_locus.containment==true`, only the following ids are permitted:

* `guardian.trigger` (soft/hard)
* `move.fracture` (open/append/close per your spec)
* `lens.refuse` (for safe declining + forward route)

Everything else yields `E_CONTAINMENT_BLOCKED`.

---

## 8) What moved to `extended/`

* Recap spec/validator, closure archive, spotcheck/sentinel, mode profiles,
  escalation gates, externalist/mirror, policy enforcement/query/report,
  glyphs, and any additional lenses/moves not listed above.
```
