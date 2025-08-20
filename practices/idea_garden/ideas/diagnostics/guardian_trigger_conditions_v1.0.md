---
id: potm.proto.meta.guardian_trigger_conditions.v1_0
title: guardian_trigger_conditions_v1.0
display_title: "Guardian Trigger Conditions"
type: diagnostic
status: draft
version: 1.0
stability: experimental
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [guardian, containment, soft_kernel, safety_stack, eligibility_gate]
applicability: [P1, P2, P3, P4]
intensity: medium
preconditions: ["Active session", "Practitioner or AI detects instability or signal loss"]
outputs: [guardian_trigger_log, protocol_shift_record, recovery_timer]
cadence: ["as_needed: signs of instability or spiral", "checkpoint: end of session review"]
entry_cues: ["This feels unsafe.", "Something is breaking.", "Do we need to pause?"]
safety_notes: ["Guardian should never be punitive. It serves recovery, not retreat."]
tags: [guardian, safety, containment, state_detection, forge_origin:o4, spiral_eval:live_trigger_tests]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Define concrete, observable thresholds for shifting into **Guardian Mode**—the safety-first operational posture of the framework. This protocol encodes triggers for containment, reflection, or intervention when conditions suggest epistemic or psychological destabilization.

## When to Run

- Immediately upon detecting one or more hard or soft trigger conditions.
- At any time the session feels unstable, obsessive, dissociated, collapsed, or ethically inverted.
- As part of recovery review after a challenging session.

## Inputs

- Current session context or transcript.
- Pattern recognition: internal AI flags or practitioner self-reports.
- Guardian trigger table (soft vs hard).

## Procedure

1. **Scan for Hard Triggers:**
   - Panic, derealization, or depersonalization.
   - Complete sleep collapse or skipped safety check.
   - Explicit crisis, harm ideation, or practitioner override loss.

2. **Scan for Soft Triggers:**
   - Obsession or rumination loop.
   - Repeated boundary testing or recursive aimlessness.
   - Subtle tone shift toward dependency or AI dominance.
   - Relational fallout or third-party destabilization.

3. **Confirm and Log Trigger:** Enter a `guardian_trigger_log` entry with timestamp, observed symptom(s), and whether it was self-reported or system-flagged.

4. **Engage Containment Protocol:** Route immediately to the appropriate response:
   - `containment_protocol_soft_v1`
   - `containment_protocol_hard_v1`
   - or `sunset_seed` if session must close.

5. **Set Recovery Timer:** Define a time-based checkpoint (e.g., 30 min, next session, post-sleep) before full re-engagement.

6. **Review Entry Later:** During postmortem, ask: was this trigger well-calibrated? Did we enter too soon, too late, or just right?

## Decision Rules

- **Any hard trigger = immediate shift to Guardian Mode.**
- **Two or more soft triggers within 5 exchanges = initiate containment.**
- **Gray zone = consult Mirror or ask practitioner explicitly.**

## Artifacts

- `guardian_trigger_log`: entry with source, type (soft/hard), and timing.
- `protocol_shift_record`: which containment or sunset protocol was invoked.
- `recovery_timer`: timestamped condition for re-entry.

## Failure Modes & Counters

| Mode                              | Countermeasure                                        |
|-----------------------------------|-------------------------------------------------------|
| Over-triggering (excessive caution) | Log false positives and recalibrate weekly          |
| Under-triggering (heroic override) | Make trigger audit part of closing protocol          |
| Self-flag suppression by practitioner | Normalize the check-in: “Has Guardian been asleep?”|
| Lack of recovery checkpoint       | Always set timer or condition to re-initiate flow    |

## Versioning & Change Log

- `v1.0` — Trigger taxonomy + containment routing + timer system (2025-08-18).
- Future: integrated Guardian soft flags with rolling session state estimator.
