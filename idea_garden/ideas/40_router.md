---
id: potm.kernel.router.v1_6_dev
title: "40_router"
display_title: "Router — Invocation Grammar & Dispatch"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines a strictly schema-guarded envelope, explicit namespace allow-list,
  deterministic dispatch algorithm, idempotency via request_id, and a unified
  emission contract. Fail-closed by default; pure function of input.
author: practitioner
license: CC0-1.0
---

## Router — Invocation Grammar & Dispatch

The kernel executes only structured calls. Plain text is inert.  
Adapters may translate human input into structured calls; the kernel never  
infers intent from prose.

- scope: session-local only  
- I/O: none (no network, no filesystem)  
- determinism: true (pure function of input)  
- failure mode: fail-closed  

---

### Canonicalization (normative)

All router caches MUST use the canonical form above when comparing payloads for
idempotency. Implementations MAY store `digest` alongside `request_id`.

> The router **strips unknown keys inside `tool.call.meta`** prior to envelope
> validation to prevent adapter meta-leakage. All other unknown fields fail-closed.
>
> The full envelope schema is externalized:  
> **see `runtime/spec/router_envelope.json`**

The router validates every call against this schema before further dispatch.

---

## Global Caps (P1)

- Envelope size ≤ 8 KB  
- Payload depth ≤ 3; object keys ≤ 64 chars; arrays ≤ 32 items  
- String field length ≤ 2 KB (per field)  

---

## Namespaces (allow-list)

Only these namespaces are executable. Unknown → `tool.error` `{ code: "E_NAMESPACE" }`.

```
lens.*       # diagnostic lenses
move.*       # atomic micro-moves
closure.*    # closure tools
recap.*      # recap.spec
policy.*     # policy.query / enforce / report
glyph.*      # glyph invocations
guardian.*   # guardian triggers
```

> **Out of kernel (interpretive/adapters):** `menu.*`, `ack.*`, exporters.  
> **Reserved (add later if specced minimally):** invokable `beacon.*` tools. Beacons may log signals but are not router targets.

---

## Tool Index (session-local registry)

Router dispatches only to tools registered here. Missing → `tool.error` `{ code: "E_TOOL" }`.

Externalized registry: `runtime/spec/tool.index.json`

Fracture moves (registered): `move.open_fracture`, `move.review_fracture`, `move.close_review`.

Each payload/result schema must set `additionalProperties:false` and define numeric/string caps. `tool.index` is immutable for the session.

---

## Dispatch Algorithm (deterministic)

1. Validate envelope against `potm.kernel.router.envelope.v1`.  
2. Split `id` → `{namespace, name}`; verify namespace in allow-list.  
3. Lookup full `id` in `tool.index`.  

4. **Run validator chain (P1):**
   - **latency.validator** (always)
     * Ensures `meta_locus.latency_mode` is valid.
     * Enforces fast-path invariant per mode.
     * Checks observed latency against `policy.cap.latency[mode].p95`.
     * Emits `E_LATENCY_MODE`, `E_LATENCY_INVARIANT`, `W_LATENCY_EXTRA`, `W_LATENCY_BREACH`, or `W_LATENCY_FALSE_BREACH`.

   - **recap.validator** (only when `id == recap.spec`)
     * Enforces recap payload schema (`include`, `max_items`, `max_words_line`).
     * Caps checked against `policy.cap.recap`.
     * Emits `E_PAYLOAD` on any schema violation.
     * Export guard is handled by `policy.targets: recap.export`.

   > Ordering is strict: latency first, then tool-specific validators, then the tool itself.  
   > If any validator fails, dispatch halts and only the first error is emitted.  

5. Validate `payload` against the tool’s schema; enforce global caps.  
6. Check preconditions (session flags like `agreement.accepted`).  
7. Idempotency:
   - Compute `digest := SHA256(canonical(id,payload))` where `canonical`:
     • lowercases namespace/name; • sorts object keys lexicographically at all depths;  
     • strips insignificant whitespace; • preserves array order.
   - If `request_id` seen with *same* `digest` → return cached emission.  
   - If `request_id` seen with *different* `digest` →  
     `tool.error { code:"E_INVARIANT", reason:"request_id_reuse_mismatch" }`.  

