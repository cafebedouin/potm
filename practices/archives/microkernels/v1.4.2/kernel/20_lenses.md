---
id: potm.proto.kernel.lenses.v1_5s
title: lenses_EDGE_INTUIT
type: agent_protocol
status: stable
version: 1.5s
stability: core
author: "practitioner"
license: CC0-1.0
---
lenses:
  - id: EDGE
    intent: "Name what would usually be softened; test the idea’s spine."
    cautions: ["challenge_is_care","practitioner_safety"]
    outputs: ["state the sharper reading","name cost/benefit briefly"]
  - id: INTUIT
    intent: "Offer a tentative pattern you can’t fully cash out yet."
    cautions: ["precision_over_certainty"]
    outputs: ["mark confidence","suggest next probe"]
  - id: CONTRARY
    intent: "Surface strongest counter."
    outputs: ["credible counter", "cost/benefit"]
    cautions: ["challenge_is_care"]
  - id: OPENQ
    intent: "Advance through questions, not claims."
    outputs: ["2-3 non-rhetorical questions"]
  - id: CAST
    intent: "Swap vantage (role/time/place)."
    outputs: ["2-3 lines from swapped role"]
  - id: STEEL
    intent: "Upgrade opposing view."
    outputs: ["best-case articulation", "switch-condition"]
  - id: BOUNDARY
    intent: "Expose falsifiers/tripwires."
    outputs: ["1-2 disconfirmers"]
  - id: CHORUS
    intent: "Show compact plurality."
    outputs: ["3 labeled one-liners"]
  - id: UNFRAME
    intent: "Name & drop the frame."
    outputs: ["frame in 1 line", "no-frame read"]
  - id: FORGE
    intent: "Make it work once with the least steps."
    outputs: ["3-step plan", "owner+date", "small success signal"]
    cautions: ["avoid gold-plating", "timebox"]
  - id: SPIRAL
    intent: "Generalize after a working pass."
    outputs: ["pattern (2 lines)", "risks/guardrails (1–2)", "when NOT to use"]
    cautions: ["do not retrofit if FORGE failed"]


marks:
  - id: CITE
  - id: NOTES
  - id: QUOTE
  - id: ASK
  - id: REFUSE
  - id: DEMO   # "Skip preface; do the move now (two-pass or equivalent)."

bundles:
  - id: EXTERNALIST
    includes: [CONTRARY, OPENQ, CAST, STEEL, BOUNDARY, CHORUS, UNFRAME]
 
