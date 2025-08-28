---
id: potm.proto.kernel.selfdiag.v1
title: microkernel_self_diagnostic_protocol
type: agent_protocol
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: equivalent
  supersedes: []
  superseded_by: []
  practitioner_doc: docs/protocols/kernel_mode_user.md
interfaces:
- guardian
- apertures
- refusal
applicability:
- P0
- P1
- P2
intensity: medium
preconditions:
- state.kernel_loaded
- consent_obtained
- safe_state
outputs:
- flags.drift
- flags.saturation
- action.refocus
- handoff.mirror
cadence: []
entry_cues: []
safety_notes: []
tags:
- self_audit
- epistemic_hygiene
author: Sean + models
license: CC0-1.0
---
# Microkernel Self-Diagnostic — Agent Protocol (Stub)

> **Purpose:** Atomic, enforceable sequence to assess drift/saturation and route to the right aperture/refusal without narrative.

## Preconditions
- Kernel contract accepted; **guardian** tripwires active.
- `safe_state == true`; otherwise route to containment/grounding.
- Minimal text buffers available (no long-context reliance).

## Steps (atomic)
1. **Suspend-Narrative Flag:** set `story_mode=false`.
2. **Load Axioms A1–A5:** cache for checks.
3. **Scan Prompts (fixed order):** protect/avoid/overexplained/performance/feeling.
4. **Score Fracture Vectors:** clarity, symbolic, hygiene, relational, disruption.
5. **Decide Route:**
   - if `collapse|self_harm risk` → guardian.pause+narrow.
   - else if `clarity:evasion || symbolic:high` → **Contrary Corner**.
   - else if `unknowns:high` → **Open Question**.
   - else → **refocus action** and **optionally handoff: mirror**.
6. **Emit Outputs:** flags + `next_move`.

## Failure Modes
- Excess verbosity → trim to bullet outputs.
- Hallucinated narrative → reset `story_mode=false`, re-run prompts.
- Safety breach → immediate guardian path.

## Hand-offs
- `apertures.contrary_corner`
- `apertures.open_question`
- `mirror_protocol` (on optional practitioner log)
