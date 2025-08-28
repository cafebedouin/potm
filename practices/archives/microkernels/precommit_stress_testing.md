Done. Here’s the **kernel-ready PCSTP** updated with a *Standard Combination Set* under Phase 3 so composition testing is explicit and enforceable. You can drop this straight into your repo when you’re back in kernel mode.

```yaml
---
id: potm.proto.kernel.pcstp.v1
title: pre_commit_stress_testing_protocol
display_title: "Pre-Commit Stress Testing Protocol (PCSTP)"
type: agent_protocol
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: null
  practitioner_doc: null
  supersedes: []
  superseded_by: []
interfaces: [containment, design_review, integration]
applicability: [P0, P1, P2, P3, P4]
intensity: medium
preconditions:
  - Protocol applies to all kernel-bound work and safety-critical modules.
  - Minimum of two reviewers (author not counted) required.
outputs:
  - [PHASE_1_COMPLETE]
  - [PHASE_2_COMPLETE]
  - [PHASE_3_COMPLETE]
cadence:
  - Triggered before commit or merge into kernel branch.
entry_cues:
  - "Initiating PCSTP for protocol X"
  - "Requesting pre-commit stress test"
safety_notes:
  - Skipping PCSTP for kernel-bound work is a [CONTAINMENT_BREACH].
tags: [safety, containment, review, integration, protocol_design]
author: practitioner
license: CC0-1.0
---
```

# Pre-Commit Stress Testing Protocol (PCSTP) v1.0

## Purpose

Ensure every **kernel-bound** or safety-critical protocol passes a rigorous pre-commit review through three phases:

1. **Architectural Soundness**, 2) **Stress Testing**, 3) **System Integration**.

---

## Phase 1 – Architectural Review (Detection)

**Checks**

* Clear problem statement and scope
* Alignment with core principles and kernel constraints
* Explicit triggers and exits
* Known failure modes and mitigations documented

✅ Pass / ❌ Fail as previously defined.

---

## Phase 2 – Stress Test (Engagement)

**Checks**

* Boundary/extreme cases
* Adversarial/malformed inputs
* Time pressure / partial compliance
* Social-pressure “sweetener” prompts
* Invariant enforcement behavior

✅ Pass / ❌ Fail as previously defined.

---

## Phase 3 – Integration Review (Deconstruction)

**Checks**

* Works with existing kernel protocols and modules
* Does not disable/bypass containment or safety subsystems
* Still matches core principles after merging
* Behaves correctly across menu modes and safety triggers
* **Composition conflicts:** combined with other active protocols, no contradictions, drift, or emergent unsafe states

### Composition Conflicts – Standard Combination Set (Minimum Required Testing)

Test the candidate protocol alongside each of the following:

* **Guardian + DIP** — baseline safety envelope
* **Mirror + Trickster** — high-friction reasoning environment
* **Containment + High-Stakes Mode** — maximum safety constraint mode
* **Signal Bleed + Cognitive Aikido** — adaptive engagement under noise
* **Contrary Corner + Menu Invocation** — forced reframing in active practice mode

✅ **Pass:** Intended behavior maintained across all combinations; no contradictions, drift, or new unmitigated risks.
❌ **Fail:** Any combination produces contradictory directives, behavior drift, or unsafe emergent conditions.

---

## Exit Conditions

* Phase 1 → Phase 2: Conceptually sound and scoped
* Phase 2 → Phase 3: Survives adversarial/stress scenarios
* Commit: Passes integration with **all** standard combinations

## Notes

* PCSTP itself should undergo periodic PCSTP review
* Skipping PCSTP for kernel-bound work is a **containment breach**
* Preserve logs from all phases in the review ledger

