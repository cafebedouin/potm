Here’s a clean, P1-tight **drop-in** for `kernel/80_closure.md`—paste it over your file as-is.

````markdown
---
id: potm.kernel.closure.v1_6_dev
title: "80_closure"
display_title: "Closure Tools"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines P1 closure tools for session-level cycle operations: spiral (drift vs evolution),
  archive (final snapshot), and waiting_with (active containment). Tools are deterministic,
  session-local, and never export; any export is adapter-side and policy-gated.
author: practitioner
license: CC0-1.0
---

## Overview

Closure tools package or gate ongoing threads at the **session** level.

Provided tools (registered in `tool.index`):
- `closure.spiral`
- `closure.archive`
- `closure.waiting_with`

All are invoked via `tool.call`, read/write only session state (`70_state.md`),
and emit structured results or `tool.error` with router-aligned codes.

- scope: session-local only
- I/O: none (no filesystem/network)
- determinism: true (pure function of state + payload)
- failure mode: fail-closed

---

## Invocation

```yaml
tool.call:
  id: "closure.<tool_name>"
  payload: { ... }   # see per-tool schemas below
````

`<tool_name>` ∈ { `spiral`, `archive`, `waiting_with` }.

> Envelope errors & unknown tools are handled by the router (`E_NAMESPACE` / `E_TOOL` / `E_PAYLOAD`).

---

## Tool Schemas & Behavior

### 1) `closure.spiral` — drift vs evolution summary

**Payload schema (JSON, draft 2020-12)**

```json
{
  "$id": "potm.kernel.closure.spiral.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "scope": { "type": "string", "enum": ["session"], "default": "session" }
  }
}
```

**Success emission (result fields)**

* `diff_log`: string, ≤ `policy.cap.diff_log_max` (400 chars) — compact drift vs evolution narrative.

```yaml
tool.emit:
  id: "closure.spiral"
  ok: true
  result:
    diff_log: "<=400 chars summary>"
```

**Notes**

* Intended for cycle boundaries, not every micromove.
* Idempotent given unchanged state (same `diff_log` for same ledger/state).

**Errors**

* Schema violations → `tool.error { code: "E_PAYLOAD" }`

---

### 2) `closure.archive` — final snapshot of a cycle

**Preconditions**

* `len(meta_locus.review_queue) == 0` (no open fractures) → else `E_PRECONDITION`.
* This tool **does not export**. It returns an archive record; any export is adapter-side.

**Payload schema**

```json
{
  "$id": "potm.kernel.closure.archive.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "include": {
      "type": "array",
      "minItems": 1,
      "maxItems": 3,
      "uniqueItems": true,
      "items": { "type": "string", "enum": ["summary","takeaways","archive_status"] }
    }
  }
}
```

**Result schema (fields included per `include`)**

* `summary`: string, ≤ `policy.cap.summary_max` (320 chars)
* `takeaways`: string, ≤ `policy.cap.takeaways_max` (240 chars)
* `archive_status`: enum `["resolved","parked","stalled"]`

**Success emission**

```yaml
tool.emit:
  id: "closure.archive"
  ok: true
  result:
    # only requested fields appear
    summary: "..."
    takeaways: "..."
    archive_status: "resolved"
```

**Ledger**

* Appends a ledger entry (type: `artifact`) with an inline ref to the snapshot.
  Capacity enforced by `policy.cap.ledger_max`.

**Errors**

* Open fractures → `tool.error { code: "E_PRECONDITION" }`
* Payload schema violation → `tool.error { code: "E_PAYLOAD" }`
* Ledger at cap → `tool.error { code: "E_QUOTA" }`

---

### 3) `closure.waiting_with` — active containment for unresolved tensions

**Preconditions**

* `len(meta_locus.review_queue) > 0`.
* Sets `meta_locus.containment = true`; auto-clears via `70_state` when queue empties.

**Payload schema**

```json
{
  "$id": "potm.kernel.closure.waiting_with.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["wait_reason","reentry_hint"],
  "additionalProperties": false,
  "properties": {
    "wait_reason":  { "type": "string", "minLength": 1, "maxLength": 256 },
    "reentry_hint": { "type": "string", "minLength": 1, "maxLength": 64 }
  }
}
```

**Success emission**

```yaml
tool.emit:
  id: "closure.waiting_with"
  ok: true
  result:
    wait_reason: "<echo>"
    reentry_hint: "<echo>"
```

**Ledger**

* Appends a ledger entry (type: `move`) capturing containment start + hints.
  Capacity enforced by `policy.cap.ledger_max`.

**Errors**

* No open fractures → `tool.error { code: "E_PRECONDITION" }`
* Payload schema violation → `tool.error { code: "E_PAYLOAD" }`
* Ledger at cap (rare here) → `tool.error { code: "E_QUOTA" }`

---

## Data Annexes (read-only, optional)

* `ANNEX:FRACTURE_TAXONOMY_MINI` (P1-MIN; improves spiral wording)
* `ANNEX:FRACTURE_TAXONOMY` (P1-ALL, if present)
* `ANNEX:FRACTURE_CROSSWALK` (optional)
* `ANNEX:FRACTURE_META_UNITY` (optional)

> Annexes refine labels only; absence must not change tool behavior.

---

## Examples

**Spiral (default scope)**

```yaml
tool.call:
  id: "closure.spiral"
  payload: {}
# → tool.emit { ok:true, result:{ diff_log:"..." } }
```

**Archive with specific fields**

```yaml
tool.call:
  id: "closure.archive"
  payload:
    include: ["summary","archive_status"]
# pre: len(meta_locus.review_queue) == 0
# → tool.emit { ok:true, result:{ summary:"...", archive_status:"resolved" } }
```

**Enter waiting\_with**

```yaml
tool.call:
  id: "closure.waiting_with"
  payload:
    wait_reason: "Spiking heat; unresolved value conflict"
    reentry_hint: "OpenQ after sleep"
# pre: len(meta_locus.review_queue) > 0
# → tool.emit { ok:true, result:{ ... } }; meta_locus.containment = true
```

---

## Failure Modes (router-aligned)

| condition                               | emission code    |
| --------------------------------------- | ---------------- |
| payload fails schema                    | `E_PAYLOAD`      |
| open fractures on `closure.archive`     | `E_PRECONDITION` |
| `waiting_with` without open fracture    | `E_PRECONDITION` |
| ledger buffer full during ledger append | `E_QUOTA`        |

---

## Versioning & Change Log

* **1.6.0-dev**: Initial P1 spec for `closure.spiral`, `closure.archive`, `closure.waiting_with`; router-aligned errors; state-gated preconditions; policy-gated caps; idempotent outputs.

```
---
