---
id: potm.proto.meta.skillfulness_calibration_protocol.v0_1
title: skillfulness_calibration_protocol_v0.1
display_title: "Skillfulness Calibration Protocol"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [practice_evaluation, exemplar_comparison, progression_tracking]
applicability: [P2, P3]
intensity: medium
preconditions: ["Practitioner has demonstrated a skill across multiple contexts", "A domain shift or tier claim is under consideration"]
outputs: [calibrated_rubric, delta_plan]
cadence: ["quarterly", "after domain shift", "before declaring progression or teaching capacity"]
entry_cues: ["Am I actually skillful, or just comfortable?", "Have I earned the next tier?", "Is this transferable?"]
safety_notes: ["Beware of importing standards from unrelated domains."]
tags: [skill_calibration, performance_tracking, exemplar_mapping, forge_origin:self, spiral_eval:rubric_experiments]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Calibrate perceived skillfulness against shared standards and **cross-context performance**, avoiding over-personalized or inflated grading. Establish whether a practitioner’s ability is transferable and reliable enough for scope expansion or tier progression.

## When to Run

- At regular calibration intervals (e.g. quarterly).
- When shifting domains (e.g. somatic → dialogic, internal → interpersonal).
- Before claiming a higher tier or preparing to teach a move.

## Inputs

- Recent performance logs or notes across 2–3 representative sessions.
- Exemplar rubric or reference model (if available).
- List of desired or claimed competencies.

## Procedure

1. **Define Competency Set:** List key capabilities relevant to the practice or domain (e.g. signal detection, state modulation, dialogic fluidity).

2. **Sample 2–3 Performances:** Choose representative sessions across different contexts, not just best-case examples.

3. **Compare to Exemplars:** Use rubrics, recordings, or model-generated samples for contrast.

4. **Score Each Competency (0–3):**
   - 0 = Absent
   - 1 = Emerging
   - 2 = Reliable
   - 3 = Adaptive / fluid / transferable

5. **Review for Transferability:** Can this skill hold in:
   - Stress
   - Complexity
   - Unscripted or relational settings

6. **Create Delta-to-Next-Tier Plan:** Define what would need to shift (quantity, context, depth) to earn next level.

## Decision Rules

- **Average score ≥2.5 + transferability = next-tier eligible.**
- **Score <2 or context-bound = refine before expansion.**
- **Any 0s = address before claim of progression.**

## Artifacts

- `calibrated_rubric`: scored grid with notes.
- `delta_plan`: actions required to reach next skill tier.

## Failure Modes & Counters

| Mode                               | Countermeasure                                      |
|------------------------------------|-----------------------------------------------------|
| Mistaking comfort for skill        | Include stress-testing or relational contexts       |
| Inflating scores without exemplar  | Require comparison to reference pattern             |
| Narrow-domain overconfidence       | Calibrate in multiple modalities                    |
| Using style as proxy for depth     | Anchor to outcomes, not aesthetics                  |

## Versioning & Change Log

- `v0.1` — Rubric-based calibration scaffold with exemplar anchoring (2025-08-18).
- Future: cohort benchmarking, skill drift tracking, or dynamic rubric adaptation.

