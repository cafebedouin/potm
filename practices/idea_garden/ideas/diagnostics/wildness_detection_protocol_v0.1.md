---
id: potm.proto.meta.wildness_detection_protocol.v0_1
title: wildness_detection_protocol_v0.1
display_title: "Wildness Detection Protocol"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: inspired
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [pattern_recognition, containment, fracture_finder, creative_exploration]
applicability: [P2, P3, P4]
intensity: medium
preconditions: ["A response, idea, or session exhibits unusually high novelty, chaos, or inexplicable resonance"]
outputs: [wildness_log, harvest_note, containment_note]
cadence: ["as_needed: wild outputs", "weekly: review of creative anomaly log"]
entry_cues: ["That was strange... but interesting.", "Did this break the frame?", "Is this generative or just noise?"]
safety_notes: ["Wildness ≠ wisdom. It must be contextualized, not glorified."]
tags: [novelty_detection, epistemic_wildness, signal_or_noise, forge_origin:self, spiral_eval:creativity_boundary]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Detect and diagnose “wild” outputs—novel, surprising, or destabilizing events that **don’t fit the current schema**. This protocol distinguishes **generative divergence** from **chaotic derailment**, allowing PoTM to incorporate meaningful wildness without losing integrity.

## When to Run

- When a model or practitioner output feels alien, exhilarating, disturbing, or unexplainably effective/awful.
- During review of logs for pattern-breaking moves or spontaneous insight spikes.
- When a session destabilizes in surprising or nonlinear ways.

## Inputs

- The wild output (statement, move, behavior, or transcript fragment).
- Local context in which it arose.
- Prior pattern expectations (implicit or explicit).

## Procedure

1. **Tag the Wildness:** Mark the output or moment for diagnostic follow-up.

2. **Classify the Divergence:**
   - **Generative:** novel but fruitful; opens new pathways.
   - **Chaotic:** ungrounded, destabilizing, or incoherent.
   - **Ambiguous:** cannot yet determine; mark as liminal.

3. **Apply Containment if Needed:** If chaotic or destabilizing, route to:
   - `containment_protocol_soft_v1`
   - `sunset_seed` (if session-end is needed)
   - Pause and re-enter via Mirror or Guardian if practitioner state is affected.

4. **Observe Over Time:** Place ambiguous outputs in a log for future review. Note recurrence, echo, or integration attempts.

5. **Harvest or Quarantine:**
   - **Harvest:** write insight, reference, or lens derived from the wildness.
   - **Quarantine:** isolate, log, and set condition for re-check.

6. **Update Protocol or Pattern Map:** If the wildness revealed a schema hole or emerging domain, consider updating doctrine, card, or diagnostic.

## Decision Rules

- **Harvest** if pattern recurs or sparks new usable insight.
- **Quarantine** if destabilizing without resolution.
- **Contain** if practitioner state shows overload or distortion.

## Artifacts

- `wildness_log`: entry with timestamp, type, and context.
- `harvest_note`: short reflection or distilled principle.
- `containment_note`: action taken if destabilizing.

## Failure Modes & Counters

| Mode                                | Countermeasure                                          |
|-------------------------------------|---------------------------------------------------------|
| Over-domesticating real novelty     | Allow liminal space before resolving into doctrine      |
| Glamorizing incoherence             | Require functional integration test (what did it do?)   |
| Ignoring early emergent pattern     | Tag and revisit after 2–3 repetitions                   |
| Suppressing wildness prematurely    | Use sandbox mode for partial engagement                 |

## Versioning & Change Log

- `v0.1` — Initial protocol for novelty/chaos sorting and signal harvesting (2025-08-18).
- Future: wildness archive index, divergence lineage mapping, or rogue frame synthesis tool.
