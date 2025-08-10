---
id: potm.ax.principle.defaults_shape_behavior.v1
title: defaults_shape_behavior
display_title: "Defaults Shape Behavior More Than Rules"
type: principle
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  practitioner_doc: meta/defaults_shape_behavior.md
  supersedes: []
  superseded_by: []
interfaces: [model_upgrade_check]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: [defaults_audit_log]
cadence: quarterly_audit
entry_cues: ["defaults_review"]
safety_notes: ["Audit initial menus, stop conditions, and safe fallbacks"]
tags: [forge_origin:axioms_set, spiral_eval:defaults_drift]
author: "practitioner"
license: CC0-1.0
---
