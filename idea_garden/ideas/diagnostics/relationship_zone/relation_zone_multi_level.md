---
id: potm.tactic.relation_zone_multi_level.v0_2_2
title: relation_zone_multi_level_diagnostic
display_title: "RELATION_ZONE — Multi-Level Diagnostic"
type: tactic
subtype: diagnostic
lifecycle: idea_garden
version: 0.2.2
status: draft
stability: experimental
summary: "Multi-scale diagnostic for relational health (dyad/community/meta). Integrates critiques on illusion of precision, exit-bias, and reframes Messy as generative."
relations:
  supersedes: [potm.tactic.relation_zone_multi_level.v0_2_1]
  superseded_by: []
tags: [relation_zone, community_baseline, nested_context, diagnostics, lenses, messy_is_normal]
author: practitioner
license: CC0-1.0
---

# RELATION_ZONE — Multi-Level Diagnostic (v0.2.2)

## Purpose
Diagnose relational dynamics across **three nested scales** (dyad, community, meta) to guide whether to **repair, exit/contain, or cultivate**. Prevents misapplied dyadic fixes in hostile fields.  
This version integrates critiques: avoid illusion of precision, watch for exit-bias, and acknowledge Messy as a potentially generative baseline.

---

## Model
**Gradient:** Exploitative (0–10%) → Messy (10–90%) → Insight (90–100%)

**Messy sub-bands:**  
- **M-Low (30–45%):** Chronic deflect/defend; **boundary-first** (e.g., time limits, topic containment).  
- **M-Mid (45–65%):** Mixed honesty; **repair possible** with staged trust (small agreements → larger).  
- **M-High (65–80%):** Mostly cooperative; **cultivate-lite** (e.g., interpretive ledger for friction points).  

**Scales:** Dyad (micro) · Community (meso) · Meta-community (macro)

---

## When to Run
- **Dyad-only:** single tie, stable context.  
- **Multi-level:** repeated failures, community-dependent stakes, or major moves (relocation/sector).

---

## Procedure

### Step 1 — Dyad Read
- Place on gradient → label + % + confidence; cite behaviors.  
- **Confidence guide:**  
  - 0.9–1.0 = clear patterns, multiple data points.  
  - 0.7–0.8 = likely, needs validation.  
  - ≤0.6 = speculative, hypothesis only.  

**Output:** `dyad: {zone, percent, confidence, evidence[]}`

---

### Step 2 — Community Baseline
Use if patterns repeat or stakes involve community reliance.  

**Weighted indicators (≥2):**
- Trust density (0.4)  
- Truth-telling safety (0.4)  
- Deception frequency (0.4)  
- Reputation recovery (0.3)  
- Conflict handling (0.3)  

**Heuristics:**  
- High-function ≥70%  
- Mixed 30–70%  
- Dysfunctional ≤30%

**Output:** `community: {zone, percent, indicators[]}`

---

### Step 3 — Cross-Level Adjustment

| Dyad zone        | Community baseline   | Adjustment logic | Action              |
|------------------|----------------------|------------------|---------------------|
| Insight (≥80%)   | High (≥70%)          | None             | Cultivate           |
| Messy (40–80%)   | High (≥70%)          | Raise floor      | Improve +10%        |
| Messy (40–80%)   | Dysfunctional (≤30%) | Lower ceiling    | Contain / Exit      |
| Exploit (≤20%)   | Any                  | Safety override  | Immediate Exit       |

**Safety default:** baseline ≤30 → assume toxicity.  
**Bias correction:** Dysfunctional fields normalize “Messy”; high-function fields over-pathologize it.

---

### Step 4 — Meta-Community
Run if considering big moves (region/sector).  

**Factors:** mobility, selection effects, institutional support, economic pressure.  

**Transition Difficulty Guide:**  
- **Low:** High mobility, low cost (e.g., switching remote teams).  
- **Medium:** Moderate barriers (e.g., regional move with network rebuild).  
- **High:** Binding constraints (e.g., familial, legal, financial locks).  

**Transition rules:**  
- Constraints dominate / low mobility → **Adapt-in-Place**: shrink exposure, seek micro-pockets, time-box search.  
- Opportunities exist → **Pilot** small moves before committing.  

**Output:** `meta: {context, opportunities[], constraints[], transition_difficulty}`

---

## Tools by Zone
- **Exploitative (0–10):** Contain / Exit; never repair.  
- **Messy (sub-bands):**  
  - M-Low → boundary-first.  
  - M-Mid → +10% repair.  
  - M-High → cultivate-lite.  
- **Insight (90–100):** Interpretive Ledger, joint sense-making; guard against drag.

---

## Quick Triggers
Dyad only (clear/stable) · Add Community (repeats/stakes) · Add Meta (big moves).

---

## Failure Modes & Counters
- Over-fixing in bad fields → cap cycles + exit plan.  
- Romanticizing “tight-knit” → test truth-safety.  
- Ignoring meta → name ≥1 lever per decision.  
- Sampling bias → require ≥2 weighted indicators.  

---

## Example — Before/After
**Before:** “Boss Messy 50 → Drift-Tolerant Waiting.”  
**After Community Check:** baseline 30 → Contain/Exit.

---

## Limitations & Research Needs
- **Illusion of precision:** % and sub-bands are **guides, not exact measures**. Treat labels qualitatively.  
- **Exit bias:** Model leans toward contain/exit. In **familial or binding communities**, repair may be non-optional despite tactical irrationality.  
- **Messy as feature:** Friction/ambiguity can be **generative**, not just pathology. Messy ≠ failure; often baseline human condition.  
- **Subjectivity:** Indicators remain judgment-heavy; need calibrated examples.  
- **Evidence base:** Heuristic, experimental; requires case logs & cross-cultural testing.

---

## Field Test Note
1. **Log 3 Cases:** Test with one dyad in each zone (Messy-Low, Messy-Mid, Insight).  
2. **Check Adjustments:** Did the community/meta layers change your action?  
3. **Refine Confidence:** Calibrate your % estimates against outcomes.  

---

## Appendix — Generative Messiness Note
> Messy interactions are not always problems to solve. They can be crucibles for resilience, creativity, and unexpected collaboration.  

**Example:**  
A team’s "Messy" debate over priorities surfaced **three new project categories** and a shared language for tension. The friction was **generative**, not pathological.  

**Practitioner probe:**  
- Is this messiness destructive, or producing **new categories / bonds**?  
- Am I pathologizing normal friction?  
- Could this ambiguity itself be leveraged as material, rather than escaped?  

Beacon: `messy_is_normal`

---

## Outputs (uniform payload)

```json
{
  "dyad": {"zone":"Messy","percent":55,"confidence":0.7,"evidence":["deflects specifics twice"]},
  "community": {"zone":"Mixed","percent":60,"indicators":["truth rewarded","gossip common"]},
  "adjustment": {"logic":"raise_floor","recommended_action":"improve_10","tool_hint":"DriftTolerantWaiting"},
  "meta": {"context":"remote-startup-tri-culture","opportunities":["talent breadth"],"constraints":["norm clash"],"transition_difficulty":"medium"}
}
