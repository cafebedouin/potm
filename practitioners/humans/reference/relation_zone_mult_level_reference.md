---
id: potm.tactic.relation_zone_multi_level.v0_2_2
title: relation_zone_multi_level_reference
display_title: "RELATION_ZONE — Multi-Level Diagnostic"
type: tactic
subtype: diagnostic
lifecycle: idea_garden
version: 0.2.3
status: draft
stability: experimental
summary: "Diagnostic tool for mapping relational dynamics across dyad, community, and meta scales, balancing precision with recognition of generative messiness."
relations:
  supersedes: [potm.tactic.relation_zone_multi_level.v0_2_2]
  superseded_by: []
tags: [relation_zone, messy_is_normal, multi_level, diagnostic, experimental]
author: practitioner
license: CC0-1.0
---

# RELATION_ZONE — Multi-Level Diagnostic (v0.2.3)

---

## Purpose
A structured diagnostic for assessing relational dynamics across scales (dyad, community, meta). Maps relationships on a gradient from **Exploitative → Messy → Insight**, while preventing two failure modes:  
1. **False precision** (treating % as math).  
2. **Exit-bias** (over-relying on containment/exit when adapt-in-place or generative messiness are viable).  

---

## Procedure

### Step 0 — Beacon Check: messy_is_normal
Before diagnosing, pause:

- Is this friction **destructive** (erodes trust, induces harm)?  
- Or **generative** (sparks new categories, builds shared language)?  

➡️ If **generative**, pause the diagnostic. Cultivate the process directly.

---

### Step 1 — Dyad Zone Estimate
Assign a **qualitative label + % guide**:  
- **Exploitative (≤30%)** → assume toxicity, default to exit/contain.  
- **Messy (30–80%)** → see sub-bands below.  
- **Insight (≥80%)** → cooperative baseline, maintain & grow.  

⚠️ Percentages are *guides, not exact measures*. Labels are primary.

#### Messy Sub-Bands
- **M-Low (30–45%):** Chronic deflect/defend → **boundary-first** (time limits, topic containment).  
- **M-Mid (45–65%):** Mixed honesty → **repair possible** via **staged trust** (small → larger agreements).  
- **M-High (65–80%):** Mostly cooperative, ego spikes → **cultivate-lite** (interpretive ledger for friction points).  

---

### Step 2 — Community Baseline Check
Score weighted indicators (trust density, truth-telling safety, deception frequency, reputation recovery, conflict handling).  
- **Low (≤30):** Assume exploitative.  
- **Medium (31–65):** Messy → cross-check dyad.  
- **High (≥66):** Cooperative → support Insight path.  

---

### Step 3 — Meta-Level Transition Difficulty
Evaluate constraints:  
- **Low:** High mobility, low cost (switching teams).  
- **Medium:** Regional / network rebuild.  
- **High:** Binding constraints (familial, legal, financial).  

➡️ If **High**, favor **Adapt-in-Place**.  
➡️ If **Low/Medium**, pilot exit or structural shift is viable.  

---

## Outputs

Standard JSON-style bundle:

```json
{
  "dyad_zone": "M-Mid",
  "dyad_confidence": "medium",
  "community_baseline": 55,
  "meta_transition_difficulty": "High",
  "recommended_action": "Adapt-in-Place"
}
