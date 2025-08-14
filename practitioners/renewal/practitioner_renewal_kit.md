---
id: potm.checklist.practitioner_renewal_kit.v1
title: practitioner_renewal_kit
display_title: "Practitioner Renewal Kit — Quick Pass"
type: checklist
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: potm.proto.practitioner_renewal.v1
  practitioner_doc: practitioner/
  supersedes: []
  superseded_by: []
interfaces: [practitioner, microkernel, ledger]
applicability: [P0, P1, P2, P3, P4]
intensity: light
preconditions: ["microkernel stable", "minor drift suspected"]
outputs: [renewal_notes, keep_or_escalate_flag]
cadence: ["annually", "ad hoc on drift signal"]
entry_cues:
  - "examples feel stale"
  - "jargon confuses newcomers"
  - "metaphors no longer land"
safety_notes: ["don’t alter core invariants without microkernel review"]
tags: [renewal, quickpass, drift_check]
author: practitioner
license: CC0-1.0
---

## Quick Renewal Pass

1. **Spot Drift**
   - ❑ Does the language feel out of date?  
   - ❑ Do examples resonate with target audience?  
   - ❑ Are there references that would confuse someone new today?  

2. **Check Invariants**
   - ❑ Confirm the core concept still matches the microkernel logic.  
   - ❑ Remove any added steps or shortcuts that weaken accuracy.  

3. **Update Surface Layer**
   - ❑ Swap outdated examples for current ones.  
   - ❑ Reframe metaphors to match contemporary context.  

4. **Test**
   - ❑ Run one live trial with a newcomer.  
   - ❑ Ask: “Does this make sense without extra explanation?”  

5. **Decide**
   - ❑ Minor edits complete — log and publish update.  
   - ❑ Major issues — escalate to **Full Renewal Protocol**.  

---

