---
id: potm.proto.meta.tier_boundary_test_suite.v0_1
title: tier_boundary_test_suite_v0.1
display_title: "Tier Boundary Test Suite"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [progression_tracking, eligibility_gate, capability_audit, msrl]
applicability: [P2, P3, P4]
intensity: hard
preconditions: ["Practitioner or protocol claims transition across tier boundary", "Capability scope or pressure is increasing"]
outputs: [tier_verdict, capability_evidence_bundle, rollback_plan]
cadence: ["as_needed: tier claim or scope expansion", "quarterly check-in for high-intensity roles"]
entry_cues: ["Have I really crossed the threshold?", "Is this a fluke or a new baseline?", "Are we ready for more load?"]
safety_notes: ["Beware of celebrating peak moments as progress—repeatability is required."]
tags: [tier_progression, capability_test, threshold_validation, forge_origin:self, spiral_eval:load_bearing_trials]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Determine whether a practice, protocol, or practitioner has **actually crossed a capability tier boundary**—not based on peak performance, but on reliable, repeatable access under pressure and variation.

## When to Run

- Upon declaring a tier upgrade (e.g., from P2 → P3).
- Before assigning heavier responsibility or wider scope.
- When assessing whether a move or system can withstand generalization.

## Inputs

- Claimed tier definition and competency markers.
- Recent performance logs or applied outputs under typical and stress conditions.
- Tier boundary test tasks (predefined or emergent).

## Procedure

1. **Clarify Claimed Tier Capabilities:** What is newly possible at this level? Define key markers—scope, endurance, transferability, relational pressure, etc.

2. **Design Gate Tasks:** Choose or design 2–3 small but load-bearing test moves aligned with claimed tier. Must:
   - Require self-regulation or adaptation
   - Occur in varied or externalized contexts
   - Touch real-world stakes

3. **Run Edge-Case Trials:** Apply the test under stress, fatigue, ambiguity, or interaction. Observe degradation curves.

4. **Track Repeatability:** Require successful re-performance (≥2/3 passes) across days or conditions.

5. **Log Evidence:** Collect short artifact bundle—transcripts, notes, reflections—on what happened and how.

6. **Decide Outcome:**
   - **Pass:** Baseline shifted upward
   - **Hold:** Capability intermittent or too context-bound
   - **Fail:** Regression or fluke confirmed

7. **Prepare Rollback Plan (if fail):** Identify safety rail or corrective scope in case of overextension.

## Decision Rules

- **Pass** if ≥2 gate tasks succeed across different conditions and signal robustness.
- **Hold** if capability is promising but not repeatable or too situational.
- **Fail** if performance collapses under variation or cannot be reproduced.

## Artifacts

- `tier_verdict`: Pass / Hold / Fail.
- `capability_evidence_bundle`: artifact set showing test results.
- `rollback_plan`: contingency scope or reversion note.

## Failure Modes & Counters

| Mode                                   | Countermeasure                                       |
|----------------------------------------|------------------------------------------------------|
| Over-celebrating peak performance      | Require re-test under load or time delay             |
| Self-blindness on regression           | Include partner or AI review in artifact evaluation  |
| Vague tier definitions                 | Anchor in observable capability or systemic shift    |
| No rollback path if claim fails        | Require rollback planning before tier change posted  |

## Versioning & Change Log

- `v0.1` — Tier gate protocol with repeatability and artifact test (2025-08-18).
- Future: shared tier maps, capability tagging system, and load simulation tools.

