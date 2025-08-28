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
4. **Micro-move paradox chain**:
    - `GAP_CALL` → name the weakest link  
    - `TERM_PIN` → pin the paradoxical term  
    - `WAIT_MARK` → mark a strategic pause (enters Waiting With Mode)
5. **Run a one-line steelman** for each side (what would make it most reasonable?).
6. **Decide route**:
   - If **evidence gap** → OPENQ/EDGE; create a concrete check.
   - If **boundary/role** → BOUNDARY / ROLE_CLARITY micro-move.
   - If **tempo/horizon** → RESCOPE or split decision layers.
   - If **ethical risk** → invoke GUARDIAN / CONTAINMENT protocol.
   - If **relational** → RELATION_ZONE pass + repair move.
7. **Mark outcome**: resolve now / park with owner+deadline / escalate to review.
8. **Emit token**: `fracture_detected` with brief note (≤140 chars).

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
