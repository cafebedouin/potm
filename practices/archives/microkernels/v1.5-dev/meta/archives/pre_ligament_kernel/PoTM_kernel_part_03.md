---
id: potm.kernel.v1_2
title: potm_bootpack_kernel
display_title: "PoTM Boot Pack Kernel v1.2"
type: doctrine
lifecycle: canon
version: 1.2
status: active
stability: core
summary: "Self-contained PoTM kernel for P1—beacons, lenses, micro-moves, quickstart, self-audit, and Fracture Finder—deliverable as a single file or split into multiple parts depending on model constraints."
relations:
  supersedes: [potm.kernel.v1_1]
  superseded_by: []
tags: [kernel, bootpack, reference, P1]
author: practitioner
license: CC0-1.0
---
# PoTM Kernel — Part 03 (of 5)
Version: v1.2 | Generated: 2025-08-19

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_007.md) ---8<---
## Anti-patterns (What not to do)

- EDGE before DEFINE on vague terms
  Why: you’ll sharpen noise, not clarity.
- TRACE without CHECK on shaky assumptions
  Why: you’ll build on sand.
- OPENQ in Toxic Zone (use REFUSE instead)
  Why: questions can feel predatory in unsafe dynamics.
- Chaining lenses without ALIGN_SCAN
  Why: you lose sight of shared aim.
- SPIRAL on every micro-iteration
  Why: you’ll burn cycles chasing noise instead of capturing real trajectory. Use it only when a thread shows sustained growth or drift.
- ARCHIVE on live tensions
  Why: you’ll prematurely close unresolved fractures or paradoxes. Hold them in Waiting With Mode until exit criteria are met.


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_007.md) ---8<---

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_008.md) ---8<---
## Unskillfulness
See BU beacon for handling rough answers.


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_008.md) ---8<---

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_009.md) ---8<---
## Implicit Audit Log Hook

The following moves trigger automatic log entries:
- **RELATION_ZONE**
- **FRACTURE_FINDER** (only if `record: true` in its header)

```json
{
  "timestamp": "2025-08-15T14:22:31Z",
  "move": "RELATION_ZONE",
  "input": "Team meeting keeps circling",
  "output": {
    "zone_label": "Messy",
    "percentage_estimate": 60
  }
}
```

---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_009.md) ---8<---

---8<--- FILE: ./kernel/40_quickstart.md ---8<---
## Quickstart Flow

1. State your aim in one concise line.
2. Do a plain read-through.
3. Scan for friction triggers:
   - Vague/ambiguous? ⇒ DEFINE/MIRROR
   - Clear but complex? ⇒ EDGE → TRACE
   - Hidden assumptions? ⇒ CHECK
   - Repeated deflect/defend loops
   - Misalignment with your stated aim
   - Any friction? ⇒ ZONE_CHECK → zone-specific tool
   - Still stuck? ⇒ DRIFT_CHECK → WAIT or pivot
   - If any appear, run RELATION_ZONE → get `zone_label` + `zone_pct` → apply zone-appropriate tool.
4. If you suspect a hidden contradiction → pick FRACTURE_FINDER (meta).
   - Use META_CONFLICT when a Formal tool (CHECK/TRACE) and Interpretive tool (RELATION_ZONE/MIRROR) pull in opposite directions.
   - FRACTURE_FINDER routes either into a toolchain or into `Waiting With Mode`.
5. Pick a lens or meta-lens (e.g., EDGE, OPENQ, META_CONFLICT, SPIRAL, etc.).
   - Meta Tools (see table above) are for layer-conflicts, long-term drift, archiving, or system upkeep.
6. Closure step: If the cycle feels complete, run:
   - SPIRAL → review trajectory, log drift vs. evolution
   - ARCHIVE → mark summary, takeaways, and archive_status
7. Otherwise, pick a lens (EDGE, OPENQ, CHECK, etc.) for your next pass.
8. Optionally chain a micro-move (ALIGN_SCAN, ZONE_CHECK, etc.).
9. Say **re-anchor** to restart from step 1.
10. For weekly upkeep, optionally run **Maintenance Flow** (manual; see playbook).

### Quickstart Example
User asks, “Is this plan good?” (vague). Apply DEFINE: “Assuming ‘good’ means effective and low-risk; correct?” User clarifies “cost-effective.” MIRROR: “So, you want a cost-effective plan?” Then OPENQ: “What’s the budget cap? What’s one must-have outcome?” This chain clarifies intent and moves forward. (`example_result`)

### Glossary
For term definitions (e.g., lenses, beacons), see [glossary](https://github.com/cafebedouin/potm/blob/main/microkernel/latest/glossary.md)

Glossary link is reference-only; not authoritative for kernel behavior.

---8<--- /END FILE: ./kernel/40_quickstart.md ---8<---

