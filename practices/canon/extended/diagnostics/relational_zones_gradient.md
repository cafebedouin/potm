---
id: potm.diagnostic.relationalzones.v1
title: relational_zones_gradient
display_title: "Relational Zones Gradient"
type: diagnostic
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: potm.kernel.v1_2
  practitioner_doc: modules/diagnostics/relational_zones_gradient.md
  supersedes: []
  superseded_by: []
interfaces: [lenses, micro_moves, diagnostics]
applicability: [P1, P2, P3]
intensity: medium
tags: [relational, gradient, cookedness, defend, zones]
author: practitioner
license: CC0-1.0
---

# Relational Zones Gradient

## Purpose
To provide a **diagnostic taxonomy of relationships** based on the handling of truth, distortion, and defensiveness.  
This gradient distills the *Degrees of Cookedness* and *Deflect & Defend* concepts into a **three-zone model** practitioners can use in real time.  

The question is never *whether* relationships are cooked — they all are. The question is *how cooked*, and whether the distortions are **toxic, improvable, or generative**.

---

## The Gradient

### 1. Toxic Zone (0–10%)
- **Nature:** Exploitative, extractive, or manipulative.  
- **Mode:** *Cooked Books* — truth systematically overwritten by agenda.  
- **Behaviors:** Gaslighting, blame inversion, chronic deflect & defend.  
- **PoTM Role:** **Containment** — diagnose early, exit or protect.  
- **Practitioner Prompt:** *“Am I safe to practice here?”*  

### 2. Messy Zone (10–90%)
- **Nature:** Ordinary ego-games and status maneuvering.  
- **Mode:** *Deflect & Defend as default.* Truth slips, but repair possible.  
- **Behaviors:** Justifications, small lies, avoidance, inconsistent trust.  
- **PoTM Role:** **Improvement** — raise usable truth ratio incrementally.  
- **Practitioner Prompt:** *“What would move this 10% upward?”*  

### 3. Generative Zone (90–100%)
- **Nature:** Conversations where truth and distortion are worked with openly.  
- **Mode:** *Interpretive Ledger* — even errors become data for growth.  
- **Behaviors:** Truth welcomed, friction cultivated, distortions named together.  
- **PoTM Role:** **Cultivation** — deepen insight, log fractures, explore paradox.  
- **Practitioner Prompt:** *“What’s the insight hiding in this friction?”*  

---

## Zone Shifts
- **Toxic → Messy:** Identify distortion explicitly (“This feels unsafe; let’s pause”).  
- **Messy → Generative:** Surface one small avoided truth.  
- **Generative → Sustained:** Use Fracture Logs, Edge/Contrary chains, or paradox work.  

---

## Integration with Kernel
- Implemented as the **RELATION_ZONE lens** in `potm_bootpack_kernel.md v1.2`.  
- Output: `{ zone_label, percentage_estimate }`.  
- Linked to **ZONE_CHECK** micro-move.  
- Only lens that **auto-logs JSON entries** in the implicit audit trail.  

---

## Practitioner Use
1. **Run ZONE_CHECK** when friction or deflect/defend loops appear.  
2. **Get output:** e.g. `Messy Zone (60%)`.  
3. **Apply zone-appropriate tool:**  
   - Toxic → REFUSE or exit.  
   - Messy → MIRROR + CONTRARY.  
   - Generative → EDGE + SYNTH.  
4. **Repeat:** Ask, *“What would move this 10% upward?”*  

---

## Why It Matters
- **Clarifies safety:** not all contexts are suitable for practice.  
- **Avoids binary thinking:** moves from *good/bad* to *gradient*.  
- **Anchors progress:** even small shifts (20 → 30%) count as real improvement.  
- **Honors Sturgeon’s Law:** 90% of interactions are noise, but the usable 10% can be cultivated.  

---

## Lineage
- **Forge Origin:** Degrees of Cookedness continuum (cooked vs raw).  
- **Spiral Evaluation:** Deflect & Defend overlay → three-zone taxonomy.  
- **Integration:** RELATION_ZONE lens, Boot Pack Kernel v1.2.  

---

**Tagline:** *All relationships are cooked. PoTM helps you climb the gradient.*  
