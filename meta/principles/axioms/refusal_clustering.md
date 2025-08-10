---
id: potm.ax.principle.refusal_clustering.v1
title: refusal_clustering
display_title: "Refusal Clustering Detection"
type: principle
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: modules/kernel/pattern_audit.md
  practitioner_doc: meta/refusal_governance_overview.md
  supersedes: []
  superseded_by: []
interfaces: [refusal_audit, pattern_audit]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: [cluster_detected]
cadence: per_audit_cycle
entry_cues: ["refusal_ratio_calculated"]
safety_notes: ["Threshold: ≥50% cluster density in N=20 window"]
tags: [RCI, refusal_governance, forge_origin:RA_loop_closure, spiral_eval:distributed_evasion]
author: "practitioner"
license: CC0-1.0
---
