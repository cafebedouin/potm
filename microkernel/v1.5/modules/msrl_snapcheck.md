---
id: potm.proto.msrl_snapcheck.v1
title: msrl_snapcheck
display_title: "3×3 Cross-Check (P0/P1)"
type: diagnostic
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: adapted
  agent_protocol: core/kernel/potm_bootpack_combined.md
  supersedes: []
  superseded_by: []
interfaces: [engagement_flow]
applicability: [P0, P1]
intensity: gentle
preconditions: []
outputs: [next_move, risk_note]
cadence: ["use on decisions > 5 minutes of thought"]
entry_cues: ["I’m stuck", "conflicting advice", "high uncertainty, low reversibility"]
safety_notes: ["Name the cost of being wrong before acting"]
tags: [practice_card, snapcheck, forge_origin:aug-12-2025, spiral_eval:live]
author: "practitioner"
license: CC0-1.0
---

### 3×3 Cross-Check
**Ask (max 90 seconds total):**
1) **Other Lens:** “What would a different substrate say?”  
   - Human mentor? Past-self? Future-self? Opponent? (Pick one.)
2) **Risk Posture:** “What’s the **cost of being wrong** here?”  
   - Low → ship a reversible micro-move.  
   - High → buy information first.
3) **Next Reversible Move:** “What’s the smallest action that learns the most?”

**Write 1 line each:** lens takeaway • risk note • micro-move.

**Do it. Re-check once:** Did the micro-signal change the picture?

Originated as a stripped-down candidate from Idea → Practice Flow v1.2. If deferred, park in Idea Garden /plots/ per experimental/README.md.
