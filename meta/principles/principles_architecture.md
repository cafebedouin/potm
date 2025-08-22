---
id: potm.meta.principles.architecture.v1
title: principles_architecture
display_title: "Principles Architecture"
type: guideline
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: null
  practitioner_doc: meta/principles/
  supersedes: []
  superseded_by: []
interfaces: [doctrine_principle_relation, values_integrity_audit, meta_log_layer, doctrine_mutation_vectors]
applicability: [P0, P1, P2, P3, P4]
intensity: n/a
preconditions: []
outputs: [principle_file, stress_test_pack, registry_entry]
cadence: [review_annually, review_on_major_drift]
entry_cues: ["new principle emerges", "principle drift detected"]
safety_notes: ["Changes require multi-vector confirmation."]
tags: [principles, governance, ethics, epistemic]
author: practitioner
license: CC0-1.0
---

# Principles Architecture — Scaffold

This document standardizes **how a Principle is defined, tested, adopted, reviewed, and retired** in PoTM.

## 1) Principle Types (taxonomy)
- **ethical** — dignity, harm, agency
- **epistemic** — truth/validity, evidence thresholds
- **aesthetic** — tone, design, symbolic fit
- **relational** — consent, boundaries, presence
- **operational** — practice-first, non-simulation, filtering-first

> Use the most specific single type; add a secondary type only if truly cross-cutting.

## 2) Principle File Schema (per-principle)
Every principle gets its own file under `meta/principles/registry/`. Use this exact front-matter and body layout.

```yaml
---
id: potm.principle.<slug>.v1
title: <slug>
display_title: "<Human-facing title>"
type: principle
status: proposed | provisional | active | deprecated
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: null
  practitioner_doc: meta/principles/<folder>/<name>.md
  supersedes: []
  superseded_by: []
interfaces: [doctrine_principle_relation, values_integrity_audit, meta_log_layer]
applicability: [P0,P1,P2,P3,P4]
intensity: n/a
preconditions: []
outputs: [stress_tests, audit_fragments]
cadence: [review_annually, review_on_major_drift]
entry_cues: ["principle audit:<slug>"]
safety_notes: ["Revise only with multi-vector confirmation."]
tags: [<type>, principles]
author: practitioner
license: CC0-1.0
---

# Signature
A one-sentence **non-negotiable** (what we refuse to betray).

# Commitments
- Concrete behaviors this principle *demands*.
- Concrete behaviors this principle *forbids*.

# Scope & Boundaries
- Where it applies / where it doesn’t.
- Known tradeoffs (list).

# Doctrine Links
- Doctrines this constrains (list).
- Doctrines this enables (list).

# Strategy Hooks
- Protocols that express this principle (list).
- Required defaults (pre-steps, buffers).

# Antipatterns
- Typical violations and their telltale signs.

# Stress Tests (references)
- Link to `/meta/principles/stress_tests/<slug>_tests.md`.

# Indicators & Drift Signals
- Positive indicators (it’s alive).
- Drift signals (it’s decaying).
- Red flags (breach risk).

# Evidence Log (append only)
- Timestamps + short notes linking to `meta_log_layer` entries, audits, or field notes.