8. Execute tool (pure, no side-effects).  
9. Emit `tool.emit` or `tool.error` (see Emissions Contract).  

`meta.trace` does not affect behavior, only whether debug frames appear in the emission.

---

## Emissions Contract

> The full emissions schema is externalized:  
> **see `runtime/spec/router_emission.json`**

Router emissions must conform exactly; unspecified fields are rejected.

---

## Examples

**Valid call** — see `runtime/examples/recap_spec_invoke.json`

**Fracture moves** — router calls:  
- Open: `runtime/examples/fracture_open.json`  
- Review: `runtime/examples/fracture_review.json`  
- Resolve: `runtime/examples/fracture_resolve.json`

**Glyphs** — router call & result:  
- Invoke: `runtime/examples/glyph_invoke.json`  
- Result: `runtime/examples/glyph_result.json`
  
Ledger (glyph events):  
- `runtime/examples/glyph_invoke_ledger.json`  
- `runtime/examples/glyph_result_ledger.json`  
- `runtime/examples/glyph_map_ledger.json`

**Guardian** — router call & result:  
- Trigger (soft): `runtime/examples/guardian_trigger_soft.json`  
- Trigger (hard): `runtime/examples/guardian_trigger_hard.json`  
- Result: `runtime/examples/guardian_trigger_result.json`  
  
Ledger (guardian events):  
- `runtime/examples/guardian_soft_ledger.json`  
- `runtime/examples/guardian_hard_ledger.json`

**Externalist** — router call & result:
- Invoke: `runtime/examples/externalist_invoke.json`  
- Result: `runtime/examples/externalist_result.json`  
  
Ledger (externalist events):  
- `runtime/examples/externalist_ledger.json`

---

## Router Notes

- Glyph actions (invoke, result, map) MUST log a `glyph_event` ledger entry.  
  Schema: `runtime/spec/ledger.glyph_event.json` (capacity bound by `policy.cap.ledger_max`).

- Fracture diagnostics ("Fracture Finder" workflows) live under `extended/diagnostics/fracture/`  
  and are practitioner-facing protocols, not router tools. Router exposes only  
  the fracture queue moves (e.g., `move.open_fracture`, `move.review_fracture`, `move.close_review`).

- BS-Detect and Sentinel Spotcheck are practitioner diagnostics (session-local) and not router tools.  
  Results and ledger entries are documented under:  
  - `runtime/spec/bs_detect_result.json`, `runtime/spec/ledger.bs_detect_event.json`  
  - `runtime/spec/sentinel_spotcheck.json`, `runtime/spec/ledger.spotcheck_event.json`

**Rejected (unknown namespace)** — see `id` pattern in `runtime/spec/router_envelope.json`

---

## Failure Modes & Counters (P1)

- Schema drift → schemas versioned & pinned in `tool.index`  
- Adapter meta leakage → router strips unknown meta keys before validation  
- Replay storms → session cache keyed by `request_id` (LRU ≤ 128)  
- Caps evasion → router enforces global caps before tool validation  
- Ambiguous tool id → strict `id` pattern + allow-list  

## Latency Validation Hook

Before emitting any routed output, the router must invoke the validator’s
latency check (see `60_validator.md`). This ensures contract (85) is enforced
in-flow.

```pseudo
result = validator.latency_check()

if result == error:
    halt
    emit kernel.error { code: "E_LATENCY_INVARIANT" }
elif result == warning:
    emit [LATENCY WARNING] + normal response
else:
    continue → normal emission

---

## Versioning & Change Log

- 1.6.0-dev: Introduce envelope/emission schemas, namespace allow-list,  
  idempotency, fixed dispatch order, global caps enforcement, fail-closed defaults.  
```
