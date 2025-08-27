```markdown
---
id: potm.kernel.recap_validator.v1_0_dev
title: "60_recap_validator"
display_title: "Recap — Payload Validator (P1)"
type: kernel
lifecycle: canon
version: 1.0.0-dev
status: active
stability: stable
summary: >-
  Validates `recap.spec` payload for allowed fields and hard caps.
author: practitioner
license: CC0-1.0
---

## Overview

Asserts that every key and value in a `recap.spec` call  
adheres to the fixed set of fields and numeric ranges.  
Session-local and side-effect free; fails closed on any violation.

- scope: session-local only; no background I/O  
- side effects: none  

---

## Invocation (router contract)

The router invokes this validator before dispatching to `recap.spec`:

```yaml
tool.validate:
  id: "recap.validator"
  payload_schema: "recap_validator"
```

Unknown or out-of-range values cause immediate failure.

---

## Schema (`recap_validator`)

```yaml
recap_validator:
  type: object
  properties:
    include:
      type: array
      items:
        type: string
        enum: ["summary","open_questions","next_hints","last_moves","flags","ledger_refs"]
    max_items:
      type: integer
      minimum: 1
      maximum: 10
    max_words_line:
      type: integer
      minimum: 1
      maximum: 32
  additionalProperties: false
```

- omit any property to apply defaults (`max_items:5`, `max_words_line:24`)  
- `include` default set: `["summary","open_questions","next_hints","last_moves","flags"]`

---

## Failure modes (errors)

| condition                                      | emission                                    |
| ---------------------------------------------- | ------------------------------------------- |
| `include` not an array of allowed strings      | `error.signal { code: "invalid_payload" }`  |
| `max_items` < 1 or > 10                        | `error.signal { code: "invalid_payload" }`  |
| `max_words_line` < 1 or > 32                   | `error.signal { code: "invalid_payload" }`  |
| extra keys present in payload                  | `error.signal { code: "invalid_payload" }`  |
```

---
