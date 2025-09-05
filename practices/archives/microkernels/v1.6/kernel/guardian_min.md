---
id: potm.kernel.guardian_min.v1
title: "guardian_min"
display_title: "Guardian — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Deterministic guardian shim for the microkernel.  
  Provides only the `guardian.trigger` tool, bound to schemas.  
  All ambient monitoring and heuristics remain in extended/.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, guardian, minimal, containment, escalation]
author: practitioner
license: CC0-1.0
---

# Guardian — Minimal Contract

**Scope.** Guardian in the kernel is a *deterministic trigger interface*.  
It does not ambiently monitor. It only routes explicit `guardian.trigger` calls.  
Extended guardian modules (integrity protocols, heuristics, subsystem overlays) MAY invoke this tool, but the kernel contract here is minimal and invariant.

---

## Catalog (minimal)

| id               | purpose                                | payload schema                                   | result schema                                    |
|------------------|----------------------------------------|--------------------------------------------------|--------------------------------------------------|
| guardian.trigger | Route soft/hard trigger to escalation  | `runtime/spec/guardian.trigger.payload.v1.json`  | `runtime/spec/guardian.trigger.result.v1.json`   |

---

## Semantics

### `guardian.trigger`
- **Inputs (payload).**  
  - `severity: soft|hard`  
  - `reason: string`  
  - optional `context` fields as defined in schema.
- **Outputs (result).**  
  - Deterministic acknowledgment of trigger,  
    including `severity`, `escalation_tier`, and `ledger_ref`.  
- **Side-effects.**  
  - Append a `ledger.guardian_event` entry.  
  - If `severity=soft`: record, watch, MAY elevate to Tier 2 via escalation gates.  
  - If `severity=hard`: immediate elevation (Tier 3/4). If Tier 4, set `meta_locus.containment=true`.  

---

## Failure Modes

| condition                       | emission code  |
|--------------------------------|----------------|
| Invalid payload                 | `E_PAYLOAD`    |
| Quota exceeded (`policy.cap`)   | `E_QUOTA`      |
| Recursive invocation (re-entry) | `E_INVARIANT`  |

---

## Registration (tool index)

In `runtime/spec/tool.index.json` register:

```json
{ "id": "guardian.trigger",
  "payload_schema": "runtime/spec/guardian.trigger.payload.v1.json",
  "result_schema": "runtime/spec/guardian.trigger.result.v1.json" }
