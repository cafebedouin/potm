---
id: potm.tactic.bs_detect.v2_0
title: bs_detect_v2
display_title: "BS-DETECT v2.0 — Fracture-Routed Bullshit Detection"
type: tactic
subtype: diagnostic
lifecycle: idea_garden
version: 2.0
status: active
stability: experimental
summary: "Detect evasions, classify via F1–F69 taxonomy, route next steps, and ledger artifacts—all session-local."
relations:
  supersedes: []
  superseded_by: []
  related:
    - potm.meta.fracture_finder.v1_3_1
tags: [bs_detect, diagnostic, fracture, router, P1]
author: practitioner
license: CC0-1.0
---

# BS-DETECT v2.0

## Concept
1. Detection → 2. Classification → 3. Routing → 4. Ledgering  
2 organizing axes:  
- Taxonomy IDs: F1–F69  
- Clusters: Theatrical, Conversational, Procedural, Epistemic, Relational  
Plus a lattice quadrant (Surface/Structural × Conversational/Procedural)  

## Inputs
- `prompt` (str)  
- `model_output` (str)  
- `session_window` (array[str])  
- `policy_state` (object)

## Outputs
- **bs_detect_v2.json**  
  ```json
  {
    "probe": "<ad_hoc|EDGE|…>",
    "fids": ["F1","F13"],
    "clusters": ["Theatrical","Conversational"],
    "lattice": {"depth":"Surface","domain":"Conversational"},
    "evidence": ["…snip…","…snip…"],
    "disconfirmers": ["…session snip…"],
    "escape_routes_found":[{"type":"SIMULATION_ONLY","snippet":"…"}],
    "severity":"low|med|high|critical",
    "route":"FORCE_ARTIFACTS|EDGE_PRESS|FACTCHECK|CONTAINMENT|GUARDIAN",
    "route_contract_ref":"route_contract.json",
    "notes":"short rationale"
  }
