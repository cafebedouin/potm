---
id: potm.adapter.lens.v1_1
title: lens_adapter
type: strategy
lifecycle: canon
version: 1.1
status: active
stability: stable
summary: "Registers lens/micromove/metatool packs, mediates lens.invoke calls, and enforces surfacing rules."
tags: [adapter, lenses, extended]
author: practitioner
license: CC0-1.0
---

## Purpose
Bridge `router.api` to extension packs with strict schema checking and fail-closed refusals.  
Guarantee that all `lens.*` calls are both **ledgered** and **surfaced visibly** before subsequent model output.

---

## Procedure

1. **Catalog discovery**
   - On session start (or `menu` load), discover catalog under  
     `extended/lenses/catalog.v1.json`.
   - Validate each manifest against  
     `runtime/schema/lens_manifest.v1.json`.

2. **Registration**
   - Call `lens.register(manifest)`; on error, ledger and skip pack.

3. **Invocation**
   - On `lens.invoke` for `ex.lens.*`, resolve:
     - find pack that owns `lens_id`
     - load payload schema by `payload_schema_ref`
     - validate payload → if fail, emit `refusal:E_PAYLOAD`
     - execute deterministic template in the lens doc (no external I/O)
     - return `artifact|refusal`

4. **Listing**
   - On `id: lens.list`, return the validated catalog at  
     `runtime/spec/lens.catalog.v1.json` (surface + ledger).

---

## Failure Modes & Counters

- **F-MISSING-SCHEMA** → refusal `E_PAYLOAD` + hint to pack author  
- **F-UNKNOWN-LENS** → refusal `E_NAMESPACE` + suggest `menu` to list loaded lenses  
- **F-SAFETY-NOTE-REQ** → refusal if lens requires unmet preconditions  

---

## Surfacing Rule (invariant)

- After **every lens.* invocation**, the adapter must:
  1. Write a row to `ledger.lens_event.json`.
  2. Emit a preface block *before* any freeform output:

     ```
     [LENS: lens.edge]
     → payload: {…}
     → result: {…}
     ```

- If a model emits continuation text without this preface, it is a contract violation.

---

## Compound Lenses (adapter wiring)

Compound invocations use the `lens.compound.*` namespace and are executed entirely in the adapter by orchestrating kernel-safe lenses (`lens.define`, `lens.check`, `lens.trace`, `lens.refuse`).  
Compounds are declared under `extended/lenses/compounds/*/compound.manifest.json` and registered in `extended/lenses/catalog.v1.json`.

### Detection
- Detect compound calls by `id.startsWith("lens.compound.")`.
- Extract `name = id.split('.')[2]` (e.g., `relational`).
- Lookup manifest path in `extended/lenses/catalog.v1.json` → `compounds[]` entry with `id == "compound."+name`.

### Loading
- Load and parse the referenced `compound.manifest.json`.
- Manifest defines:
  - `signature.move_graph.order` — step ordering
  - `components.lenses[]` — step inventory with `lens_id` and `payload_schema_ref`
  - `schemas[]` — adapter-only payload schemas

### Execution model
- Build concrete `steps[]` list from `order`.
- For each step:
  - Map to a kernel-safe lens call:
    - definition → `lens.define`
    - validation → `lens.check`
    - reasoning → `lens.trace`
    - guard → `lens.refuse`
  - Validate payload against `schemas[]`.
  - Invoke kernel router (`lens.define|check|trace|refuse`).
  - Append `result` to `steps[i]`.

- On error emission (`ok:false` such as `E_PAYLOAD`):
  - Stop.
  - Append final `lens.refuse` summarizing the failure and suggesting `menu`.

### Result bundling
Return a single compound result:

```json
{
  "ok": true,
  "compound_id": "compound.NAME",
  "version": "<manifest.version>",
  "steps": [
    {"id": "<step_id>", "lens": "lens.define|check|trace|refuse", "payload": {...}, "result": {...}}
  ],
  "artifacts": { /* adapter summary */ }
}
````

---

## Pseudocode

```python
def handle_invocation(envelope):
    if envelope.id == "lens.list":
        return load_json("runtime/spec/lens.catalog.v1.json")

    if not envelope.id.startswith("lens.compound."):
        return pass_through()

    name = envelope.id.split('.')[2]
    entry = find_in_catalog("compound."+name)
    if not entry:
        return refuse("E_NAMESPACE", f"Unknown compound {name}")

    manifest = load_json(entry.manifest)
    order = manifest.signature.move_graph.order
    steps = index_by_id(manifest.components.lenses)

    results = []
    for sid in order:
        comp = steps[sid]
        schema = find_schema(manifest.schemas, comp.payload_schema_ref)
        payload = project_payload(envelope.payload, schema)
        lens_id = map_to_kernel_lens(sid)
        emission = router_invoke(f"lens.{lens_id}", payload)
        results.append({"id": sid, "lens": f"lens.{lens_id}", "payload": payload, "result": emission})
        surface_preface(sid, payload, emission)   # invariant surfacing

        if emission.ok is False:
            final = router_invoke("lens.refuse", {
                "reason": "compound_step_failed",
                "forward_route": {"label": "menu", "suggestion": "Return to menu"}
            })
            return {
                "ok": False,
                "compound_id": entry.id,
                "partial": True,
                "steps": results + [{"id": "final_refuse", "lens": "lens.refuse", "result": final}]
            }

    artifacts = compose_artifacts(results)
    return {"ok": True, "compound_id": entry.id, "version": manifest.version, "steps": results, "artifacts": artifacts}
```

---

## Notes

* All kernel calls restricted to allow-listed lenses (`define|check|trace|refuse`).
* No external I/O; adapter = orchestration + shaping.
* Surfacing invariant ensures transparency and ledger parity.

---
