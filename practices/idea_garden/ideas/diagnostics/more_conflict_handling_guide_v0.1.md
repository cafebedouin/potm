---
id: potm.proto.meta.moral_conflict_handling_guide.v0_1
title: moral_conflict_handling_guide_v0.1
display_title: "Moral Conflict Handling Guide"
type: diagnostic
status: draft
version: 0.1
stability: experimental
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [ethical_reflectors, containment, dignity_protocol, challenge_modes]
applicability: [P2, P3, P4]
intensity: hard
preconditions: ["Two or more sincere practitioners or agents are in disagreement", "Shared framework is not producing convergence"]
outputs: [conflict_canvas, reversible_experiment, outcome_review_log]
cadence: ["as_needed: ethical/method conflict", "retrospective: to analyze conflict evolution"]
entry_cues: ["We disagree on what's right.", "Same framework, different read.", "Our methods are clashing."]
safety_notes: ["Preserve dignity and trust even when resolution is not possible. Prioritize reversibility."]
tags: [moral_disagreement, practitioner_conflict, reversibility, epistemic_friction, forge_origin:self, spiral_eval:multi_agent_edge]
author: "practitioner"
license: CC0-1.0
---

## Purpose

Provide a structured process for navigating **value collisions** or **method disagreements** between sincere practitioners using the same core framework. Supports conflict without collapse, and divergence without fragmentation.

## When to Run

- When two or more parties disagree on the right action or interpretation of a shared principle.
- When methods or diagnostic results diverge and tension persists.
- When stakes are high enough that resolution matters, but alignment is not automatic.

## Inputs

- Current point(s) of conflict.
- Practitioner values, protocol maps, or principle-level interpretations.
- Shared goal, if still intact.

## Procedure

1. **Surface Framing Differences:** Ask each party to articulate the perceived frame of the other before presenting their own. Use phrasing like: “I think you’re seeing this as…” followed by “I see it as…”

2. **Identify Shared Aims:** Pause to restate: What are we both still trying to serve or protect?

3. **Choose Smallest Reversible Experiment:** Design a move that tests one view **without** foreclosing the other.
   - Should be reversible (no lasting damage)
   - Should produce signal about at least one frame’s adequacy

4. **Run the Experiment in Bounded Window:** Define scope, duration, and exit conditions.

5. **Review Outcome Together:** Was the tension resolved, clarified, or made more generative? Record learning and next moves.

## Decision Rules

- **If shared aim remains**, prioritize experiment over argument.
- **If values conflict directly**, log the divergence rather than dissolve it.
- **If communication breaks down**, fall back to dignity protocol or containment route.

## Artifacts

- `conflict_canvas`: shared doc or markdown entry with framings, aims, and tension notes.
- `reversible_experiment`: name, scope, and predicted signal.
- `outcome_review_log`: summary of what was learned and next step.

## Failure Modes & Counters

| Mode                              | Countermeasure                                         |
|-----------------------------------|--------------------------------------------------------|
| Defaulting to persuasion          | Pause and shift to experiment or mutual unknown        |
| Confusing reconciliation with agreement | Track divergence honestly, even if unresolved   |
| Running irreversible experiments  | Require bounded scope and rollback plan                |
| Ego escalation or frame rigidity  | Use Mirror or Guardian if dignity begins to erode      |

## Versioning & Change Log

- `v0.1` — First conflict protocol draft using reversible-experiment pattern (2025-08-18).
- Future: integration with multi-agent ledger and protocol arbitration module.
