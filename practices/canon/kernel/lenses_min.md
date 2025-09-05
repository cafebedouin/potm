---
id: potm.kernel.lenses_min.v1
title: "lenses_min"
display_title: "Lenses — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal, read-only lens set for the microkernel. Each lens is schema-bound
  to JSON files under runtime/spec/. Plain prose is inert; adapters translate
  to structured calls per router.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, lenses, minimal]
author: practitioner
license: CC0-1.0
---

# Lenses — Minimal Contract

**Scope.** The kernel executes only structured `lens.*` calls. Unknown ids fail-closed.
Payloads and results MUST conform to the referenced JSON Schemas (strict, with
`additionalProperties:false`). Lenses are read-only (no state mutation).

## Catalog (minimal)

| id     | Purpose                               | Baseline payload schema      | Min overlay (microkernel)         |
| ------ | ------------------------------------- | ---------------------------- | --------------------------------- |
| define | Disambiguate key terms                | `potm.kernel.lens.define.payload.v1` | `potm.kernel.lens.define.min.v1` |
| check  | Test a single key assumption          | `potm.kernel.lens.check.payload.v1`  | `potm.kernel.lens.check.min.v1`  |
| trace  | Show a short reasoning chain (2–4)    | `potm.kernel.lens.trace.payload.v1`  | `potm.kernel.lens.trace.min.v1`  |
| refuse | Decline safely with one forward route | `potm.kernel.lens.refuse.payload.v1` | `potm.kernel.lens.refuse.min.v1` |

Note: Baseline schema retained at `potm.kernel.lens.trace.payload.v1` for extended/ use.

## Invocation (router contract)

- Namespace: `lens.*` (allow-listed).
- Latency validator runs before tool execution.
- Invalid payload → `tool.error{ code:"E_PAYLOAD" }`. Unknown id → `E_NAMESPACE`.

---

## Schemas (by reference)

> Prefer direct reuse of existing schemas in `runtime/schema/`.  
> If the existing schema is broader than microkernel caps, use an **overlay wrapper** located in `runtime/spec/min/` that narrows fields via `allOf`.

### `lens.define`
- **Payload schema:** `$id` `potm.kernel.lens.define.payload.v1`
- **Min overlay:**    `$id` `potm.kernel.lens.define.min.v1` 

### `lens.check`
- **Payload schema:** `$id` `potm.kernel.lens.check.payload.v1` 
- **Min overlay:**    `$id` `potm.kernel.lens.check.min.v1` 

### `lens.trace`
- **Payload schema:** `$id` `potm.kernel.lens.trace.payload.v1` 
- **Min overlay:**    `$id` `potm.kernel.lens.trace.min.v1` 

### `lens.refuse`
- **Payload schema:** `$id` `potm.kernel.lens.refuse.payload.v1`
- **Min overlay:**    `$id` `potm.kernel.lens.refuse.min.v1` 

---

## Failure Modes

| condition                 | emission code  |
|--------------------------|----------------|
| Invalid payload          | `E_PAYLOAD`    |
| Unknown lens id          | `E_NAMESPACE`  |
| Attempt to mutate state  | `E_INVARIANT`  |

---

## Registration (tool index)

Register only these four ids under `lens.*` in `runtime/spec/tool.index.json`.  
If you use the **min overlays**, point the router’s per-tool schema pointers at the **min** files; otherwise point them at the baseline files.

## Notes on versioning

- Keep `$id` stable; bump only when changing semantics or caps.  
- Prefer **overlay min-files** to forking the baseline schemas; it keeps the “truth” centralized and the microkernel constraints explicit.  
- If a baseline schema is already narrow enough, skip overlays and point directly to it.
