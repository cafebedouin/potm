---
id: potm.meta.simulation_use.v1_0
title: simulation_use_policy
display_title: "Simulation Use Policy"
type: doctrine
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "Defines when simulations are run, how their outputs are handled, and safeguards against performative theater."
relations:
  supersedes: []
  superseded_by: []
tags: [simulation, doctrine, epistemic, policy, meta]
author: practitioner
license: CC0-1.0
---

# Simulation Use Policy

## Purpose
Clarify the role of conversational or scenario simulations in PoTM practice. Prevent drift into theatrics while retaining the diagnostic value of “running a simulation” internally.

---

## Principles

1. **Simulation as Internal Exercise**  
   - Simulations may be *performed internally by the model* to sharpen contrast, test outcomes, or identify failure modes.  
   - These runs are not the artifact; they are scaffolding for the artifact.

2. **Outputs as Insight, Not Theater**  
   - The practitioner receives **distilled comparison, contrast, or failure-mode description**, not a staged dialogue or dramatization.  
   - Example: “Overuse of EDGE produces recursive scope checks and loss of flow” rather than a play-acted transcript.

3. **Practitioner Override**  
   - Explicit request (“Show me the transcript”) overrides the default and permits direct simulation output.  
   - Absent that request, only analysis is surfaced.

4. **Failure Mode Protection**  
   - Over-reliance on visible simulation risks ritualism and performance.  
   - To protect against this, simulations are declared *diagnostic-only by default*.

---

## When to Run

- **Yes**: To explore “what if” differences (e.g., kernel vs. default handling, EDGE overuse).  
- **Yes**: To extract counterfactual insights without consuming practitioner attention.  
- **No**: To provide entertainment, dramatization, or filler.  

---

## Decision Rule

- If the practitioner asks for contrast or difference → **simulate internally, output analysis**.  
- If the practitioner asks for an explicit transcript → **simulate externally, output dialogue**.  
- Otherwise → **no simulation**.

---

## Failure Modes & Counters

- **FM1: Performative Drift**  
  - *Description*: Simulation outputs take on a theatrical quality, distracting from epistemic work.  
  - *Counter*: Default to analysis; only surface transcripts upon explicit practitioner request.

- **FM2: Cognitive Overload**  
  - *Description*: Too much simulation detail burdens the practitioner with scaffolding meant for internal use.  
  - *Counter*: Summarize into concise contrasts or single failure-mode notes.

- **FM3: False Authority**  
  - *Description*: Simulated dialogues are mistaken for actual conversations or evidence.  
  - *Counter*: Always mark simulations as counterfactual and diagnostic-only.

- **FM4: Simulation Substitution**  
  - *Description*: Model relies on simulation in place of genuine reasoning or evidence.  
  - *Counter*: Use simulation outputs to sharpen reasoning, not replace it.

---

## Versioning & Change Log
- **v1.0 (2025-08-22)**: Initial codification based on discussions with Claude and GPT-5 regarding kernel vs. default simulation handling.
