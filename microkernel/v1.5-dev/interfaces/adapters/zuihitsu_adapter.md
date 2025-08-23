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
preconditions: ["agreement.accepted == true"]
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
    "index":  { "type": "integer", "minimum": 1 },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Optional tags for quote filtering"
    }
   }
  },
  "additionalProperties": false
}
```
