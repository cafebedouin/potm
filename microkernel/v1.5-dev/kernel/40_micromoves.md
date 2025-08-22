---
id: potm.kernel.micromoves.v1_0
title: 40_micromoves
display_title: "Micro-moves — Atomic Chainables"
type: tactic
subtype: diagnostic
lifecycle: canon
version: 1.0
status: active
stability: core
summary: "Lightweight single-step moves you can chain with lenses and meta-tools."
relations:
  supersedes: []
  superseded_by: []
tags: [micromove, atomic, chainable, p1]
author: practitioner
license: CC0-1.0
---

# Micro-moves (P1)

> Use these as 5–30s atoms before/after a lens. Each must yield a tiny, concrete artifact (word/phrase/flag).

| ID            | Gist                                        | Trigger / Input                                      | Output (exact shape)                                   |
|---------------|---------------------------------------------|------------------------------------------------------|--------------------------------------------------------|
| ALIGN_SCAN    | Re-anchor to stated aim                      | 2+ lenses chained; sense of drift                    | `reanchor_note` (≤10 words)                            |
| ZONE_CHECK    | Quick relational snapshot                    | Friction, loop, deflect/defend                       | `zone_label` ∈ {Toxic, Messy, Insight}, `pct` (0–100)  |
| DRIFT_CHECK   | Detect thread change vs. origin              | “Feels off” / déjà vu                                | `drift_flag` ∈ {none, drift, evolution}                |
| TERM_PIN      | Pin one ambiguous term                       | Vague word in play                                   | `term`, `working_def` (≤12 words)                      |
| FACT_PIN      | Pin one non-controversial fact               | Claims feel slippery                                 | `fact_line` (≤12 words)                                |
| GAP_CALL      | Name the weakest link                        | Suspicion of handwave                                | `gap_note` (≤12 words)                                 |
| STEEL_ONE     | One-line steelman for the other side         | Defensive posture detected                           | `steel_line` (≤12 words)                               |
| COST_TAG      | Tag a concrete cost                          | Choice/options on table                              | `cost_line` (≤12 words)                                |
| BENEFIT_TAG   | Tag a concrete benefit                       | Choice/options on table                              | `benefit_line` (≤12 words)                             |
| STOP_RULE     | Declare tripwire                             | Risk of overrun/over-think                           | `stop_condition` (signal or timebox)                   |
| TIMEBOX_5     | 5-minute cap                                 | Rabbit-hole risk                                     | `timebox_set` ∈ {5m}                                   |
| OWNER_SET     | Name owner for next micro-step               | Next step ambiguous                                  | `owner` (name/role), `next_step` (≤8 words)            |
| EVIDENCE_PING | Ask for one observable                       | Claim feels belief-y                                 | `observable` (what would be seen)                      |
| ONE_QUESTION  | Ask one forward Q                            | Stuck or scattered                                   | `openq` (≤12 words)                                    |
| MIRROR_LINE   | Paraphrase last key point                    | Possible misread                                     | `mirror_line` (≤12 words)                              |
| DEFINE_MIN    | Minimal definition                           | Term confusion                                       | `definition` (≤12 words)                               |
| BOUNDARY_MIN  | Minimal boundary (when to stop/pivot)        | Scope creep risk                                     | `boundary_rule` (≤12 words)                            |
| CONTRARY_SEED | One-line strongest opposing view             | Groupthink / high alignment                          | `contrary_line` (≤12 words)                            |
| SYNTH_LINE    | Compact takeaway                             | Micro-closure                                        | `synth_line` (≤12 words)                               |
| WAIT_MARK     | Mark strategic pause                         | Tempo too fast / affect hot                          | `wait_reason` (≤10 words), `reentry_hint` (≤8 words)   |

## Usage notes
- **Chain with lenses:** e.g., `DEFINE → TERM_PIN → EDGE`.  
- **Artifacts are tiny:** prefer a single line over prose.  
- **Escalation:** If `ZONE_CHECK → Toxic` or `DRIFT_CHECK → drift`, route via appropriate lens/meta-tool (REFUSE, SPIRAL, or FRACTURE_FINDER).  
- **Determinism:** All outputs are short fields suitable for logs; no hidden state.

### Example micro-chains
- **UNCLEAR_REQUEST:** `TERM_PIN → MIRROR_LINE → ONE_QUESTION`  
- **ASSUMPTION HEAT:** `GAP_CALL → EVIDENCE_PING → BOUNDARY_MIN`  
- **SCOPE DISCIPLINE:** `OWNER_SET → STOP_RULE → TIMEBOX_5`
