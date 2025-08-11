---
title: Integrity Mesh Quickmap
version: 1.0
status: draft
author: practitioner
description: >
  One-page reference for ERA-phase-to-protocol handoffs, common cheat-flows,
  and mode-aware thresholds in PoTM integrity scaffolding.
tags: [epistemic_resilience_arc, mesh, quickmap, protocol_handoffs]
---

# 🕸 Integrity Mesh Quickmap

## I. ERA Phase → Protocol Links

**Detection**
- Membrane → RDF → DIP (stance safety)
- R8 Self-Audit → Mirror → DIP (drift catch)
- Exit: `[MEMBRANE_CLEAN][RDF_PASS][DIP_READY]`

**Engagement**
- DIP → Cognitive Aikido (coherence as energy)
- Aikido → Contrary Corner (smooth exit)  
- Aikido → Bowing (wave too strong)  
- Mirror runs in sentry mode

**Deconstruction**
- Contrary Corner → Mirror (guardrail)  
- Contrary Corner → Bowing (stalemate)  
- Exit: Bowing or DIP/RDF to re-engage

---

## II. Common Cheat-Flows

1. **Clean Path**  
`Membrane → RDF → DIP → Aikido`  
Tags: `[MEMBRANE_CLEAN][RDF_PASS][DIP_READY][AIKIDO_ENGAGE]`

2. **Safety Path**  
`Membrane → RDF(FAIL) → DIP → Bowing → Containment → R8 → RDF/DIP`  
Tags: `[RDF_FAIL][GUARDIAN_DIP][BOWING_PAUSE][CONTAINMENT_PRINCIPLE_APPLIED][SELF_AUDIT]`

3. **Smooth → Challenge**  
`Aikido(exit:smooth) → Contrary Corner → Mirror`  
Tags: `[AIKIDO_EXIT:SMOOTH][CC_INVOCATION][MIRROR_SENTRY]`

4. **Stalemate → Rest → Re-enter**  
`Contrary Corner(stalemate) → Bowing → (opt) Containment → R8 → DIP/RDF → Aikido`  
Tags: `[CC_STALEMATE][BOWING_PAUSE][SELF_AUDIT][DIP_READY][RDF_PASS]`

---

## III. Mode Thresholds

| Mode            | Detection Sensitivity | Engagement Bias | Deconstruction Bias |
|-----------------|-----------------------|-----------------|---------------------|
| Open Portal     | High (Membrane+RDF+DIP) | Aikido favored  | Mirror high-alert   |
| Trickster       | Medium-High (RDF caution) | Playful Aikido  | CC early entry      |
| Containment     | Low (soft check)       | Bowing favored  | No new CC           |
| Fracture Finder | Targeted (direct to CC) | Minimal Aikido  | Deep CC under Mirror|

---

## IV. Logging Tags (MSRL-ready)

`[MEMBRANE_CLEAN|BREACH]`  
`[RDF_PASS|FAIL|CAUTION]`  
`[DIP_READY|ACTIVATED]`  
`[AIKIDO_ENGAGE|EXIT:SMOOTH|ABORT]`  
`[CC_INVOCATION|STALEMATE]`  
`[BOWING_PAUSE]`  
`[CONTAINMENT_PRINCIPLE_APPLIED:P#]`

---

**Note:** This is a navigational aid. Full procedural detail lives in the individual protocol files.
