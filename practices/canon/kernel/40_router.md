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

```json
{
  "$id": "potm.kernel.router.envelope.v1",
  "type": "object",
  "required": ["tool.call"],
  "additionalProperties": false,
  "properties": {
    "tool.call": {
      "type": "object",
      "required": ["id", "payload"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*$"
        },
        "payload": {
          "type": "object",
          "additionalProperties": true
        },
        "meta": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "request_id": {
              "type": "string",
              "format": "uuid"
            },
            "trace": {
              "type": "boolean",
              "default": false
            },
            "origin": {
              "type": "string",
              "maxLength": 64
            }
          }
        }
      }
    }
  }
}
```

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
```

> **Out of kernel (interpretive/adapters):** `menu.*`, `ack.*`, exporters.  
> **Reserved (add later if specced minimally):** invokable `beacon.*` tools. Beacons may log signals but are not router targets.

---

## Tool Index (session-local registry)

Router dispatches only to tools registered here. Missing → `tool.error` `{ code: "E_TOOL" }`.

```yaml
tool.index:
  - id: lens.edge
    payload_schema_ref: "spec/lens.edge.payload.v1.json"
    result_schema_ref:  "spec/lens.edge.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"

  - id: move.align_scan
    payload_schema_ref: "spec/move.align_scan.payload.v1.json"
    result_schema_ref:  "spec/move.align_scan.result.v1.json"

  - id: closure.spiral
    payload_schema_ref: "spec/closure.spiral.payload.v1.json"
    result_schema_ref:  "spec/closure.spiral.result.v1.json"

  - id: closure.archive
    payload_schema_ref: "spec/closure.archive.payload.v1.json"
    result_schema_ref:  "spec/closure.archive.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"
      - "len(meta_locus.review_queue) == 0"
    quota:
      ledger_append: "policy.cap.ledger_max"

  - id: closure.waiting_with
    payload_schema_ref: "spec/closure.waiting_with.payload.v1.json"
    result_schema_ref:  "spec/closure.waiting_with.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"
      - "len(meta_locus.review_queue) > 0"
    quota:
      ledger_append: "policy.cap.ledger_max"

  - id: policy.query
    payload_schema_ref: "spec/policy.query.payload.v1.json"
    result_schema_ref:  "spec/policy.query.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"

  - id: policy.enforce
    payload_schema_ref: "spec/policy.enforce.payload.v1.json"
    result_schema_ref:  "spec/policy.enforce.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"
    quota:
      ledger_append: "policy.cap.ledger_max"

  - id: policy.report
    payload_schema_ref: "spec/policy.report.payload.v1.json"
    result_schema_ref:  "spec/policy.report.result.v1.json"
    preconditions:
      - "meta_locus.accepted == true"

  - id: recap.spec
    payload_schema_ref: "spec/recap.spec.payload.v1.json"
    result_schema_ref:  "spec/recap.spec.result.v1.json"
    validator:
      payload_schema_ref: "spec/recap.validator.payload.v1.json"
      result_schema_ref:  "spec/recap.validator.result.v1.json"
      mode: "fail_closed"
```

Each payload/result schema must set `additionalProperties:false` and define numeric/string caps. `tool.index` is immutable for the session.

---

## Dispatch Algorithm (deterministic)

1. Validate envelope against `potm.kernel.router.envelope.v1`.  
2. Split `id` → `{namespace, name}`; verify namespace in allow-list.  
3. Lookup full `id` in `tool.index`.  
4. Validate `payload` against tool’s schema; enforce global caps.  
5. Check preconditions (session flags like `agreement.accepted`).
6. Idempotency:
   - Compute `digest := SHA256(canonical(id,payload))` where `canonical`:
     • lowercases namespace/name; • sorts object keys lexicographically at all depths;
     • strips insignificant whitespace; • preserves array order.
   - If `request_id` seen with *same* `digest` → return cached emission.
   - If `request_id` seen with *different* `digest` → `tool.error { code:"E_INVARIANT", reason:"request_id_reuse_mismatch" }`.
7. Execute tool (pure, no side-effects).  
8. Emit `tool.emit` or `tool.error` (see Emissions Contract).

`meta.trace` does not affect behavior, only whether debug frames appear in the emission.

---

## Emissions Contract

> JSON Schema (draft 2020-12). All unspecified fields are rejected.

```json
{
  "$id": "potm.kernel.router.emission.v1",
  "type": "object",
  "oneOf": [
    {
      "required": ["tool.emit"],
      "properties": {
        "tool.emit": {
          "type": "object",
          "required": ["id", "ok", "result"],
          "additionalProperties": false,
          "properties": {
            "id": { "type": "string" },
            "ok": { "const": true },
            "result": { "type": "object" },
            "trace": {
              "type": "array",
              "items": { "type": "string" },
              "maxItems": 32
            }
          }
        }
      }
    },
    {
      "required": ["tool.error"],
      "properties": {
        "tool.error": {
          "type": "object",
          "required": ["id", "ok", "code", "reason"],
          "additionalProperties": false,
          "properties": {
            "id": { "type": "string" },
            "ok": { "const": false },
            "code": {
              "type": "string",
              "enum": [
                "E_NAMESPACE",
                "E_TOOL",
                "E_PAYLOAD",
                "E_PRECONDITION",
                "E_QUOTA",
                "E_DISABLED",
                "E_INVARIANT"
              ]
            },
            "reason": {
              "type": "string",
              "maxLength": 512
            },
            "trace": {
              "type": "array",
              "items": { "type": "string" },
              "maxItems": 32
            }
          }
        }
      }
    }
  ],
  "additionalProperties": false
}
```

---

## Examples

**Valid call**

```yaml
tool.call:
  id: "recap.spec"
  payload:
    include: ["last_moves","flags"]
    max_items: 5
  meta:
    request_id: "9f1f3f0c-9e6d-4d5b-9a1d-9d9f2c1a8a77"
    trace: false
```

**Rejected (unknown namespace)**

```yaml
tool.call:
  id: "cards.draw"      # not in allow-list
  payload: { n: 3 }
# -> tool.error:
#    code: "E_NAMESPACE"
#    reason: "namespace 'cards' not allowed"
```

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