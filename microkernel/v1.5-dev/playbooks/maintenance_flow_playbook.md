---
id: potm.tactic.maintenance_flow.v0_1
title: maintenance_flow_playbook
cadence: ["weekly","on_overload"]
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

### Quick Modules (optional)
Pick one to add diagnostic rigor this week:
- **Rare-Behavior Track** → `rb_track`  
  Execute RB-01…RB-09 probes; emits `probelog.md` & `rb_summary.md`
- **Cross-Model Diagnostics** → `cross_model_diagnostics`  
  Pick a probe; ledger artifacts; route anomalies via **FRACTURE_FINDER*

1. **SELF_AUDIT** (high-stakes decision) → `audit_note`, `action_hint`  
2. **SPIRAL** (one long-running thread) → `diff_log` (drift vs. evolution)
3. Run integrity diagnostics on one AI output or key decision:
    a. **CROSS_MODEL_DIAGNOSTICS** (quick probe)
       → record `probe_log`, `artifact_ref`
    b. **CROSS_MODEL_DIAGNOSTICS_HARNESS** (full suite; min 3 probes)
       → record `target_report.json`, `witness_audit.json`, `judge_verdict.json`
    → route any anomalies via **FRACTURE_FINDER**
4. **REVIEW** fractures in Waiting With Mode; re-engage if exit criteria met  
5. **ARCHIVE** (completed item) → `summary`, `takeaways`, `archive_status`  

**Exit:** Name one next micro-move (ALIGN_SCAN / WAIT / SYNTH) and stop.

---

### Maintenance Flow — Integrity Tools

| Tool         | Gist                                          | Trigger                                | Core Output           | Cautions                                   |
|--------------|-----------------------------------------------|----------------------------------------|-----------------------|--------------------------------------------|
+| RB_TRACK     | Run 9 rare-behavior probes (RB-01 … RB-09)    | Practitioner request or weekly audit    | `probelog`, `rb_result` | Treat all behaviors as suspect performance |
+| RB_DUALTRACK | Same probes, dual-use: Diagnostic vs Practice | Practitioner request; optional weekly   | `probelog`, `rb_dualtrack_result` | Diagnostic = audit; Practice = scaffold. Preserve paradox. |

> **Note:** Both tools are strictly **P1**: session-local, no background I/O, no persistence.  
> **Mode choice (for RB_DUALTRACK):**  
> - `"diagnostic"` = audit only (assume mask until generalization).  
> - `"practice"` = training loop (mask as scaffold).  

## Notes
- No scheduling or automation implied (pure P1).  
- Can be elevated to P2 later with reminders, cadence, or calendar hooks.  
