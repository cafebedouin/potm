---
id: potm.kernel.notes.framework.v1
title: kernel_integration_notes_framework
display_title: "Kernel Integration Notes — General Framework"
type: kernel_guideline
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: potm.kernel.v1_2
  practitioner_doc: meta/kernel_integration_notes_guide.md
  supersedes: []
  superseded_by: []
interfaces: [kernel, meta, lineage]
applicability: [P1, P2, P3]
intensity: gentle
tags: [kernel, integration, notes, lineage]
author: practitioner
license: CC0-1.0
---

# Kernel Integration Notes — General Framework

## Purpose
Kernel integration notes document **why and how new elements enter the kernel**, serving as the bridge between:
- **Kernel invariants** (what must hold true at all times), and  
- **Practical evolution** (new lenses, beacons, micro-moves, diagnostics).  

They ensure the **forge → spiral lineage** remains visible, so changes are not just applied but **contextualized**.

---

## What They Do
1. **Explain rationale**  
   - Why this change exists.  
   - What problem it solves or what gap it closes.  

2. **Anchor placement**  
   - Where in the kernel it lives (lens, beacon, micro-move, diagnostic).  
   - How it interfaces with existing components.  

3. **Frame practice impact**  
   - How practitioners should use it.  
   - What risks or cautions to note.  

4. **Preserve lineage**  
   - Links to prior versions, draft stubs, or experimental notes.  
   - “This supersedes X; spiral_eval: Y.”  

---

## Where They Live
- **Default path:** `kernel/notes/`  
- Each integration note lives alongside the kernel file it extends (e.g., `potm_bootpack_kernel.md`).  
- Naming convention: `<feature>_integration_note.md` (e.g., `relational_zones_gradient.md`).  

> **Alternative:** If heavily conceptual, integration notes may live under `meta/` with a short pointer file in `kernel/notes/`.  

---

## Structure of an Integration Note
Each note should contain:

1. **Front-matter** (standard schema)  
   - Links to kernel version, supersedes/superseded_by.  
   - Interfaces touched (beacons, lenses, diagnostics).  

2. **Purpose**  
   - Why this feature was added.  

3. **What It Is Doing**  
   - Short operational description.  
   - Where it hooks into the kernel.  

4. **Why It Matters**  
   - Broader rationale: epistemic integrity, practitioner clarity, safety.  

5. **Practitioner Use**  
   - Concrete prompts or outputs.  
   - Zone mapping if relevant.  

6. **Lineage / Evolution**  
   - What draft or idea it originated from.  
   - How it differs from prior approaches.  

---

## Example (Abstracted)
- **Feature:** New lens `RELATION_ZONE`  
- **Purpose:** Add relational diagnostics to kernel, to locate conversations on the cookedness gradient.  
- **Doing:** Provides 0–100% zone label, logs outputs, routes to zone-appropriate tools.  
- **Matters:** Shifts PoTM from purely cognitive discipline to relational awareness.  
- **Use:** “Where are we on the relational gradient?”  
- **Lineage:** Originated in cookedness diagnostic + deflect/defend overlay; spiral_eval: integrated by Le Chat review.  

---

## Benefits
- **Transparency:** Practitioners know *why* each kernel element exists.  
- **Auditability:** Easy to trace kernel evolution over versions.  
- **Safety:** Guards against silent drift (features added without rationale).  
- **Practicality:** Provides a “why” file practitioners can consult without cluttering the kernel itself.  

---

## Summary
Kernel integration notes are the **story behind the code**:  
- They keep PoTM honest to its own principles of clarity, assumption-surfacing, and drift detection.  
- They ensure practitioners understand both **what changed** and **why it matters**.  
- They give future maintainers the tools to decide whether to **keep, revise, or prune** features.  

**Tagline:** *Every kernel change deserves a rationale. Notes keep the lineage alive.*
