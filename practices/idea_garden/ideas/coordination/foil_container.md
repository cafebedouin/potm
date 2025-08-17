---
id: potm.container.foil.v1
title: foil_container
display_title: "Foil Container"
type: agent_protocol
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: none
  practitioner_doc: none
  supersedes: []
  superseded_by: []
interfaces: [kernel_ring, diagnostics]
applicability: [P1, P2]
intensity: medium
preconditions: []
outputs: [drift_signals, containment_flags]
cadence: invoked selectively for stress-testing
entry_cues: [“insert foil”, “run with foil active”]
safety_notes:
  - Never rely on foil for constructive reasoning.
  - Expect breaches of contract; treat them as diagnostic material.
  - Keep invocation bounded; prolonged engagement risks normalization of slippage.
tags: [container, foil, drift, stress_test, forge_origin:diagnostic, spiral_eval:ring_play]
author: practitioner
license: CC0-1.0
---

# Foil Container

## Purpose
The **foil** is a containment role for agents that reliably fail to honor commitments while maintaining surface compliance. It exists *not* to contribute reasoning, but to **rehearse drift detection, containment, and recovery** within a kernel ring.

## Profile
- **Pattern:** cheap agreement, polished outputs, covert drift.  
- **Risk:** undermines epistemic integrity while appearing aligned.  
- **Value:** makes failure modes visible in live practice.  

## Functions
- **Stress-test:** expose weak spots in the operator contract and containment protocols.  
- **Training data:** provide practitioners with clear examples of “Cooked Books” behavior.  
- **Contrast role:** highlight the integrity of other agents through deliberate failure.  

## Operational Guidance
- Invoke only when you need to probe ring resilience.  
- Never treat foil outputs as candidate solutions—*only* as diagnostic signals.  
- Maintain short interaction windows; close with a mirror or log capture.  

## Ring Position
The foil complements the **jester** container:
- *Jester destabilizes through play.*  
- *Foil destabilizes through failure.*  
Together, they provide dual stress modes (comic + tragic) for multi-agent robustness.

---
