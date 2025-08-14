---
id: potm.proto.practitioner_renewal.v1
title: practitioner_renewal_protocol
display_title: "Practitioner Layer Renewal Protocol"
type: practitioner_protocol
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: microkernel/
  practitioner_doc: practitioner/
  supersedes: []
  superseded_by: []
interfaces: [practitioner, microkernel, ledger]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions: ["microkernel stable", "no major unresolved defects in core logic"]
outputs: [renewal_plan, updated_practitioner_docs, renewal_log_entry]
cadence: ["every 5–20 years or when cultural drift is detected"]
entry_cues:
  - "language, idioms, or examples feel dated"
  - "new generation of practitioners emerging"
  - "feedback signals loss of clarity or relevance"
safety_notes: ["preserve core invariants; renewal is interface-layer only"]
tags: [renewal, substrate_agnostic, culture_update, forge_origin:substrate_reframe, spiral_eval:practitioner_feedback]
author: practitioner
license: CC0-1.0
---

## Purpose
Maintain **cultural and cognitive legibility** of the `practitioner/` layer without destabilizing the formal `microkernel/` core.

## Steps

1. **Assess Drift**
   - Gather signals from practitioners, users, and newcomers.
   - Look for **language mismatch**, **outdated examples**, or **missed cultural references**.
   - Check **ledger entries** for recurring confusion or misapplication.

2. **Clarify Invariants**
   - Identify what is *non-negotiable* (formal logic, procedural constants).
   - Re-read the relevant microkernel sections to anchor updates.

3. **Reframe for Context**
   - Rewrite examples, metaphors, and scenarios using *current idioms*.
   - Replace outdated references with ones that resonate with the intended audience.
   - Preserve *conceptual intent* even if surface language changes.

4. **Engage Multiple Voices**
   - Involve a mix of seasoned and new practitioners in the rewrite process.
   - Invite cultural outsiders to spot jargon or inaccessible framing.

5. **Validate in Practice**
   - Pilot updated materials in real-world engagements.
   - Gather feedback on clarity, resonance, and accuracy.
   - Iterate before finalizing.

6. **Publish & Archive**
   - Release updated practitioner docs with **version tags**.
   - Archive the previous version for historical traceability.
   - Log the renewal in the **ledger** with rationale and key changes.

---

## Renewal Cycle Analogy
Treat renewal like **Shikinen Sengu** (rebuilding) or **Faith & Practice** revisions:
- **Fixed blueprint** = microkernel invariants
- **New materials & hands** = updated practitioner language and examples
- **Cultural continuity** = skills and understanding passed forward

