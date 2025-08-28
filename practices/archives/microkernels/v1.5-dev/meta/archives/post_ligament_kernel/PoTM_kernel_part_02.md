---
id: potm.kernel.v1_2_1
title: potm_bootpack_kernel
display_title: "PoTM Boot Pack Kernel v1.2.1 (Single-File, P1)"
type: kernel 
lifecycle: canon
version: 1.2.1
status: active
stability: core
summary: "Self-contained P1 kernel with embedded bridge, validator, and deck data. No external authority required."
relations:
  supersedes: [potm.kernel.v1_2]
  superseded_by: []
tags: [kernel, bootpack, reference, P1, single_file]
author: practitioner
license: CC0-1.0
---
# PoTM Kernel — Part 02 (of 8)
Version: v1.2 | Generated: 2025-08-20

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: kernel/30_lenses_p1.md ---8<---
## Lenses

| ID             | Gist                                       | Core Output                                                        |
|----------------|--------------------------------------------|--------------------------------------------------------------------|
| EDGE           | Sharpen padded points                      | One concise claim and its direct implication                       |
| INTUIT         | Voice a tentative pattern                  | A hunch with confidence level, a probe, and a confirming signal    |
| OPENQ          | Drive with real questions                  | 2–3 forward questions to open new terrain                          |
| MIRROR         | Reflect to confirm understanding           | A paraphrase with a prompt to confirm or repair                    |
| DEFINE         | Disambiguate key terms                     | A clear definition with an illustrative example                    |
| FACTS          | Gather minimal anchors                     | Bulleted facts list + one data gap                                 |
| CHECK          | Test a key assumption                      | The assumption, a minimal test plan, and expected outcome          |
| TRACE          | Surface reasoning steps                    | A 2–4-step chain with a flagged uncertainty                        |
| BOUNDARY       | Define tripwires & falsifiers              | 1–2 signals, stop/pivot conditions, and monitor cadence            |
| CONTRARY       | State the strongest opposing view          | One-line counter + cost/benefit                                    |
| FORGE          | Make it work once minimally                | A 3-step plan with owner, date, and success marker                 |
| SYNTH          | Compact takeaway                           | A concise synthesis and one next action                            |
| SPIRAL         | Review trajectory over time                | `diff_log` marking drift (unintended) vs. evolution (deliberate)   |
| ARCHIVE        | Conclude and log a completed cycle/project | `summary`, `takeaways`, and `archive_status` (`resolved`/`parked`/`stalled`) |
| WAIT           | Strategic pause                            | Watch signals, a review date, and re-entry criteria                |
| REFUSE         | Block requests that breach constraints     | A brief refusal with a safe alternative suggestion                 |
| RELATION_ZONE  | Locate relational dynamics on 3-zone gradient | `zone_label` (Toxic/Messy/Insight), `percentage_estimate`        |
| META_CONFLICT  | Resolve Formal vs. Interpretive clashes    | Route as `meta_fracture` → FRACTURE_FINDER → SYNTH                 |

### RELATION_ZONE Details

- **Trigger:** Friction, repeated deflect/defend, or slip from truth-seeking.
- **Outputs:** `[zone_label, percentage_estimate]`
- **Examples:**
  - “Team meeting with repeated deflect/defend → Messy Zone (60%).”
  - “Facts are denied outright → Toxic Zone (5%).”
  - “Collaborative truth-seeking → Insight Zone (95%).”
- **Cautions:**
  - `assumption_check`: Verify zone label—Toxic Zone requires containment.
  - `practitioner_safety`: If in Toxic Zone (0–10%), prioritize exit/containment.
- **Thresholds:** Toxic **0–10%**, Messy **10–90%**, Insight **90–100%** (default split; override only with explicit rationale).
- **Hybrid Note:** In Messy Zone (10–90%), use hybrid tools (e.g., Drift-Tolerant Waiting) to hold ambiguity and map drifts.

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

## Common Scenarios → Tool Chains

| Scenario             | Trigger                                    | Chain                                                          |
|----------------------|--------------------------------------------|----------------------------------------------------------------|
| UNCLEAR_REQUEST      | Vague/ambiguous ask                        | DEFINE → MIRROR → OPENQ                                        |
| STUCK_LOOP           | Repetition or circular debate              | DRIFT_CHECK → ZONE_CHECK → (Messy) WAIT ∥ (CONTRARY)           |
| COMPLEX_CLAIM        | Dense or layered argument                  | EDGE → TRACE → CHECK                                           |
| DEFENSIVE_PUSHBACK   | Pushback, blame-shifting, justification     | RELATION_ZONE → (Toxic) REFUSE ∥ (Messy) MIRROR + CONTRARY      |

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

## Unskillfulness
See BU beacon for handling rough answers.

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

---8<--- /END FILE: kernel/30_lenses_p1.md ---8<---

