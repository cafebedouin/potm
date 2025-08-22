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
Always-on for all outputs: `bridge_event | deck_call | zui_call | adapter_result`.

## Inputs  
- `ligament_output`  
- `state_envelope`  
- `origin_event` (optional)  

## Procedure  
1. Parse & shape-check (`LigamentOutput.schema.json`).  
2. Whitelist check (`allowed_events_p1.yaml`) for event *and* (if present) surface keys (e.g., `bridge_event: MENU.RENDER -> surface ∈ allowed_surfaces`).
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
Return on FAIL: `bridge_event:DENY.WITH_GROUNDING`

## Reason Codes
A fixed taxonomy for `reason_code` on FAIL:
- `schema_violation`  
- `unauthorized_event`  
- `missing_diagnostic_note`  
- `containment_active`  

## Artifacts  
- `schemas/ligament_output_schema.json`
- `interfaces/validators/policies/allowed_events_p1.yaml`
- `interfaces/validators/policies/mode_policy.yaml`
- `tests/ligament_validator_spec.yaml`
