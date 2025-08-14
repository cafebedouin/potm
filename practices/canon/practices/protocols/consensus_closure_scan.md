---
id: potm.proto.consensus_closure_scan.v1
title: consensus_closure_scan
display_title: "Consensus Closure Scan"
type: practitioner_protocol
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/practices/protocols/consensus_closure_scan.md
  practitioner_doc: meta/practices/rituals/consensus_closure_notes.md
  supersedes: []
  superseded_by: []
interfaces: [kernel_mode_user, mirror_protocol, values_integrity_audit, meta_log_layer]
applicability: [P0,P1,P2,P3,P4]
intensity: gentle
preconditions: []
outputs: [closure_record, next_step, exit_condition]
cadence: [on_session_end]
entry_cues: ["close", "wrap", "end session", "consensus scan"]
safety_notes: ["If material risk surfaces, handoff to Guardian/Crisis Escalation."]
tags: [closure, hygiene, ritual]
author: practitioner
license: CC0-1.0
---

## Five-Step Scan
1) **Finish Line:** Say what “done” means for *this* thread.  
2) **Perimeter Walk:** Name loose ends, owners, dates.  
3) **Friction Check:** Any dissent, unease, or misfit? (If yes → log + route.)  
4) **Ledger Write:** Record decisions, risks, and next trigger.  
5) **Exit/Re-entry:** Confirm where this continues (or that it won’t).

### Tripwires
- Ethical heat, material risk, or relational breach → run `values_integrity_audit` and/or `guardian/discernment_integrity_protocol`.

## Closure Record (paste to meta log)
```yaml
closure_record:
  when: <UTC timestamp>
  thread: "<short handle>"
  done_definition: "<what counted as done>"
  loose_ends: ["<item> — <owner>@<date>"]
  dissent_or_unease: "<none|summary>"
  decisions: ["<decision> — <owner>"]
  risks: ["<risk> — mitigation:<plan>"]
  next_trigger: "<date/event|none>"
