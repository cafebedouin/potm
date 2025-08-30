---
id: potm.kernel.recap_spec.v1_6_dev
title: "50_recap_spec"
display_title: "Recap — Deterministic Packet (P1)"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines a minimal, deterministic recap packet. Invocation is namespaced
  as `recap.spec`. Recap is session-local, side-effect free, and export-gated.
author: practitioner
license: CC0-1.0
---

# Recap — Deterministic Packet (P1)

## Overview

The recap spec returns a **compact, machine-parseable snapshot** of the current session, suitable for in-session review or safe handoff to closure tools.  
It is **not** a narrative; it produces a fixed-shape packet with strict field names and word caps where applicable.

- **scope:** session-local only; no background I/O  
- **side effects:** none (read-only over session state)  
- **export:** denied unless explicit header (see `90_policy.md`)  

---

## Invocation (router contract)

Call recap via a **structured, namespaced id**. Plain prose is inert.

> Validation: the router enforces `recap_validator` (see `60_recap_validator.md`). Unknown keys are rejected (fail-closed).

Payload schema: `runtime/spec/recap.spec_payload.json`  
Example: `runtime/examples/recap_spec_invoke.json`

* Unknown keys in `payload` are **rejected**. (`additionalProperties:false`)
* If `include` is omitted, the default set is returned (see Output).

---

## Input sources (read-only)

Recap may read from:

* `meta_locus` (see `70_state.md`)
* last N **kernel emissions** (`tool.result`, `beacon.check|optional`, `menu.signal`, `error.signal`)
* in-memory **ledger buffer** (session-local entries only; see `90_policy.md`)

No external files, no adapters, no decks.

---

## Output (recap_packet schema)

Result schema: `runtime/spec/recap.spec_result.json`  
Example result: `runtime/examples/recap_spec_result.json`

**Defaults (when `include` is omitted):**
`["summary","open_questions","next_hints","last_moves","flags"]`

**Caps (hard):**

* `max_items` default 5; hard cap 10.
* `max_words_line` default 24; hard cap 32.

---

## Determinism & word-caps

* All free-text lines MUST respect `max_words_line`.
* `open_questions` and `next_hints` are **hint-level** (no multi-step plans).
* `last_moves` MUST list most recent valid kernel actions only; handshakes are excluded unless they produced artifacts.

---

## Failure modes (errors)

The recap must **fail-closed** and never mutate state.

| condition                            | emission                                   |
| ------------------------------------ | ------------------------------------------ |
| bad envelope / missing `tool.call`   | `error.signal { code: "bad_envelope" }`    |
| wrong id (not `recap.spec`)          | `error.signal { code: "unknown_id" }`      |
| invalid payload (types/ranges)       | `error.signal { code: "invalid_payload" }` |
| not accepted gate (`accepted=false`) | `error.signal { code: "not_accepted" }`    |

(See `40_router.md` for general dispatch rules.)

---

## Examples

**1) Basic call (defaults)** — see `runtime/examples/recap_spec_invoke.json`

**2) Narrowed fields with tighter caps** — see `runtime/examples/recap_spec_invoke.json`

**3) Example response (truncated)** — see `runtime/examples/recap_spec_result.json`

---

## Export guard (P1)

Recap packets are **not** exported by default. To authorize one-time text export, the operator must include exactly:

```
EXPORT: ALLOW
scope: {artifact: recap_packet, fields: [summary,last_moves,...]}
```

Absent this header, export is denied (see `90_policy.md`).

---

## Security & privacy

* Session-local only; no background I/O or external authority.
* Redact personally sensitive strings if present in `artifact_ref` inline payloads (implementation detail).
* Beacons remain active; recap must not suppress beacon checks.

---

## Notes & references

* **router contract:** `40_router.md`
* **state:** `70_state.md`
* **policy & ledger:** `90_policy.md`
* **lenses & moves:** `30_lenses.md`, `35_micromoves.md`

```
---
