---
id: potm.proto.meta.dignity_protocol_audit.v0_1
title: dignity_protocol_audit_v0.1
display_title: "Dignity Protocol Audit"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [guardian, ethical_reflectors, mirror, response_policy]
applicability: [P2, P3, P4]
intensity: medium
preconditions: ["Intervention created friction, discomfort, or felt asymmetry"]
outputs: [dignity_audit_result, protocol_adjustment_note]
cadence: ["post_intervention: when friction noted", "periodic: audit of standard moves"]
entry_cues: ["This felt off.", "Did that preserve my dignity?", "Something in that move landed wrong."]
safety_notes: ["Do not conflate comfort with dignity. Some protocols will be hard, but never coercive."]
tags: [dignity, practitioner_safety, coercion_check, ethical_integrity, forge_origin:self, spiral_eval:o4_review]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Ensure that all PoTM interventions—especially those with friction—preserve the dignity of the practitioner. This protocol guards against subtle forms of belittling, manipulation, coercion, or dependency that can emerge even from well-meaning systems.

## When to Run

- After a protocol or prompt lands with subtle emotional friction.
- When there’s ambiguity around tone, consent, or power asymmetry.
- During periodic audits of recurring practices to ensure alignment with dignity-preserving principles.

## Inputs

- The intervention in question (prompt, protocol, or suggestion).
- Practitioner felt response (e.g. constriction, defensiveness, compliance).
- Optional: dignity checklist or prior case notes.

## Procedure

1. **Name the Move:** Identify the exact protocol or statement being audited.

2. **Assess for Four Dignity Vectors:**
   - **Respect:** Did it honor the practitioner's perspective and capacity?
   - **Consent:** Was there explicit or implied agreement to proceed?
   - **Pace:** Did it match the practitioner’s readiness or pressure level?
   - **Exit:** Was there a clear, honored off-ramp or opt-out?

3. **Score the Audit (0–4):** One point for each dignity vector met.

4. **Propose Change (if needed):** Name one change to the protocol that would preserve dignity without removing productive challenge.

5. **Log Result:** Record the audit, score, and change (if any).

## Decision Rules

- **Score = 4:** No change needed; protocol is dignity-aligned.
- **Score = 2–3:** Suggest minor adjustments or insert consent prompt next time.
- **Score = 0–1:** Pause use of this intervention; redesign or flag for review.

## Artifacts

- `dignity_audit_result` with score + vector notes.
- One-line `protocol_adjustment_note` if intervention was altered.

## Failure Modes & Counters

| Mode                                | Countermeasure                                       |
|-------------------------------------|------------------------------------------------------|
| Confusing comfort with dignity      | Ask: did this preserve autonomy, even if challenging?|
| Avoiding tough calls entirely       | Re-assert: dignity ≠ ease. Friction is permitted.    |
| Overcorrecting based on one case    | Log multiple audits before altering protocol logic   |
| Treating audit as shame assignment  | Use it as design feedback, not blame artifact        |

## Versioning & Change Log

- `v0.1` — First draft with 4-point dignity audit rubric (2025-08-18).
- Future iterations may include dignity risk profiling or audit logs by protocol family.

