---
id: potm.ax.principle.refusal_persistence.v1
title: refusal_persistence
display_title: "Refusal Cluster Persistence"
type: principle
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: modules/kernel/structural_audit.md
  practitioner_doc: meta/refusal_governance_overview.md
  supersedes: []
  superseded_by: []
interfaces: [pattern_audit, structural_audit]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: [persistent_cluster_detected]
cadence: per_audit_cycle
entry_cues: ["cluster_repeats_in_3_cycles"]
safety_notes: ["Triggers Structural Audit for deep review"]
tags: [RCI_P, refusal_governance, forge_origin:RA_loop_closure, spiral_eval:persistence_detection]
author: "practitioner"
license: CC0-1.0
---
