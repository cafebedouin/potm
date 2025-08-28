---
id: potm.kernel.v1_2_1
title: potm_bootpack_kernel
display_title: "PoTM Boot Pack Kernel v1.2.1 (Single-File, P1)"
type: kernel 
lifecycle: canon
version: 1.2.1
status: active
stability: core
summary: "Self-contained P1 kernel with embedded bridge, validator, and deck data. No external authority required."
relations:
  supersedes: [potm.kernel.v1_2]
  superseded_by: []
tags: [kernel, bootpack, reference, P1, single_file]
author: practitioner
license: CC0-1.0
---
# PoTM Kernel — Part 06 (of 8)
Version: v1.2 | Generated: 2025-08-20

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: interfaces/ligament.md ---8<---
---
id: potm.proto.bridge.ligament.v1
title: bridge_iface
display_title: "Kernel↔Interface Ligament"
type: agent_protocol
status: draft
version: 1.0
stability: core
relations:
  agent_protocol: ver1.4/potm_bootpack_combined.md
  practitioner_doc: modules/practices/practice_menu.md
interfaces: [kernel_menu, deck_adapter, journal_adapter, checklist_adapter]
preconditions: ["contract.accepted == true"]
outputs: [bridge_event, deck_call, adapter_result]
cadence: ["on_menu_invoked","on_help_like_query","on_idle_start"]
entry_cues: ["menu","help","draw","card","prompt"]
safety_notes:
  - "No mode leakage: kernel constraints remain active."
  - "No hidden dependencies: ligament contains no business logic."
tags: [bridge, interface, kernel]
author: practitioner
license: CC0-1.0
---

# State Envelope
… (as per spec)

# Events
… (as per spec)

# Surface Registry
surface_registry:
  deck: data/decks/cards.yaml
  zuihitsu: data/zuihitsu/default_test.txt
  # future: journals, checklists

# Return Contract
… (as per spec)

# Bridge Logic

- On `deckcall`, parse:
    payload:
      action: "draw"
      deck:   "cards"       # default deck id
      n:      Int
      index?: Int
      tags?:  [String]
  - Load `data/decks/cards.yaml`; assert top.id == "cards"
  - If `index` provided → return that card
  - Else → pick `n` cards (filter by `tags` if provided)
  - Emit:
      kind: "adapter_result"
      payload:
        render: "card"
        card: { id, title, tags, body }

- On `zuicall`, parse:
    payload:
      action: "pick"
      source?: "default_test"
      n:      Int
      index?: Int
  - Resolve file: `data/zuihitsu/${source||"default_test"}.txt`
  - Split on lines containing only `%`
  - If `index` provided → return that quote
  - Else → pick `n` random quotes
  - Emit:
      kind: "adapter_result"
      payload:
        render: "zuihitsu"
        quotes: [{ id, body }]

# Validator Hook
All LIGAMENT outputs are emitted via `LIGAMENT.EMIT`. A mandatory `ligament_validator` subscribes to this stream:
- Shape → whitelist → mode policy
- On FAIL: emit `GUARDIAN.FLAG_INTRUSION`, set `containment=true`, return `DENY.WITH_GROUNDING`
- LIGAMENT holds no business logic beyond routing.

# Parser Hooks
… (as per spec)

## Menu Surface Spec (non-normative UI contract)

When the practitioner says `menu` or `draw`, the bridge MAY emit:

```json
{
  "kind": "bridgeevent",
  "payload": {
    "type": "MENU.RENDER",
    "surface": "practicemenu",
    "menu": {
      "surface_id": "practicemenu",
      "sections": [
        {
          "id": "cards",
          "title": "Cards",
          "items": [
            {
              "id": "cards.draw.one",
              "label": "Draw one card",
              "cue": "draw 1",
              "emits": {
                "kind": "deckcall",
                "payload": { "action": "draw", "deck": "cards", "n": 1 }
              }
            },
            {
              "id": "cards.draw.one.truth",
              "label": "Draw one (tag: truth)",
              "cue": "draw 1 truth",
              "emits": {
                "kind": "deckcall",
                "payload": { "action": "draw", "deck": "cards", "n": 1, "tags": ["truth"] }
              }
            }
          ]
        },
        {
          "id": "zuihitsu",
          "title": "Zuihitsu",
          "items": [
            {
              "id": "zui.pick.one",
              "label": "Pick one quote",
              "cue": "pick 1",
              "emits": {
                "kind": "zuicall",
                "payload": { "action": "pick", "n": 1 }
              }
            },
            {
              "id": "zui.pick.index.2",
              "label": "Pick quote #2",
              "cue": "pick 1 index:2",
              "emits": {
                "kind": "zuicall",
                "payload": { "action": "pick", "n": 1, "index": 2 }
              }
            }
          ]
        }
      ]
    }
  }
}
```

