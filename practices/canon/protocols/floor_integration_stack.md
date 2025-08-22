---
id: potm.proto.floor_integration_stack.v1
title: floor_integration_stack
type: practitioner_protocol
status: stable
version: 1.0
interfaces: [baseline_practices, meta_log_layer]
applicability: [P0,P1,P2,P3,P4]
license: CC0-1.0
---

# Floor Integration Stack
**Purpose:** capture unanswered choices during "floor" sessions so they can be resolved later without breaking flow.

## Capture Rule
If a multi-choice prompt goes unanswered, append an entry (id, question, options, default_taken, state=open, due).

## Nudge Rule
At the first "floor" each day, show up to two oldest `open` (not snoozed). 60s cap. Options: choose | snooze 1w | skip today.

## Sweep Rule
Weekly: resolve or snooze overdue items; archive resolved.
