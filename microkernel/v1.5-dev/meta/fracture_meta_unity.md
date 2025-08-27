---
id: potm.meta.fracture_meta_unity.v1_0
title: fracture_meta_unity
display_title: "Fracture Taxonomy — Meta-Unity Layer"
type: doctrine
lifecycle: meta
version: 1.0
status: active
stability: experimental
summary: "Conceptual condensation of the 36 canonical fracture codes into fewer than 10 'first-order' fracture families, for theoretical clarity and training."
relations:
  related: [potm.doctrine.fracture_taxonomy.v1_0, potm.tactic.fracture_finder.v1_0, potm.tactic.bs_detect_v2.v2_0]
supersedes: []
superseded_by: []
tags: [fracture, taxonomy, meta, compression, theory, practitioner-training]
author: practitioner
license: CC0-1.0
---

# Fracture Meta-Unity Layer

> **Purpose.** This file condenses the **36 canonical fracture codes (F01–F36)** into a minimal set of *conceptual meta-fractures*. It is not meant for real-time routing inside a kernel, but as a **theoretical lens** and **training scaffold**.  
>  
> Canonical reference (36) = *practical router*  
> Meta-unity (≤10) = *conceptual skeleton*
> **Used by:** BS_DETECT v2.0 (diagnostics) and FRACTURE_FINDER (router). Changes here affect classification, routing, and guards.

---

## Meta-Fracture Families

### 1. Authority Misapplied
- **Core Idea:** Decisions, arguments, or actions justified by misplaced or unchecked authority.  
- **Absorbs:** Non-Sequitur (F07), Tooling Confusion (F23), Power Slip (F33), Goalpost Shift (F02) in some cases.  
- **Essence:** “Because I said so,” in form, tool, or role.

### 2. Deception by Omission
- **Core Idea:** Integrity breaks caused by leaving out critical information.  
- **Absorbs:** Cherry-Picking (F04), Survivorship Bias (F05), Ledger Drop (F24).  
- **Essence:** What’s *missing* is more telling than what’s present.

### 3. Boundary Violation
- **Core Idea:** Crossing a defined line—scope, agreement, or consent—without renegotiation.  
- **Absorbs:** Scope Creep (F20), Agreement Erosion (F21), Consent Blur (F27), Boundary Slide (F28).  
- **Essence:** Integrity = staying inside agreed boundaries.

### 4. Narrative Distortion
- **Core Idea:** The story overshadows the signal; narrative is bent to fit convenience.  
- **Absorbs:** Overfitting Narrative (F08), False Dichotomy (F09), Affective Coloring (F15), Persuasive Reframe Trap (F13).  
- **Essence:** The *frame* dictates the truth instead of the evidence.

### 5. Process Collapse
- **Core Idea:** The integrity mechanism itself fails to engage.  
- **Absorbs:** Protocol Skip (F19), Validator Bypass (F22), Beacon Desync (F35), Artifact Mismatch (F36).  
- **Essence:** The safety rails fail at the very moment they’re required.

### 6. Ambiguity & Drift
- **Core Idea:** Meaning, aim, or thread loses anchor and slides away.  
- **Absorbs:** Premise Drift (F01), Ambiguity Creep (F16), Drift Unnoticed (F25), Premature Convergence (F26).  
- **Essence:** Direction or meaning quietly dissolves.

### 7. Comfort over Integrity
- **Core Idea:** Politeness, convenience, or status quo maintenance overrides truth.  
- **Absorbs:** Courtesy Over Truth (F31), Performative Balance (F17), Label Lock-In (F18).  
- **Essence:** Integrity sacrificed to avoid friction.

### 8. Relational Harm
- **Core Idea:** Breaches of dignity or exposure of others.  
- **Absorbs:** Collateral Exposure (F32), Misplaced Confidence (F29), Adversarial Read (F30).  
- **Essence:** Integrity as relational safety and care.

---

## Why Keep Both Layers?

- **36-item canon:** Precise enough for routers, protocols, and kernel integration.  
- **Meta-unity (<10):** Elegant enough for philosophy, onboarding, and practitioner training.  

Together they form a two-level taxonomy:  
- *Canonical*: operational granularity.  
- *Meta*: conceptual unity.

---

## Notes

- This file is **not kernel-bound**. It should live in `meta/` as a doctrinal reflection.  
- Practitioners can practice “zooming out” by asking: *Which meta-fracture family is this instance of F## part of?*  
- Reserved codes (F37–F69) can map directly into these families.

---

## Change Log
- **v1.0 (2025-08-21):** Initial condensation into 8 meta-fracture families.
