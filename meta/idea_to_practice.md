---
id: potm.proto.idea_to_practice.v1_2
title: idea_to_practice
display_title: "Idea → Practice Flow"
type: guideline
status: stable
version: 1.2
stability: core
relations:
  relation_to_agent_protocol: none
  practitioner_doc: meta/idea_to_practice.md
  supersedes: [potm.proto.idea_to_practice.v1_1]
  superseded_by: []
interfaces: [idea_garden, bazaar_cathedral_archive]
applicability: [P0, P1, P2, P3, P4]
intensity: adaptive
preconditions: []
outputs: [practice_item, idea_garden_entry]
cadence: ["as_insight_occurs"]
entry_cues: ["new insight", "detected gap", "new affordance"]
safety_notes: ["Minimum viable ≠ ready to ship", "Impact ratings are provisional hypotheses"]
tags: [meta, forge_origin:aug-12-2025, spiral_eval:live]
author: "practitioner"
license: CC0-1.0
---

## Purpose
Structured path for moving from raw insight to active practice without creating operational drag. Preserves ideas that aren’t ready, while preventing premature shipping.  
Integrates with **Bazaar → Cathedral → Archive** lifecycle to ensure ideas are periodically re-evaluated.

## Flow
1. **Spot the Insight**  
   Triggered by a need, gap, or novel affordance.

2. **Push to Logical Extreme**  
   Draft the maximal form without scope restraint.

3. **Strip to Minimum Viable Form**  
   Reduce complexity until only the smallest potentially usable form remains.

4. **Evaluate for Current Fit** *(Bazaar framing)*  
   **Scoring Matrix:** Rate the idea’s *Impact* and *Effort* (High/Low).  
   - **Impact rating is a provisional hypothesis** until tested in live practice.  
   - High Impact / Low Effort → strong candidate for shipping.  
   - Low Impact / High Effort → likely shelve or discard.  
   Also consider maturity of current practice and environment support.

5. **Decision**  
   - **Ship:** Integrate into active practice (kernel, module, card, etc.).  
   - **Shelve:** Park in Idea Garden (Bazaar holding space) with tags + lineage.  
   - **Discard:** Remove entirely if neither current nor future value is likely.

## Feedback Loops
- **Ship → Spot the Insight:** Shipping generates real-world signals that may trigger new insights or reveal missing maximal forms.  
- **Shelve → Evaluate/Strip:** Shelved ideas are revisited as practice maturity changes.  
- **Shelve → Idea Garden review cycle:** Park in `/plots/` and follow seasonal review and compost/transplant rules in `experimental/README.md`.  
- **Archive Review:** Quarterly garden reviews + annual deep cull prevent drift into intellectual graveyard state.

## Intensity
Adaptive — the scaffolding is cognitively light, but the content of an insight may demand gentle handling or high-rigor build-out depending on its nature.

## Optional Collaborative Layer
For multi-agent contexts, insert a **Stakeholder Alignment** check before Decision: “Does this align with the needs, timing, and constraints of the group/system?”

## Lineage
- Forge: emergent from MSRL down-scaling discussion (Aug 12, 2025).  
- Spiral: refined with Gemini audit and lifecycle integration (Aug 12, 2025).


