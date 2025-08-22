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
interfaces: [kernel_menu, deck_adapter, zuihitsu_adapter]
preconditions: ["contract.accepted == true"]
outputs: [bridge_event, deck_call, zui_call, adapter_result]
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

- On `deck_call`, parse:
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

- On `zui_call`, parse:
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
  "kind": "bridge_event",
  "payload": {
    "type": "MENU.RENDER",
    "surface": "practicemenu",
    "menu": {
      "surface_id": "practice_menu",
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
                "kind": "deck_call",
                "payload": { "action": "draw", "deck": "cards", "n": 1 }
              }
            },
            {
              "id": "cards.draw.one.truth",
              "label": "Draw one (tag: truth)",
              "cue": "draw 1 truth",
              "emits": {
                "kind": "deck_call",
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
                "kind": "zui_call",
                "payload": { "action": "pick", "n": 1 }
              }
            },
            {
              "id": "zui.pick.index.2",
              "label": "Pick quote #2",
              "cue": "pick 1 index:2",
              "emits": {
                "kind": "zui_call",
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
