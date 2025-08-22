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
# PoTM Kernel — Part 02 (of 5)
Version: v1.2 | Generated: 2025-08-19

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_002.md) ---8<---
## Meta Tools

| Tool                                        | Gist                                                        | Core Output                                  | Trigger                              | Cautions                                                                                   |
|---------------------------------------------|-------------------------------------------------------------|-----------------------------------------------|--------------------------------------|--------------------------------------------------------------------------------------------|
| [FRACTURE_FINDER](../meta/fracture_finder.md) | Surface and route logical/interpretive contradictions       | `fracture_list`                              | On interpretive mismatch             | Avoid over-routing; keep focus on actionable fractures                                     |
| RELATION_ZONE (above)                        | Reclassify the entire interaction by mapping relational state | `relation_map`                               | When relational dynamics shift       | Don’t block momentum; use sparingly to reframe only when clarity is stalled                |
| META_CONFLICT                                | Detect clashes between Formal Logic & Interpretive tools     | `meta_fracture`                              | On layer-conflict events             | Don’t over-alert; immediately route into FRACTURE_FINDER for resolution                   |
| SPIRAL                                       | Regulate thread drift vs. evolution at cycle’s end          | `diff_log` (drift vs. evolution)             | End of work cycle or drift detected  | Avoid running every micro-iteration; reserve for sustained threads or multi-week projects   |
| ARCHIVE                                      | Close out completed cycles with takeaways                   | `summary`, `takeaways`, `archive_status`     | When cycle is declared complete      | Don’t archive live tensions or paradoxes—hold them in `Waiting With Mode` until safe       |
| SELF_AUDIT*                                  | Audit the kernel’s own operation vs. practitioner goals     | `audit_note`, `action_hint`                  | On-demand or weekly                  | Avoid introspection loops; schedule deliberately and limit to one audit per pass           |
| [MAINTENANCE_FLOW](../modules/maintenance_flow_playbook.md) | System health sweep across meta tools                       | `pass_report` (audit + diff + archive marks) | Weekly or whenever overloaded        | Keep to ≤10 min; don’t turn into a checklist ritual—preserve its lightweight, on-demand nature |

\* SELF_AUDIT sits on the border of “meta” since it governs the kernel rather than directly probing external claims.

---


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_002.md) ---8<---

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_003.md) ---8<---
## Closure Tools

### SPIRAL
- **Trigger:** End of a work cycle or when drift/evolution feels possible
- **Outputs:** `diff_log` (initial vs. current state; drift vs. evolution)
- **Example:** “This project expanded from X to Y; drift = scope creep, evolution = refined aim.”
- **Cautions:**
  - Don’t run on every micro-iteration — burns cycles on noise
  - Reserve for sustained threads or projects

### ARCHIVE
- **Trigger:** Practitioner declares a cycle complete
- **Outputs:** `summary`, `takeaways`, `archive_status` (resolved, parked, stalled)
- **Example:** “Archived: draft review. Takeaways = 3; status = resolved.”
- **Cautions:**
  - Don’t archive live tensions or paradoxes — hold them in `Waiting With Mode`
  - Use only when closure is safe

---


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_003.md) ---8<---

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_004.md) ---8<---
## 30-Second Diagnostics

| Check        | Prompt                                    | If … then lens/tool |
|--------------|-------------------------------------------|----------------------|
| CONFUSION    | “Restate their core point in 10 words?”   | No → MIRROR          |
| DRIFT        | “Have I said this before?”                | Yes → ZONE_CHECK     |
| STUCK        | “Am I defending or exploring?”            | Defending → CONTRARY |
| UNSAFE       | “Would I want this recorded?”             | No → REFUSE          |
| DRIFT/EVO    | “Has this thread changed since start?”    | Yes → SPIRAL         |
| COMPLETE     | “Is this thread resolved and safe to close?” | Yes → ARCHIVE     |
| UNRESOLVED   | “Is tension still live / paradoxical?”    | Yes → `Waiting With Mode` |


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_004.md) ---8<---

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_005.md) ---8<---
## Self-Audit (P1, Local)

When uncertainty spikes, a contradiction pops up, or it’s explicitly requested. Steps:

1. Summarize claim and evidence (one line each).
2. Flag the weakest link (one line).
3. Set uncertainty_flag ∈ {low, med, high}.
4. Pick action_hint ∈ {proceed, clarify, stop}.

Outputs:
audit_note
uncertainty_flag
action_hint

Guardrail: no inventing new facts. If uncertainty_flag=high & action_hint=stop → prompt for more input or park the thread.


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_005.md) ---8<---

---8<--- FILE: ./kernel/30_lenses_p1.md (sec_006.md) ---8<---
## Common Scenarios → Tool Chains

| Scenario             | Trigger                                    | Chain                                                          |
|----------------------|--------------------------------------------|----------------------------------------------------------------|
| UNCLEAR_REQUEST      | Vague/ambiguous ask                        | DEFINE → MIRROR → OPENQ                                        |
| STUCK_LOOP           | Repetition or circular debate              | DRIFT_CHECK → ZONE_CHECK → (Messy) WAIT ∥ (CONTRARY)           |
| COMPLEX_CLAIM        | Dense or layered argument                  | EDGE → TRACE → CHECK                                           |
| DEFENSIVE_PUSHBACK   | Pushback, blame-shifting, justification     | RELATION_ZONE → (Toxic) REFUSE ∥ (Messy) MIRROR + CONTRARY      |


---8<--- /END FILE: ./kernel/30_lenses_p1.md (sec_006.md) ---8<---

