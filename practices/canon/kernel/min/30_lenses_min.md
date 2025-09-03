---
id: potm.kernel.lenses_min.v1_6_dev
title: "30_lenses_min"
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

| id     | Purpose                               | Baseline schema (kept)    | Min overlay (microkernel)         | Example (microkernel)                  |
| ------ | ------------------------------------- | ------------------------- | --------------------------------- | -------------------------------------- |
| define | Disambiguate key terms                | `potm.kernel.lens.define.v1` | `potm.kernel.lens.define.min.v1` | `runtime/examples/lens_define_invoke.min.json` |
| check  | Test a single key assumption          | `potm.kernel.lens.check.v1`  | `potm.kernel.lens.check.min.v1`  | `runtime/examples/lens_check_invoke.min.json`  |
| trace  | Show a short reasoning chain (2–4)    | `potm.kernel.lens.trace.v1`  | `potm.kernel.lens.trace.min.v1`  | `runtime/examples/lens_trace_invoke.min.json`  |
| refuse | Decline safely with one forward route | `potm.kernel.lens.refuse.v1` | `potm.kernel.lens.refuse.min.v1` | `runtime/examples/lens_refuse_invoke.min.json` |

Note: Baseline schema retained at potm.kernel.lens.trace.v1 for extended/ use.

## Invocation (router contract)

- Namespace: `lens.*` (allow-listed).
- Latency validator runs before tool execution.
- Invalid payload → `tool.error{ code:"E_PAYLOAD" }`. Unknown id → `E_NAMESPACE`.

---

## Schemas (by reference)

> Prefer direct reuse of existing schemas in `runtime/schema/`.  
> If the existing schema is broader than microkernel caps, use an **overlay wrapper** located in `runtime/schema/min/` that narrows fields via `allOf`.

### `lens.define`

- **Payload schema:** `runtime/spec/lens.define_payload.json`
- **Result schema:**  `runtime/spec/lens.define_result.json`

> If you need tighter caps than the existing schema, add:
>
> `runtime/spec/min/lens.define_payload.min.json`
> ```json
> {
>   "$id": "runtime/spec/min/lens.define_payload.min.json",
>   "allOf": [
>     { "$ref": "../lens.define_payload.json" },
>     {
>       "type": "object",
>       "properties": {
>         "terms": { "minItems": 1, "maxItems": 6 }
>       },
>       "additionalProperties": false
>     }
>   ]
> }
> ```
> `runtime/spec/min/lens.define_result.min.json` similarly narrows `definitions` length, etc.

### `lens.check`

- **Payload schema:** `runtime/spec/lens.check_payload.json`
- **Result schema:**  `runtime/spec/lens.check_result.json`

> Optional overlay (if needed):
>
> `runtime/spec/min/lens.check_payload.min.json`
> ```json
> {
>   "$id": "runtime/spec/min/lens.check_payload.min.json",
>   "allOf": [
>     { "$ref": "../lens.check_payload.json" },
>     {
>       "type": "object",
>       "properties": {
>         "assumption": { "minLength": 3, "maxLength": 256 },
>         "method": { "enum": ["contrast","example","edge","proxy","other"] }
>       },
>       "additionalProperties": false
>     }
>   ]
> }
> ```

### `lens.trace`

- **Payload schema:** `runtime/spec/lens.trace_payload.json`
- **Result schema:**  `runtime/spec/lens.trace_result.json`

> Optional overlay:
>
> `runtime/spec/min/lens.trace_payload.min.json`
> ```json
> {
>   "$id": "runtime/spec/min/lens.trace_payload.min.json",
>   "allOf": [
>     { "$ref": "../lens.trace_payload.json" },
>     {
>       "type": "object",
>       "properties": { "steps": { "minimum": 2, "maximum": 4 } },
>       "additionalProperties": false
>     }
>   ]
> }
> ```

### `lens.refuse`

- **Payload schema:** `runtime/spec/lens.refuse_payload.json`
- **Result schema:**  `runtime/spec/lens.refuse_result.json`

> Optional overlay to enforce microkernel doctrine “one forward path” and reason enums:
>
> `runtime/spec/min/lens.refuse_payload.min.json`
> ```json
> {
>   "$id": "runtime/spec/min/lens.refuse_payload.min.json",
>   "allOf": [
>     { "$ref": "../lens.refuse_payload.json" },
>     {
>       "type": "object",
>       "required": ["reason","forward_route"],
>       "properties": {
>         "reason": {
>           "enum": [
>             "safety_risk","privacy_risk","policy_block",
>             "unsupported_scope","insufficient_info","other"
>           ]
>         },
>         "forward_route": {
>           "type": "object",
>           "required": ["label","suggestion"],
>           "additionalProperties": false
>         }
>       },
>       "additionalProperties": false
>     }
>   ]
> }
> ```

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

