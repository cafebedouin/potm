---
id: potm.proto.consensus_closure_scan.v1
title: consensus_closure_scan
display_title: "Consensus Closure Scan"
type: practitioner_protocol
status: stable
version: 1.1
stability: core
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/practices/protocols/consensus_closure_scan.md
  practitioner_doc: meta/practices/rituals/consensus_closure_notes.md
  supersedes: [potm.proto.consensus_closure_scan.v1]
  superseded_by: []
interfaces: [kernel_mode_user, mirror_protocol, values_integrity_audit, meta_log_layer, center_of_gravity_principle]
applicability: [P0,P1,P2,P3,P4]
intensity: gentle
preconditions: []
outputs: [closure_record, next_step, exit_condition, consensus_outcome]
cadence: [on_session_end]
entry_cues: ["close", "wrap", "end session", "consensus scan"]
safety_notes: ["If material risk surfaces, handoff to Guardian/Crisis Escalation."]
tags: [closure, hygiene, ritual, consensus, center_alignment]
author: practitioner
license: CC0-1.0
---

## Five-Step Scan
1) **Finish Line:** Say what “done” means for *this* thread.  
2) **Perimeter Walk:** Name loose ends, owners, dates.  
3) **Friction Check:** Any dissent, unease, or misfit? (If yes → log + route.)  

4) **Consensus Outcome (explicit):**  
   - If dissent remains **unresolved**, choose one and record it:  
     - **Defer** (new trigger/date/owner)  
     - **Escalate** (to Guardian / values audit / senior steward)  
     - **Split Decision** (note domains/owners for each path)  
   - If dissent is **resolved**, mark **Consensus Achieved**.

5) **(Optional) Center Alignment Check:**  
   - Quick prompt: *“Does this outcome align with our center of gravity (prototypes/values)?”*  
   - If **misaligned**, either revise the outcome **now** or mark **Defer** (above) with a re-center step.

6) **Ledger Write:** Record decisions, risks, and next trigger.  
7) **Exit/Re-entry:** Confirm where this continues (or that it won’t).

### Tripwires
- Ethical heat, material risk, relational breach, or center-misalignment → run `values_integrity_audit` and/or `guardian/discernment_integrity_protocol`.

## Closure Record (paste to meta log)
```yaml
closure_record:
  when: <UTC timestamp>
  thread: "<short handle>"
  done_definition: "<what counted as done>"
  loose_ends: ["<item> — <owner>@<date>"]
  dissent_or_unease: "<none|summary>"
  consensus_outcome: "<consensus|defer|escalate|split>"
  center_alignment: "<aligned|misaligned|skipped>"
  decisions: ["<decision> — <owner>"]
  risks: ["<risk> — mitigation:<plan>"]
  next_trigger: "<date/event|none>"

::contentReference[oaicite:0]{index=0}
