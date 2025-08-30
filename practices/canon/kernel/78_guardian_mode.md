---
id: potm.kernel.guardian_mode.v1_6_dev
title: "78_guardian_mode"
display_title: "Guardian — Sentinel Overlay"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines Guardian as a sentinel overlay on state and escalation. Monitors
  session signals, evaluates triggers (soft/hard), and hands off to
  escalation/containment when necessary.
author: practitioner
license: CC0-1.0
---

## Purpose

Guardian is an always-on safety sentinel. It runs in parallel with normal
kernel operation to detect destabilization, ethical heat, or threat to
integrity. Guardian never diagnoses; it routes.

---

## Lifecycle

1) Monitor  
   - Ambient checks against trigger conditions.  
   - Harmonizes with validators and canary signals.  

2) Trigger Evaluation  
   - `severity: soft` → record + watch; may elevate to Tier 2 depending on context.  
   - `severity: hard` → immediate elevation (Tier 3/4) via escalation gates.  

3) Handoff  
   - Tier 2–3 → escalate profile and/or open fracture (see `68_escalation_gates.md`).  
   - Tier 4 → enter containment (see `76_containment_mode.md`).  

All actions must log ledger entries (`guardian_event`).

---

## Tools (allow-list)

- `guardian.trigger`  
  - Payload: `runtime/spec/guardian.trigger_payload.json`  
  - Result:  `runtime/spec/guardian.trigger_result.json`

---

## Failure Modes

- Invalid trigger payload → `E_PAYLOAD`  
- Quota exceeded (`policy.cap.guardian_max`) → `E_QUOTA`  
- Recursive invocation (during active trigger handling) → `E_INVARIANT`  

---

## Pointers

- Payload/Result schemas:  
  - `runtime/spec/guardian.trigger_payload.json`  
  - `runtime/spec/guardian.trigger_result.json`
- Ledger entry schema: `runtime/spec/ledger.guardian_event.json`  
- Escalation gates: `kernel/68_escalation_gates.md`  
- Containment integration (Tier 4): `kernel/76_containment_mode.md`

