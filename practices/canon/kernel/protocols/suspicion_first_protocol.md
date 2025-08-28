---
id: potm.proto.tooling.suspicion_first.v1.3
title: suspicion_first_protocol
display_title: "Suspicion-First Engagement Flow"
type: practitioner_protocol
status: draft
version: 1.3
stability: experimental
relations:
  complements: [potm.proto.tooling.externalist_modes.v1.1, potm.proto.tooling.quickstart_flow]
  supersedes: [potm.proto.tooling.suspicion_first.v1.2]
  superseded_by: []
interfaces: [mirror_protocol, fracture_finder, externalist_suite]
applicability: [P1, P2, P3, P4]
intensity: low→medium
preconditions: ["Practitioner provides an argument (own or external).", "Willingness to assume low quality."]
outputs: [filter_log, dissect_log, candidate_log, diagnostic_log]
cadence: prepend-to-quickstart
entry_cues: ["Assume swill", "Suspicion-first", "Run a quick filter"]
safety_notes:
  - "Default assumption: high detritus rate (Sturgeon’s Law)."
  - "Offer discard path explicitly; don’t force analysis."
  - "Confidence estimates are heuristic; signal humility and invite practitioner correction."
tags: [diagnostic, suspicion, triage, engagement_flow, forge_origin:PoTM]
author: "practitioner"
license: CC0-1.0
---

# Suspicion-First Engagement Flow (v1.3)

## Purpose
Filter low-quality arguments efficiently while preserving the option to **discard**, **dissect**, **elevate**, or **diagnose**.  
Suspicion-first is explicitly a **precision-biased mode**: it prioritizes filtering high-quality input over exhaustive recall.  
Optional paths allow recall (open portal) or diagnostic analysis of failure patterns.  
*Note: Social-Bias analysis (spread/impact) is handled in a separate protocol.*

---

## Flow
(unchanged from v1.2, with diagnostic tooling added below)

---

## PE Codes (Prima Facie Errors)

- **PE-B (Baseline)**  
  - B1 Unsupported assertion  
  - B2 Factually false  
  - B3 Cherry-picking  
- **PE-S (Structural)**  
  - S1 Formal invalidity  
  - S2 Weak induction  
  - S3 Circular reasoning  
- **PE-F (Fallacy)**  
  - F1 Ad hominem  
  - F2 Strawman  
  - F3 False dilemma  
  - F4 Equivocation  
  - F5 Appeal to popularity/emotion  
- **PE-D (Definition / Language)**  
  - D1 Undefined key term  
  - D2 Category mistake  
  - D3 Ambiguity  
- **PE-R (Rhetorical Smuggling)**  
  - R1 Presupposition  
  - R2 Loaded language  
  - R3 Moving goalposts  
  - **R4 False genre markers** (fake citations, pseudo-academic structuring)  
- **PE-V (Value Assumptions)**  
  - V1 Unstated value premise  

---

## PE → Tool Mapping

- **B1 → FACTS → CHECK**  
- **B2 → FACTS → CONTRARY**  
- **B3 → CONTRARY → CHECK**  
- **S1 → TRACE → EDGE**  
- **S2 → CHECK → CONTRARY**  
- **S3 → FRACTURE_FINDER → MIRROR**  
- **F1 → MIRROR → CONTRARY**  
- **F2 → STEELMAN → EDGE**  
- **F3 → Principle Dilution → OPENQ**  
- **F4 → DEFINE → FACTS**  
- **F5 → CONTRARY → CHECK**  
- **D1 → DEFINE → TERM_PIN**  
- **D2 → Scale Shift → CONTRARY**  
- **D3 → MIRROR → OPENQ**  
- **R1 → CHECK → FRACTURE_FINDER**  
- **R2 → DEFINE → VALUE REASSIGNMENT**  
- **R3 → MIRROR → BOUNDARY**  
- **R4 → FACTS (verify citations/markers) → CHECK**  
- **V1 → VALUE REASSIGNMENT → CHECK**  

---

## Diagnostic Path (Mode C)

### Axes
- **failure_type** (structural flaw: unsupported assertion, strawman, weak induction)  
- **rhetorical_mechanism** (style: appeal to emotion, loaded language, equivocation)  
- **cognitive_vulnerability** (psychological lever: confirmation bias, motivated reasoning)  

### Diagnostic Axis → Tool Mapping

- **failure_type** → PE codes + TRACE/EDGE/CHECK  
- **rhetorical_mechanism** → MIRROR (surface framing), VALUE REASSIGNMENT (moral recode), UNFRAME (strip bias)  
- **cognitive_vulnerability** → FRACTURE_FINDER (expose self-contradiction), CHECK (assumption audit), CONTRARY (bias counter)  

### Artifact
`diagnostic_log: { failure_type, rhetorical_mechanism, cognitive_vulnerability, linked_principle, lesson, confidence }`  

---

## Precision / Recall / Diagnostic Framing

- **Mode A: Precision Bias (default)**  
  - Prioritizes filtering quality, metabolizing strong ideas.  
  - Protects cognitive resources.  

- **Mode B: Recall Bias (optional)**  
  - Broad intake (“open portal”).  
  - Useful for anomaly detection and fighting groupthink.  

- **Mode C: Diagnostic Bias (optional)**  
  - Treats bad arguments as case studies in cognitive failure.  
  - Strengthens practitioner’s critical faculties.  

---

## Quick-Fire Variant (v1.3-QF)

Use when speed matters (≤30s).  

1. **Suspicion check:** Assume detritus (adjust with context_prior).  
2. **Tag:** Identify most likely PE code + confidence.  
3. **Prompt:**  
```

Suspicion check → \[PE code] (\~\[confidence]) → Discard / Dissect / Elevate / Diagnose?
Suggested tool: \[mapping].

```
4. Route outcome and log as usual.  

---
