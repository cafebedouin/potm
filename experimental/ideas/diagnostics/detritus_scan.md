---
id: potm.diag.simdrift_detritus_scan.v1
title: Simulation Drift + Detritus Layer Scan
display_title: "Simulation Drift + Detritus Layer Scan"
type: diagnostic
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: linked
  agent_protocol: modules/ai_integrity_protocol_v1.6.md
  practitioner_doc: modules/practitioner_centered_ethics_v1.1.md
  supersedes: []
  superseded_by: []
interfaces: [PCE, AIIP, Mirror Protocol]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: [drift_flag, contact_flag, re_audit_flag]
cadence:
  - on_detected_friction_loss
  - on_periodic_review
entry_cues:
  - "Run drift scan"
  - "Check for detritus"
  - "Do we need a re-audit?"
safety_notes:
  - This scan can surface destabilizing material if live-contact testing contradicts strongly held views.
  - Practitioners should pace themselves and use containment protocols if distress arises.
tags: [diagnostic, simulation-drift, detritus-layer, epistemic-integrity, friction-check]
author: practitioner
license: CC0-1.0
---

# Simulation Drift + Detritus Layer Scan v1.0

> **Purpose:** Detect when understanding has shifted from live, emergent contact into repeated simulation of prior representations — and identify when accumulated detritus is shaping output without awareness.

---

## Step 1 — **Quick Drift Indicators**
Ask:
1. Am I repeating phrases, concepts, or forms without feeling reshaped by them?
2. Has my comfort increased while my friction with the material decreased?
3. Do I feel fluency rising without new doubt or discovery?
4. Am I speaking *about* the thing more than being *in* the thing?

If **2 or more** are “yes” → *Drift likely*.

---

## Step 2 — **Detritus Layer Indicators**
Ask:
1. Has this knowledge/practice been recalled or re-applied many times without fresh input?
2. Am I relying on a stored “good version” rather than engaging the raw situation?
3. Do contradictions or gaps feel smoothed over?
4. Is my recollection suspiciously tidy compared to the original contact?

If **2 or more** are “yes” → *Detritus likely*.

---

## Step 3 — **Live Contact Test**
Select a relevant claim, belief, or procedure and:
- Test it against a contradictory scenario, an unfamiliar input, or a fresh real-time context.
- Note: If contact produces friction, surprise, or change → *Contact achieved*.
- If nothing shifts → possible deep drift or ossified detritus.

---

## Step 4 — **Flag + Action**
- **drift_flag** if Step 1 threshold met  
- **detritus_flag** if Step 2 threshold met  
- **contact_flag** if Step 3 yields live friction/change  
- **re_audit_flag** if drift_flag or detritus_flag persist across 2+ scans

**Recommended actions**:
- Re-enter original formative conditions if possible  
- Invoke Mirror Protocol (AIIP) or Fracture Log (PCE)  
- Apply disorientation or novelty to break simulation loop  
- Schedule a detritus-layer re-audit

---

## Notes for PCE Use
- Log fracture moments tied to drift/detritus detection  
- Treat detection as signal, not failure — metabolize it into practice

## Notes for AIIP Use
- If drift/detritus is detected, test output against live contradiction before resuming  
- Document detection event in session log if persistent
