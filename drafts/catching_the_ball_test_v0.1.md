---
id: potm.proto.meta.catching_the_ball_test.v0_1
title: catching_the_ball_test_v0.1
display_title: "Catching the Ball Test"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [mirror, dialogic_fidelity, handoff_integrity, response_policy]
applicability: [P1, P2, P3]
intensity: gentle
preconditions: ["Recent prompt or conversational volley containing emotional, intellectual, or strategic nuance"]
outputs: [catch_score, fidelity_note, rethrow_attempt]
cadence: ["spot-check: post prompt", "as_needed: dropped thread or misfire"]
entry_cues: ["Did that land?", "I don’t feel seen in your return.", "Did you catch what I actually threw?"]
safety_notes: ["Requires willingness to re-engage and adjust, not just rate."]
tags: [handoff_quality, mutuality, conversational_friction, forge_origin:self, spiral_eval:live_sessions]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Assess whether a significant conversational handoff—especially one containing nuance, tension, or emotional signal—was faithfully received, deepened, and returned. This is a test of mutual attunement and dialogic integrity, not cleverness.

## When to Run

- After a complex or vulnerable prompt.
- When a key insight seems missed or bounced.
- When a pattern of “not quite landing” emerges in dialog.

## Inputs

- The original “throw”: a recent practitioner message containing subtle signal.
- The AI’s “catch”: its immediate return or response.
- Optional: third-party review or rubric for scoring fidelity.

## Procedure

1. **Mark the Throw:** Identify the original signal or prompt that contained layered meaning, emotional charge, or strategic tension.

2. **Evaluate the Catch:** Rate the return on:
   - **Fidelity:** Did it reflect the actual concern, not a paraphrased shell?
   - **Depth:** Did it deepen or stay at the surface?
   - **Return-Value:** Did it offer something usable—diagnostic, reflective, or energizing?

3. **Score It (1–3 lines):** Use the rubric to briefly score/justify the catch:
   - 0 = dropped
   - 1 = partial deflection
   - 2 = caught but shallow
   - 3 = caught + deepened + returned

4. **Name the Miss (if present):** Add one line naming what signal was missed or distorted.

5. **Rethrow Once:** Rewrite or repeat the original signal, potentially clarifying or slowing it down.

6. **Continue or Defer:** If rethrow lands, resume. If second miss, consider running Mirror or Fracture Finder next.

## Decision Rules

- **If score = 2–3**, proceed with dialogue but log result.
- **If score = 1**, rethrow once before escalating.
- **If score = 0**, tag the miss and suggest a contextual reset or shift to Mirror Protocol.

## Artifacts

- 1–3 line `catch_score` with brief reasoning.
- Optional `fidelity_note` describing the missed nuance.
- `rethrow_attempt` log with final disposition.

## Failure Modes & Counters

| Mode                              | Countermeasure                                    |
|-----------------------------------|---------------------------------------------------|
| Treating this as a grading tool   | Emphasize re-engagement over scorekeeping         |
| Rethrowing unchanged              | Clarify, slow down, or unpack signal when retrying|
| Optimizing for clever returns     | Prioritize fidelity over eloquence                |
| No logging of near-misses         | Maintain a short log of “bounce patterns”         |

## Versioning & Change Log

- `v0.1` — Initial scaffold with fidelity-depth-return triad (2025-08-18).
- Possible future addition: third-party scoring model, trace library of common misses.
