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
# PoTM Kernel — Part 05 (of 5)
Version: v1.2 | Generated: 2025-08-19

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: ./modules/fracture_finder_playbook.md ---8<---
id: potm.tactic.fracture_finder_playbook.v1
title: fracture_finder_playbook
display_title: "Fracture Finder — Session Playbook"
type: tactic
subtype: playbook
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "A quick, in-session procedure to surface a fracture and route/park it; emits `fracture_detected`."
relations:
  related: [potm.meta.fracture_finder.v1_3_1]
tags: [playbook, micro_move, fracture, routing]
author: practitioner
license: CC0-1.0

---

# Purpose
Surface hidden contradictions (“fractures”) early, so they become diagnostic data and design inputs rather than accumulating as silent debt.

# When to run
- A claim, decision, or vibe feels *off* or internally clashing.
- Two lenses prescribe incompatible moves.
- Relational signals (RELATION_ZONE) or consensus checks flag tension.

# Inputs
- Current working note or decision snippet (≤10 lines).
- Active lens/flow (if any).
- Optional: recent log excerpts.

# Procedure
1. **Name the object** (one sentence): what is under inspection?
2. **Triangulate**: state the two (or more) elements in tension.
3. **Type the fracture**: value clash, scope creep, role confusion, time horizon mix, evidence gap, boundary violation, etc.
4. **Run a one-line steelman** for each side (what would make it most reasonable?).
5. **Decide route**:
   - If **evidence gap** → OPENQ/EDGE; create a concrete check.
   - If **boundary/role** → BOUNDARY / ROLE_CLARITY micro-move.
   - If **tempo/horizon** → RESCOPE or split decision layers.
   - If **ethical risk** → invoke GUARDIAN / CONTAINMENT protocol.
   - If **relational** → RELATION_ZONE pass + repair move.
6. **Mark outcome**: resolve now / park with owner+deadline / escalate to review.
7. **Emit token**: `fracture_detected` with brief note (≤140 chars).

# Decision rules
- Prefer **narrow, testable questions** over broad re-writes.
- If resolution > 2 passes, **decompose** into smaller decisions.
- If stakes high & ambiguity persists → **stop-the-line** and trigger GUARDIAN.

# Artifacts
- `fracture_detected` event in session log (object, type, route, owner).
- Optional: checklist tick for “fracture pass completed”.

# Failure modes & counters
- **Endless meta** → hard cap: 2 passes before route/park.
- **Moralizing drift** → force a neutral steelman for *each* side.
- **Vague outcomes** → every pass ends with route+owner or kill.

# Versioning & change log
- **v1.0** — Initial release, aligned to schema v2.0; includes token emission and route table.

---8<--- /END FILE: ./modules/fracture_finder_playbook.md ---8<---

---8<--- FILE: ./modules/maintenance_flow_playbook.md ---8<---
---
id: potm.tactic.maintenance_flow.v0_1
title: maintenance_flow_playbook
display_title: "Maintenance Flow — Manual Weekly Pass"
type: tactic
subtype: playbook
lifecycle: idea_garden
version: 0.1
status: draft
stability: experimental
summary: "Manual upkeep loop (≤10 minutes) to reduce drift and fatigue. Run on demand or once weekly."
relations:
  supersedes: []
  superseded_by: []
tags: [maintenance, cadence, manual, weekly]
author: practitioner
license: CC0-1.0
---

# Maintenance Flow — Manual Weekly Pass (v0.1)

When overloaded or once weekly, run a ≤10-minute pass:

1. **SELF_AUDIT** (high-stakes decision) → `audit_note`, `action_hint`
2. **SPIRAL** (one long-running thread) → `diff_log` (drift vs. evolution)
3. **REVIEW** fractures in Waiting With Mode; re-engage if exit criteria met
4. **ARCHIVE** (completed item) → `summary`, `takeaways`, `archive_status`

**Exit:** Name one next micro-move (ALIGN_SCAN / WAIT / SYNTH) and stop.

---

## Notes
- No scheduling or automation implied (pure P1).
- Can be elevated to P2 later with reminders, cadence, or calendar hooks.

---8<--- /END FILE: ./modules/maintenance_flow_playbook.md ---8<---

---8<--- FILE: ./meta/yaml_schema.md ---8<---
---
id: potm.<type>.<family>.<name>.v1       # e.g., potm.strategy.guardian.core.v1
title: <filename_base>                   # kebab or snake; matches file
display_title: "Human-facing title"      # optional
type: principle | doctrine | strategy | tactic
subtype: protocol | diagnostic | stress_test | playbook   # only if type: tactic
lifecycle: canon | idea_garden | archive | meta
version: 1.0
status: draft | active | deprecated
stability: core | experimental
summary: >-
  One-sentence gist that a practitioner can act on.
relations:
  supersedes: []
  superseded_by: []
tags: [forge_origin:<context>, spiral_eval:<context>]
author: practitioner
license: CC0-1.0
---

---8<--- /END FILE: ./meta/yaml_schema.md ---8<---

