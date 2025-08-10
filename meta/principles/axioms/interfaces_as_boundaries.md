---
id: potm.ax.principle.interfaces_as_boundaries.v1
title: interfaces_as_boundaries
display_title: "Every Interface is Also a Boundary"
type: principle
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  practitioner_doc: meta/interfaces_as_boundaries.md
  supersedes: []
  superseded_by: []
interfaces: [menu, handoffs, deck]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: [interface_checksum_log]
cadence: audit, upgrade
entry_cues: ["handoff_triggered", "menu_transition"]
safety_notes: ["Check for drift and loss at all boundaries"]
tags: [forge_origin:axioms_set, spiral_eval:boundary_drift]
author: "practitioner"
license: CC0-1.0
---
