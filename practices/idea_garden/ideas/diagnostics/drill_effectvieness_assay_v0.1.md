---
id: potm.proto.meta.drill_effectiveness_assay.v0_1
title: drill_effectiveness_assay_v0.1
display_title: "Drill Effectiveness Assay"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [practice_card, signal_monitoring, fidelity_assessment, response_policy]
applicability: [P1, P2, P3]
intensity: medium
preconditions: ["Drill has been used at least 3–5 times in consistent form"]
outputs: [drill_assay_card, signal_rating, next_action_flag]
cadence: ["after set of 3+ reps", "post-session: focused drill deployment"]
entry_cues: ["Did that move the needle?", "Is this worth keeping?", "What did that actually change?"]
safety_notes: ["Drills should be evaluated for effect, not novelty or aesthetics."]
tags: [drill_testing, protocol_validation, practice_signal, forge_origin:self, spiral_eval:card_efficacy]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Rapid assay of whether a specific PoTM drill (e.g. a practice card, micro-intervention, or protocol snippet) reliably produces its intended signal within a bounded time window. Distinguishes between “cool” and “effective.”

## When to Run

- After 3–5 uses of a drill or after a focused session using it.
- When deciding whether to promote, tweak, or retire a practice element.
- During audit cycles for card decks or modular protocol packs.

## Inputs

- The drill or practice in question.
- Session notes or subjective memory of effect.
- Target signal defined beforehand (e.g. perceptual shift, behavior change, relational impact).

## Procedure

1. **Name the Drill:** Identify the exact phrase, card, or move tested.

2. **Define Intended Signal:** State what shift it is meant to produce—clarity, presence, discomfort tolerance, insight, etc.

3. **Rate Observed Signal (1–5):**
   - 1 = no shift
   - 3 = noticeable but weak/passing
   - 5 = clear, lasting, robust signal

4. **Note Duration & Persistence:** How fast did it emerge? How long did it last? Was it context-dependent?

5. **Log Side Effects (if any):** Positive (energizing, creative boost) or negative (anxiety spike, overconfidence).

6. **Choose Outcome Path:**
   - **KEEP** if effective and clean.
   - **TWEAK** if mixed or variable.
   - **RETIRE** if weak, confusing, or backfires.

7. **Record Assay Result:** Fill out or append a one-page `drill_assay_card`.

## Decision Rules

- **KEEP** if ≥4 signal rating with few/no adverse effects.
- **TWEAK** if 2–3 rating or high context-dependence.
- **RETIRE** if <2 or adverse effects outweigh benefit.

## Artifacts

- `drill_assay_card` (template log or markdown entry).
- Signal score and short rationale.
- Outcome flag (keep / tweak / retire).

## Failure Modes & Counters

| Mode                              | Countermeasure                                       |
|-----------------------------------|------------------------------------------------------|
| Keeping drills that “feel cool”   | Focus on signal yield, not conceptual elegance       |
| Ignoring adverse effects          | Log both signal *and* shadow clearly                 |
| Assuming single-run success = proof | Require consistency over ≥3 runs                  |
| Failing to test in multiple contexts | Rotate across situations or internal states       |

## Versioning & Change Log

- `v0.1` — Initial assay protocol with 5-point signal rating and triage logic (2025-08-18).
- Future versions may include batch testing dashboard or practice card analytics wrapper.
