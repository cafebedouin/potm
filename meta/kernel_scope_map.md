---
id: potm.meta.kernel_scope_map.v1_1
title: kernel_scope_map
display_title: "PoTM Kernel Scope Map"
type: meta
status: stable
version: 1.1
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: ""
  practitioner_doc: ""
  supersedes: [potm.meta.kernel_scope_map.v1_0]
  superseded_by: []
interfaces: [scaling, governance, ethos_alignment]
applicability: [P1, P2, P3, P4, P5]
intensity: gentle
preconditions: []
outputs: [scope_diagnosis, transition_recommendation]
cadence: []
entry_cues: ["unclear if module belongs in my kernel", "scaling PoTM practice beyond current group size"]
safety_notes: ["Use demand-driven scaling to avoid unnecessary complexity", "Do not load higher-scope modules without clear need"]
tags: [forge_origin:kernel_design, spiral_eval:scope_clarity]
author: "practitioner"
license: CC0-1.0
---

# PoTM Kernel Scope Map (v1.1)

**Purpose:** Define kernel boundaries by scale, preventing feature creep while maintaining coherent expansion paths.
**Current kernel version:** **P1 – Individual** (ethos-aligned modules for P2–P5 not loaded by default).

---

## Scope Levels

| Level                  | Scale  | Purpose                                        | Core Modules                                                               | Added Modules                                                                                                                    | Excluded                                        | Transition Signal                                           |
| ---------------------- | ------ | ---------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------- |
| **P1 – Individual**    | 1      | Direct personal practice with PoTM principles  | Beacons, lenses, two-pass moves, practice cards, checklists, safety checks | —                                                                                                                                | Governance, MSRL, ledgers, formal review cycles | “I keep explaining the same practice to different people”   |
| **P2 – Small Group**   | 2–8    | Coordinated practice in high-trust contexts    | All P1 modules                                                             | Consensus scan, turn-taking, facilitator role, shared session notes                                                              | Persistent roles, federation, enterprise tools  | “We’re losing track of decisions between sessions”          |
| **P3 – Community**     | 10–50  | Sustained practice in a stable container       | All P2 modules                                                             | MSRL (community variant), community ledger, roles (Guardian, facilitators, mentorship), sunset/seed cycles, continuity protocols | Federation, enterprise systems                  | “We have multiple concurrent streams and no central memory” |
| **P4 – Federation**    | 50–300 | Multi-community network with shared principles | All P3 modules                                                             | Full MSRL, federated governance, inter-community consensus, shared KB with versioning, ethical containment systems               | Enterprise integration frameworks               | “Other communities keep asking us how we do X”              |
| **P5 – Institutional** | 300+   | PoTM within large formal entities              | All P4 modules                                                             | Compliance/audit frameworks, AI-augmented workflows, public accountability protocols, legal/regulatory interfaces                | Large-scale public deployment infra             | “Legal/compliance is asking for audit trails”               |

---

## Transition Triggers

> **Demand-driven:** Move to the next scope when coordination needs exceed current tools, not purely on headcount.

---

## Ethos-Aligned but Not Loaded in P1

* MSRL (Multi-Substrate Refinement Loop)
* Multi-agent kernel ring
* Manifesto for ethical containment
* Federation governance protocols
* Enterprise compliance/audit frameworks

These live in PoTM’s design library and can be activated when transitioning to higher scope levels.

---

## Scope Check

* **P1:** “Does this help *me* think/practice better?”
* **P2:** “Does this help *us* coordinate effectively?”
* **P3:** “Does this serve our community’s sustained practice?”
* **P4:** “Does this enable healthy federation with other communities?”
* **P5:** “Does this integrate PoTM principles with institutional requirements?”

**Red flags:** Feeling “bureaucratic” in P1 → You may have accidentally loaded P3+ modules.
Coordination breakdown in P2–P3 → You may need to step up scope.

