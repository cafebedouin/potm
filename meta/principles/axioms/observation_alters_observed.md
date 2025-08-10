---
id: potm.ax.principle.observation_alters_observed.v1
title: observation_alters_observed
display_title: "Observation Alters the Observed"
type: principle
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  practitioner_doc: meta/observation_alters_observed.md
  supersedes: []
  superseded_by: []
interfaces: [model_upgrade_check]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: []
outputs: []
cadence: audit, upgrade
entry_cues: ["probe initiated", "measurement performed"]
safety_notes: ["Design probes whose distortions are legible and bounded"]
tags: [OAO, forge_origin:axioms_set, spiral_eval:measurement_effects]
author: "practitioner"
license: CC0-1.0
---
