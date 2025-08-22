---
id: potm.meta.schema.front_matter.v0_1
title: front_matter_schema_v0.1
type: guideline
status: stable
version: 0.1
stability: core
tags: [metadata, indexing, schema]
license: CC0-1.0
---

# Minimal Front-Matter Schema (v0.1)

Use this header on protocols/diagnostics/guidelines to keep models and humans aligned.

```yaml
id: potm.proto.kernel.selfdiag.v1        # namespace.type.family.version
title: microkernel_self_diagnostic_protocol
display_title: "Microkernel Self-Diagnostic"   # optional
type: agent_protocol | practitioner_protocol | diagnostic | guideline
status: stable | draft | deprecated
version: 1.0
stability: core | experimental
relations:
  relation_to_agent_protocol: equivalent | adapted | inspired | none
  agent_protocol: core/practices/protocols/microkernel_self_diagnostic_protocol.md
  practitioner_doc: docs/protocols/kernel_mode_user.md
  supersedes: []          # ids
  superseded_by: []       # ids
interfaces: [guardian, apertures, refusal]
applicability: [P0, P1, P2, P3, P4]
intensity: gentle | medium | hard
preconditions: [safe_state, consent_obtained]
outputs: [flags.drift, action.refocus, handoff.mirror]
cadence: on_drift | weekly | pre_minotaur
entry_cues: ["Strip to kernel"]
safety_notes: ["Narrative parking, not deletion"]
tags: [epistemic_hygiene, self_audit]
author: "Practitioner + A.I. models"
license: CC0-1.0
