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
preconditions: ["agreement.accepted == true"]
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

### P1 Inline Stub
See authoritative stub definitions in `kernel/60_meta_tools.md` (Inline Stubs, P1).
This file provides extended reference only; runtime behavior is governed by the kernel stubs.

# Ligament Interface

## State Envelope
… (as per spec)

## Events
… (as per spec)

## Surface Registry
surface_registry:
   deck: "[DATA:DECKS_CARDS]"           # your existing in-file deck anchor
   zuihitsu: "[DATA:ZUIHITSU_DEFAULT]"  # your existing in-file zuihitsu anchor
   journal: "[ANNEX:JOURNAL_PROMPTS]"   # new in-file annex (above)

  deck: data/decks/cards.yaml
  zuihitsu: data/zuihitsu/default.txt
  journal: data/journals/prompts.yaml
  # future: roles, checklists

## Return Agreement
… (as per spec)

## Bridge Logic

- On `deck_call`, parse:
    payload:
      action: "draw"
      deck:   "cards"|"journal"      # default deck id
      n:      Int
      context?: [String]
      index?: Int
      tags?:  [String]
   - Resolve surface (anchor-only in P1):
      if deck == "journal": anchor = surface_registry.journal
      else:                  anchor = surface_registry.deck
  - Load by anchor; assert `top.id == deck` (e.g., `id: journal` in ANNEX)
  - If load target looks like a filesystem path → FAIL‑CLOSED in P1
  - Load `path`; assert top.id == deck
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


+### Practitioner Menu Contract (v1.5.1)
`menu` is the sole public entry to surface practitioner choices. Engine categories (lenses, micromoves, meta-tools, closures) remain **backend-only**.

**Event:** `MENU.OPEN`
**Gate:** `ligament_validator`
**On pass → surface exactly six entries:**
1) Cards — `draw 1` | `draw 1 <tag>` | `draw 1 cards context:<topic>`
2) Zuihitsu — `pick 1` | `pick 1 index:<n>`
3) Journaling Prompt — `draw 1 journal`
4) Role Play — `roleplay <voice>`
5) You Have the Floor — free text
6) Card-from-Context — handled by Cards adapter via `context:<topic>`

*(Optional)* After the list, surface one Zuihitsu line as “maxim seasoning”.

**Routing Map**
- `draw*` → Deck Adapter
- `pick*` → Zuihitsu Adapter
- `roleplay*` → Roleplay handler (if present), else decline with safe alt
- free text → Open Prompt flow; backend tools may auto-invoke as needed

 **Non-goals:** Never list lenses/micromoves/meta/closures in menu. They may activate dynamically in response flow.

# Validator Hook
All LIGAMENT outputs are emitted via `LIGAMENT.EMIT`. A mandatory `ligament_validator` subscribes to this stream:
- Shape → whitelist → mode policy  
- On FAIL: emit `GUARDIAN.FLAG_INTRUSION`, set `containment=true`, return `DENY.WITH_GROUNDING`  
- LIGAMENT holds no business logic beyond routing.

# Parser Hooks
… (as per spec)

## Menu Surface Spec (non-normative UI agreement)

When the practitioner says `menu` or `draw`, the bridge MAY emit:

```json
{
  "kind": "bridge_event",
  "payload": {
    "type": "MENU.RENDER",
    "surface": "practice_menu",
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
        }
       ,
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
      ,
      {
         "id": "journals",
         "title": "Journals",
         "items": [
           {
             "id": "journals.draw.one",
             "label": "Draw one journal prompt",
             "cue": "draw 1 journal",
             "emits": {
               "kind": "deck_call",
               "payload": { "action": "draw", "deck": "journal", "n": 1 }
             }
           },
           {
             "id": "journals.draw.index.2",
             "label": "Draw journal prompt #2",
             "cue": "draw 1 journal index:2",
             "emits": {
               "kind": "deck_call",
               "payload": { "action": "draw", "deck": "journal", "n": 1, "index": 2 }
            }
          }
        ]
      }
    }
  }
}
```


