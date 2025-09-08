---
id: potm.kernel.recap_validator.v1_0
title: "60_recap_validator"
display_title: "Recap — Payload Validator (P1)"
type: kernel
lifecycle: canon
version: 1.0.0
status: active
stability: stable
summary: >-
  Validates `recap.spec` payload for allowed fields and references
  `policy.cap.recap` for numeric caps. Rejects unknown keys and
  fails closed on violation.
author: practitioner
license: CC0-1.0
---

## Overview

Asserts that every key and value in a `recap.spec` call  
adheres to the fixed set of fields and numeric ranges defined in policy.  
Session-local and side-effect free; fails closed on any violation.

- scope: session-local only; no background I/O  
- side effects: none  

---

## Invocation (router contract)

The router invokes this validator before dispatching to `recap.spec`:

See:  
- `runtime/examples/recap_validator_invoke.json`

Unknown or out-of-range values cause immediate failure.

---

## Schema (`recap_validator`)

Defined in `runtime/schema/recap_validator.json`.

- `include` (array of allowed strings)  
- `max_items` (bounded by `policy.cap.recap.max_items`)  
- `max_words_line` (bounded by `policy.cap.recap.max_words_line`)  
- `additionalProperties: false`  

Defaults:  
- `max_items: 5`  
- `max_words_line: 24`  
- `include: ["summary","open_questions","next_hints","last_moves","flags"]`

Caps are enforced against `policy.cap.recap`.

---

## Failure Modes (errors)

| condition                                 | emission                                   |
| ----------------------------------------- | ------------------------------------------ |
| `include` not an array of allowed strings | `error.signal { code: "invalid_payload" }` |
| `max_items` out of policy range           | `error.signal { code: "invalid_payload" }` |
| `max_words_line` out of policy range      | `error.signal { code: "invalid_payload" }` |
| extra keys present in payload             | `error.signal { code: "invalid_payload" }` |

---

## Examples

See canonical instances in `runtime/examples/`:

- `recap_validator_invoke.json` — router invocation example  
- `recap_validator_valid.json` — valid payload (within caps)  
- `recap_validator_violation.json` — invalid payload (cap violation)  

---

## Notes

* Export guard is handled by policy (`policy.targets: recap.export`);  
  validator does not authorize export.  
* Defaults are documented in `50_recap_spec.md`.  
