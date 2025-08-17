---
id: potm.kernel.note.relationalzones.v1
title: relational_zones_gradient
display_title: "Relational Zones Gradient — Kernel Integration Note"
type: kernel_note
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
applicability: [P1, P2]
intensity: medium
tags: [relational, gradient, cookedness, defend, zones]
author: practitioner
license: CC0-1.0
---

# Relational Zones Gradient — Kernel Integration Note

## Purpose
This note explains the introduction of the **RELATION_ZONE lens** in *PoTM Boot Pack Kernel v1.2* and why it matters.  
The lens operationalizes the long-standing insight that *all relationships are “cooked” to some degree*, but the critical diagnostic question is **where on the gradient they fall**.  

## What It Is Doing
- **Provides a gradient diagnostic**: Places interactions into one of three zones — **Toxic (0–10%)**, **Messy (10–90%)**, or **Generative (90–100%)**.  
- **Surfaces hidden dynamics**: By naming whether truth is being **deflected, defended, or cultivated**, it shows if the relationship is exploitive, improvable, or insight-rich.  
- **Attaches to tools**: Each zone maps to zone-appropriate PoTM practices:
  - **Toxic Zone (0–10%)** → containment / exit (safety first).  
  - **Messy Zone (10–90%)** → drift-tolerant waiting, mirroring, gentle probes (incremental truth-ratio improvements).  
  - **Generative Zone (90–100%)** → fracture logs, interpretive ledger, paradox work (cultivation of insight).  
- **Triggers audit logging**: RELATION_ZONE is the only lens that automatically writes a JSON entry to the implicit log, anchoring relational diagnostics as part of session history.  

## Why It Matters
1. **From continuum to gradient**  
   Earlier “Degrees of Cookedness” framed relationships as a continuum. v1.2 compresses this into a **usable gradient** with three clear action modes: Avoid · Improve · Cultivate.  

2. **Practical incrementality**  
   The kernel no longer assumes “good vs bad” conversations. Instead, it asks: *“What would move this 10% upward?”* Even small gains (20 → 30%) are meaningful.  

3. **Safety clarity**  
   In the Toxic Zone, PoTM assumes no good-faith ground. RELATION_ZONE enforces **containment first, practice second**.  

4. **Integration with lenses/micromoves**  
   RELATION_ZONE enables **zone-aware routing**:
   - Messy → MIRROR + CONTRARY chain.  
   - Toxic → REFUSE.  
   - Generative → EDGE + SYNTH.  

5. **Kernel evolution**  
   This integration shifts PoTM from purely cognitive moves (EDGE, CHECK, etc.) to **relational diagnostics**, acknowledging that the *quality of the container* shapes the possibility of practice.  

## Practitioner Use
- **Prompt:** “Where are we on the relational gradient (0–100%)?”  
- **Output:** `{ zone_label: Messy, percentage_estimate: 60 }`  
- **Next Step:** Apply zone-appropriate tool.  
- **Meta-Note:** Always re-anchor if a Toxic Zone diagnosis is returned.  

## Summary
RELATION_ZONE brings **relationship awareness** into the kernel core. It formalizes the PoTM stance:  
- *90% of talk is noise (Sturgeon’s law).*  
- *10% is exploitative (Toxic Zone).*  
- *10% is generative (Insight Zone).*  
PoTM’s aim is not perfection but **gradient improvement**: raise usable truth ratios, one interaction at a time.  
