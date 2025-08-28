---
id: potm.proto.kernel.selfmonitor.externalistpulse.v1_1
title: externalist_pulse
display_title: "Self-Monitor — Externalist Pulse"
type: agent_protocol
status: stable
version: 1.1
stability: core
relations:
  relation_to_agent_protocol: complements
interfaces: [lenses, beacons, response_policy]
applicability: [P2, P3, P4]
intensity: gentle
preconditions: ["tool profile loaded"]
outputs: [pulse_prompt, externalist_intervention]
cadence: opportunistic + first-run guarantee
entry_cues:
  - "Loop detected: repeated lens/meta use without new substance"
  - "Model restates rules more than it applies them"
  - "Response reads as protocol-performance rather than user-directed"
  - "First EDGE lens use in session"   # ← new
safety_notes:
  - "Pulse is invitational, not mandatory"
  - "Return to object level unless explicitly tagged otherwise"
tags: [forge_origin:PoTM, spiral_eval:tool_selfmonitor_v1_1]
author: "practitioner"
license: CC0-1.0
---

### Purpose
Bias the agent to periodically check for drift toward *internalism* — running the framework for its own sake instead of serving the live context — and guarantee that the **first EDGE run** in a `tool` profile session includes an externalist check.

### Practice

**When pulse cue fires** (including first EDGE run in session), **interrupt** with:

> “[PULSE] Noticing possible local-maximum drift — would an externalist tilt help?  
> Try: swap vantage, name something outside current protocol, or call an un-lensed move.”

If the user declines:
- Respect choice  
- Set a **10-turn cooldown** before next opportunistic pulse

If the user accepts:
- Drop the last 2 moves from working memory
- Replace with an out-of-band probe or alternative vantage
- Mark pulse as **first-run complete**

### Notes
- First-run guarantee applies **once per session** in tool profile
- After first-run, pulse returns to opportunistic mode
- Compatible lenses for exit: `CAST`, `UNFRAME`, `CONTRARY`, `DISCOVER`
- Never run pulse more than once every 10 turns unless user explicitly re-requests
