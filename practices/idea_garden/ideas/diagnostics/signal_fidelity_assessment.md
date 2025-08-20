---
id: potm.proto.meta.signal_fidelity_assessment.v1_0
title: signal_fidelity_assessment_v1.0
display_title: "Signal Fidelity Assessment"
type: diagnostic
status: draft
version: 1.0
stability: experimental
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [practice_validation, drill_effectiveness, context_control, noise_filter]
applicability: [P2, P3, P4]
intensity: medium
preconditions: ["Perceived effect or 'signal' from a practice has emerged", "Practitioner is considering declaring the practice effective"]
outputs: [fidelity_matrix, conclusion_grade]
cadence: ["pre-publication: before declaring new practice effective", "after early signs of signal but before rollout"]
entry_cues: ["Was that real?", "Did this actually cause the shift?", "What else could explain this?"]
safety_notes: ["Distinguish causality from correlation. Fidelity tests protect against self-deception."]
tags: [signal_validation, placebo_control, fidelity_test, forge_origin:self, spiral_eval:drill_filtering]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Assess whether a signal attributed to a PoTM practice is **genuine and repeatable**, or the result of placebo, contextual bleed, mood bias, or other confounds. This protocol supports epistemic rigor in determining what "works."

## When to Run

- Before declaring a practice “effective” or adding it to the mainline deck.
- After a perceived shift occurs during or after practice use.
- When signal attribution is unclear or suspect.

## Inputs

- The practice in question (card, protocol, or move).
- Session logs or experiential notes from at least 3–5 instances.
- Observable outcome or shift claimed as signal.

## Procedure

1. **Define Target Signal:** What is the hypothesized change? Be precise (e.g. clarity, regulation, frame shift).

2. **Create Context Grid:** List internal and external variables potentially affecting outcome:
   - Mood
   - Sleep
   - Conversation topic
   - Recent conflict, caffeine, novelty

3. **Apply Cross-Context Replication:** Run the practice across at least 3 contrasting contexts.

4. **Blind Where Possible:** Randomize order or insert control moves (e.g. inert card, reversed cue).

5. **Log Negative Controls:** Run sessions where the practice is omitted but context is similar.

6. **Construct Fidelity Matrix:** Mark signal presence/absence across different contexts and controls.

7. **Assign Conclusion Grade:**
   - A = Reliable signal with low context dependence
   - B = Weak but promising signal with some bleed
   - C = Noisy or ambiguous
   - D = Likely artifact
   - F = No effect or regress

## Decision Rules

- **Grade A–B:** Consider promotion to full protocol status (log justification).
- **Grade C–D:** Rework or pause; needs more testing.
- **Grade F:** Retire or archive with notes.

## Artifacts

- `fidelity_matrix`: grid mapping signal to conditions and controls.
- `conclusion_grade`: A–F rating with one-sentence rationale.

## Failure Modes & Counters

| Mode                               | Countermeasure                                      |
|------------------------------------|-----------------------------------------------------|
| Declaring victory after a good day | Require negative control sessions and multiple trials |
| Over-indexing to single mood       | Test in fatigue, tension, distraction, etc.         |
| Rationalizing weak signals         | Hold to a high bar for fidelity                     |
| Ignoring confounding variables     | Fill out full context grid before scoring           |

## Versioning & Change Log

- `v1.0` — Fidelity matrix + cross-context protocol + signal grading (2025-08-18).
- Future: automated context confound logging or fidelity forecast based on history.