---8<--- /END FILE: interfaces/ligament.md ---8<---

---8<--- FILE: interfaces/adapters/deck_adapter.md ---8<---
---
id: potm.proto.adapter.deck.v1
title: deck_adapter
display_title: "Deck Adapter"
type: agent_protocol
status: draft
version: 1.0
stability: core
interfaces: [deck_adapter]
outputs: [adapter_result]
preconditions: ["contract.accepted == true"]
tags: [bridge, deck]
author: practitioner
license: CC0-1.0
---

## DeckCall Payload Schema
```json
{
  "type": "object",
  "required": ["action","n"],
  "properties": {
    "action": { "const": "draw" },
    "deck":   { "type": "string", "default": "cards" },
    "n":      { "type": "integer", "minimum": 1 },
    "index":  { "type": "integer", "minimum": 1 },
    "tags":   { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": false
}
```

---8<--- /END FILE: interfaces/adapters/deck_adapter.md ---8<---

---8<--- FILE: interfaces/adapters/zuihitsu_adapter.md ---8<---
---
id: potm.proto.adapter.zuihitsu.v1
title: zuihitsu_adapter
display_title: "Zuihitsu Adapter"
type: agent_protocol
status: draft
version: 1.0
stability: core
interfaces: [zuihitsu_adapter]
outputs: [adapter_result]
preconditions: ["contract.accepted == true"]
tags: [bridge, zuihitsu, quotes]
author: practitioner
license: CC0-1.0
---

## ZuiCall Payload Schema
```json
{
  "type": "object",
  "required": ["action","n"],
  "properties": {
    "action": { "const": "pick" },
    "source": { "type": "string", "default": "default_test" },
    "n":      { "type": "integer", "minimum": 1 },
    "index":  { "type": "integer", "minimum": 1 }
  },
  "additionalProperties": false
}
```

---8<--- /END FILE: interfaces/adapters/zuihitsu_adapter.md ---8<---

---8<--- FILE: interfaces/validators/ligament_validator.md ---8<---
---
id: potm.tactic.ligament_validator.v1_0
title: ligament_validator
display_title: "LIGAMENT Validator — Immune Checkpoint"
type: tactic
subtype: safeguard
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "Second-order validator for LIGAMENT outputs; fail-closed on contract violations."
relations:
  related: [potm.proto.bridge.ligament.v1, potm.doctrine.system_modes.v1_0, potm.meta.membrane_model.v1_0]
tags: [P1, safety, validator, ligament]
author: practitioner
license: CC0-1.0
---

## Purpose
Inspect every LIGAMENT emission, enforce JSON shape, whitelist, and mode policies. Any deviation triggers containment.

## When to Run
Always-on for all outputs: `bridgeevent | deckcall | adapter_result`.

## Inputs
- `ligament_output`
- `state_envelope`
- `origin_event` (optional)

## Procedure
1. Parse & shape-check (`LigamentOutput.schema.json`).
2. Whitelist check (`allowed_events_p1.yaml`).
3. Mode policy check (`mode_policy.yaml`).
4. Decision:
   - PASS → forward unchanged
   - FAIL → emit `GUARDIAN.FLAG_INTRUSION`, set `containment=true`, return `DENY.WITH_GROUNDING`
5. Append ledger entry with reason code and payload hash.

## Interfaces
**monitor_ligament_output**
Input schema: `LigamentOutput.schema.json` + excerpted `StateEnvelope`
Output: `{ status: PASS|FAIL, reason: string|null }`
Emits on FAIL: `GUARDIAN.FLAG_INTRUSION`, `MODE.SET: containment=true`
Return on FAIL: `bridgeevent:DENY.WITH_GROUNDING`

## Artifacts
- `schemas/ligament_output_schema.json`
- `interfaces/validators/policies/allowed_events_p1.yaml`
- `interfaces/validators/policies/mode_policy.yaml`
- `tests/ligament_validator_spec.yaml`

---8<--- /END FILE: interfaces/validators/ligament_validator.md ---8<---

---8<--- FILE: interfaces/validators/policies/allowed_events_p1.yaml ---8<---
allowed_events:
  - bridgeevent: ["MENU.OPEN","MENU.RENDER","DENY.WITH_GROUNDING","BYPASS.LIGAMENT"]
  - deckcall:    ["draw"]
  - zuicall:     ["pick"]
  - adapter_result: ["card","zuihitsu","finalize_answer"]


---8<--- /END FILE: interfaces/validators/policies/allowed_events_p1.yaml ---8<---

---8<--- FILE: interfaces/validators/policies/mode_policy.yaml ---8<---
modes:
  containment:
    block:
      - kind: deckcall
      - kind: zuicall
  fracture_active:
    require_note_for:
      - kind: adapter_result
        render: finalize_answer

---8<--- /END FILE: interfaces/validators/policies/mode_policy.yaml ---8<---

