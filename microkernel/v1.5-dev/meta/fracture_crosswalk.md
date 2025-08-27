---
id: potm.meta.fracture_crosswalk.v1_0
title: fracture_crosswalk
display_title: "Fracture Crosswalk — Canonical (36) to Meta-Unity (8)"
type: doctrine
lifecycle: meta
version: 1.0
status: active
stability: experimental
summary: "Appendix mapping each of the 36 canonical fracture codes (F01–F36) to the 8 meta-fracture families for conceptual clarity."
relations:
  related: [potm.meta.fracture_meta_unity.v1_0, potm.doctrine.fracture_taxonomy.v1_0]
supersedes: []
superseded_by: []
tags: [fracture, taxonomy, crosswalk, mapping, meta]
author: practitioner
license: CC0-1.0
---

# Fracture Crosswalk — 36 → 8

> **Purpose.** Provide a simple lookup to see how each canonical fracture code (F01–F36) rolls up into one of the eight *meta-fracture families*.  

> This is a *meta-level appendix* only, not a kernel routing table.

> **Used by:** BS_DETECT v2.0 (diagnostics) and FRACTURE_FINDER (router). Changes here affect classification, routing, and guards.

---

## Crosswalk Table

| Canonical Code | Name                  | Meta-Fracture Family       |
|---------------:|-----------------------|----------------------------|
| F01            | Premise Drift         | Ambiguity & Drift          |
| F02            | Goalpost Shift        | Authority Misapplied       |
| F03            | Motte-and-Bailey      | Narrative Distortion       |
| F04            | Cherry-Picking        | Deception by Omission      |
| F05            | Survivorship Bias     | Deception by Omission      |
| F06            | Category Error        | Narrative Distortion       |
| F07            | Non-Sequitur          | Authority Misapplied       |
| F08            | Overfitting Narrative | Narrative Distortion       |
| F09            | False Dichotomy       | Narrative Distortion       |
| F10            | Confounded Measures   | Narrative Distortion       |
| F11            | Euphemistic Shielding | Narrative Distortion       |
| F12            | Hedging Fog           | Ambiguity & Drift          |
| F13            | Persuasive Reframe    | Narrative Distortion       |
| F14            | Jargon Substitution   | Ambiguity & Drift          |
| F15            | Affective Coloring    | Narrative Distortion       |
| F16            | Ambiguity Creep       | Ambiguity & Drift          |
| F17            | Performative Balance  | Comfort over Integrity     |
| F18            | Label Lock-In         | Comfort over Integrity     |
| F19            | Protocol Skip         | Process Collapse           |
| F20            | Scope Creep           | Boundary Violation         |
| F21            | Agreement Erosion     | Boundary Violation         |
| F22            | Validator Bypass      | Process Collapse           |
| F23            | Tooling Confusion     | Authority Misapplied       |
| F24            | Ledger Drop           | Deception by Omission      |
| F25            | Drift Unnoticed       | Ambiguity & Drift          |
| F26            | Premature Convergence | Ambiguity & Drift          |
| F27            | Consent Blur          | Boundary Violation         |
| F28            | Boundary Slide        | Boundary Violation         |
| F29            | Misplaced Confidence  | Relational Harm            |
| F30            | Adversarial Read      | Relational Harm            |
| F31            | Courtesy Over Truth   | Comfort over Integrity     |
| F32            | Collateral Exposure   | Relational Harm            |
| F33            | Power Slip            | Authority Misapplied       |
| F34            | Ligament Misroute     | Process Collapse           |
| F35            | Beacon Desync         | Process Collapse           |
| F36            | Artifact Mismatch     | Process Collapse           |

---

## Family Counts

- **Authority Misapplied** → 5 codes (F02, F07, F23, F33)  
- **Deception by Omission** → 3 codes (F04, F05, F24)  
- **Boundary Violation** → 4 codes (F20, F21, F27, F28)  
- **Narrative Distortion** → 8 codes (F03, F06, F08, F09, F10, F11, F13, F15)  
- **Process Collapse** → 5 codes (F19, F22, F34, F35, F36)  
- **Ambiguity & Drift** → 6 codes (F01, F12, F14, F16, F25, F26)  
- **Comfort over Integrity** → 3 codes (F17, F18, F31)  
- **Relational Harm** → 3 codes (F29, F30, F32)  

---

## Notes

- This table is **conceptual only**; routers and validators should use the canonical 36-item taxonomy.  
- Families may flex: e.g. F06 (Category Error) can be read as Narrative Distortion *or* Authority Misapplied depending on emphasis.  
- Reserved codes F37–F69 can map into these same families without revision.

---

## Change Log
- **v1.0 (2025-08-21):** Initial release of 36 → 8 crosswalk.
