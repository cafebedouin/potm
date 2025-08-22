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
