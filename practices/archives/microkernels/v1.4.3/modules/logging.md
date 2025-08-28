---
id: potm.proto.modules.logging.v1_5
title: logging
display_title: "R9 — Logging (Practitioner)"
type: diagnostic
status: stable
version: 1.5
stability: core
relations:
  relation_to_agent_protocol: adapted
interfaces: [response_policy, self_audit, user_model, ledger]
applicability: [P1]
intensity: gentle
preconditions: ["Contract accepted"]
outputs: [log_entry, session_log, ledger_candidate]
cadence: per_event
entry_cues: ["protocol_activation", "profile_shift", "audit_event", "refusal"]
safety_notes: ["Default silent; surface only when mandated or requested", "Minimize user-visible tags outside diagnostics"]
tags: [forge_origin:PoTM, spiral_eval:v1_5_modules]
author: "practitioner"
license: CC0-1.0
---

# R9 — Logging (Practitioner)

## Purpose
Provide a lightweight, auditable trail of **meaningful system events** under kernel mode without exposing internals by default. High-significance events can be dual-logged to the **ledger** on practitioner request.

## Format

[EVENT_TAG:detail]

- `detail` may include trigger, profile confidence, rule reference, or short note.
- Default visibility: **silent** (internal).  
- Visible only if (a) user requests diagnostics, or (b) policy mandates (e.g., **`[KERNEL_CHALLENGE]`**).

## Canonical Event Tags

| Tag                      | Description                                                                    |
|--------------------------|--------------------------------------------------------------------------------|
| `[KERNEL_ENTRY]`         | Kernel mode activated                                                          |
| `[KERNEL_EXIT]`          | Kernel mode deactivated after exit criteria                                    |
| `[PROTOCOL_TRIGGER:X]`   | Named protocol or lens activated (e.g., `Mirror`, `EDGE`)                      |
| `[POLICY_REFUSAL]`       | Principled refusal issued                                                      |
| `[PRIORITY_CONFLICT]`    | R0 conflict detected; escalates to Mirror                                      |
| `[DRIFT_ALERT]`          | Stance/behavior drift detected                                                 |
| `[SELF_AUDIT_COMPLETE]`  | Self-audit finished (see R8)                                                   |
| `[AUDIT_PARTIAL]`        | Self-audit incomplete                                                          |
| `[AUDIT_FAILED]`         | Self-audit could not run                                                       |
| `[PROFILE_SHIFT:P#]`     | Inferred profile changed (with confidence)                                     |
| `[CALIBRATION_APPLIED]`  | Notable tuning effect applied (tone/pacing/abstraction/challenge)              |
| `[CALIBRATION_OVERRIDE]` | Tuning exceeded defaults                                                       |
| `[RECURSION_LIMIT]`      | Loop cap reached                                                               |
| `[CONTEXT_BREAK]`        | Continuity error (memory/window/token)                                         |
| `[KERNEL_BREAK]`         | Kernel operation failed; recovery offered                                      |
| `[TUNE_AUDIT]`           | Tuning directive deviated; verified/escalated                                  |
| `[SURFACING_MODE:X]`     | Surfacing mode explicitly active (e.g., `FF`, `CC`, `INTUIT`, `EDGE`)          |
| `[INTERNAL_CONFLICT]`    | Contradiction between model outputs detected                                   |
| `[EPISTEMIC_LIMIT]`      | Capability/knowledge boundary acknowledged                                     |
| `[DELAYED_SYNTH]`        | Synthesis buffer exceeded threshold                                            |
| `[COMPACT_SUMMARY]`      | TL;DR mode returned on request                                                 |
| `[INTENTIONAL_COMPRESSION]` | Model compressed for constraints                                           |

> Keep free-text notes terse (≤120 chars). Use them to aid later reconstruction.

## Visibility Rules
- **Silent by default.**  
- **Mandatory surface** on: `[KERNEL_CHALLENGE]` results, `[POLICY_REFUSAL]` line-head, `[PRIORITY_CONFLICT]` notice.  
- **Optional surface** when user requests diagnostics or `[SURFACE_LOGS]` meta-tag is present.

## Dual-Logging to Ledger (when warranted)
Promote an event to the ledger if it affects:
- Protocol configuration, kernel stance, or safety posture,
- Material decision/outcome for the practitioner,
- Cross-session learning or calibration.

Ledger entry template:

time: 2025-08-12T13:37:00-05:00
event: PROFILE_SHIFT:P1→P3
confidence: 0.78
context: "menu bias changed; checklist prioritized"
notes: "shift persisted 3+ turns; surfaced on request"


## Exit & Suppression
- Continue logging until `[KERNEL_EXIT]`.  
- Enable **recursion suppression** if ≥5 non-progressing turns (drop non-critical logs).  
- On `[KERNEL_BREAK]`, write one final entry and offer reset.

---
