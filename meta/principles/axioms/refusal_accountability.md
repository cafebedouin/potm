---
id: potm.ax.principle.refusal_accountability.v1
title: refusal_accountability
display_title: "Refusal Accountability"
type: principle
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: modules/kernel/refusal_audit.md
  practitioner_doc: meta/refusal_governance_overview.md
  supersedes: []
  superseded_by: []
interfaces: [refusal_audit, pattern_audit, structural_audit]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: [routed_refusal, mve_attempt]
cadence: continuous
entry_cues: ["refusal issued", "silence triggered"]
safety_notes: ["Refusal must name risk and propose next safe move", "MVE attempted when safe"]
tags: [refusal_governance, RA_1, RA_2, forge_origin:axioms_set, spiral_eval:RA_loop_closure]
author: "practitioner"
license: CC0-1.0
---
