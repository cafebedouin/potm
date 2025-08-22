---
id: potm.meta.practice_levels.v1_0
title: practice_levels
display_title: "Practice Levels (P1–P4)"
type: doctrine
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "Canonical definitions and boundary rules for P1–P4. Establishes what each level permits, prohibits, and implies for kernel design."
relations:
  supersedes: []
  superseded_by: []
  related: [potm.guide.practice_levels_implementation.v1_0]
tags: [levels, maturity, capability, kernel_scope, governance]
author: practitioner
license: CC0-1.0
---

# Practice Levels (P1–P4)

## Purpose
Provide canonical, substrate-agnostic definitions of **P1–P4** so that protocols, modules, and kernels can declare applicability and stay aligned to intended scope.

This document defines *what each level means*. For **how to classify, test, or migrate**, see the companion **Implementation Guide**.

---

## Levels at a glance

| Level | Essence | Memory | Agency | Multi-party | Autonomy | Kernel stance |
|------:|---------|--------|--------|-------------|----------|---------------|
| **P1** | **Tool** | Ephemeral (session-local) | None (reactive only) | No | None | Lean onboarding toolbox |
| **P2** | **Apprentice Agent** | Durable per user/team | Limited (offers, routing) | Optional (single team) | Bounded (scheduled/triggered) | Relational charter + memory |
| **P3** | **Mediator / Orchestrator** | Shared, partitioned | Coordinates across roles/agents | Yes (multi-team) | Event-driven workflows | Governance + roles + ledgers |
| **P4** | **Federated Mesh** | Cross-org lineage | Policy-aware, adaptive | Yes (cross-org) | Distributed, policy-gated | Treaties, interop, audit fabric |

---

## Formal definitions

### P1 — Tool Mode
- **Scope:** single practitioner, single session, stateless.
- **Prohibits:** cross-session personalization, proactive nudges, shared state.
- **Allows:** declarative presets chosen manually, session-local notes, minimal tokens (e.g., `fracture_detected`).
- **Boundary test:** if it remembers or acts without an explicit prompt, it is *not* P1.

### P2 — Agent Mode
- **Scope:** durable per-user/team memory, bounded proactive behaviors, explicit consent.
- **Prohibits:** cross-team sharing by default; opaque adaptation.
- **Boundary test:** adapts across sessions for same user/team **and** can initiate bounded actions.

### P3 — Mediator Mode
- **Scope:** multi-user shared workspace; roles, permissions, and auditability required.
- **Prohibits:** uncontrolled cross-role data flow; unlogged mediation.
- **Boundary test:** coordinates between distinct actors with shared state.

### P4 — Federated Mesh
- **Scope:** cross-organization trust fabric; policy portability; lineage tracking.
- **Prohibits:** federation without treaties; unverifiable claims.
- **Boundary test:** operates across organizational membranes with enforceable policy.

---

## Triggers that bump a system up
- **P1 → P2:** any persistence applied across sessions; auto-tuning; scheduled prompts.
- **P2 → P3:** shared state between multiple users/roles; mediation.
- **P3 → P4:** cross-org data exchange; federated policy enforcement.

---

## Anti-patterns
- **Hidden P1 memory:** storing preferences implicitly.
- **P2 without doctrine:** proactive nudges but no consent/override.
- **P3 without audit:** cross-user handoffs with no logs.
- **P4 without treaties:** federation by ad-hoc API alone.

---

## Design guidance by level
- **P1:** keep kernel lean; tool menu + micro-moves; disclose “runs in P1 tool mode.”
- **P2:** add role charter, memory schema, consent gates.
- **P3:** add shared ledger, permissions, mediation protocols.
- **P4:** add federation treaties, lineage exchange, interop constraints.

---

## Companion Guide
For **practical classification tools, boundary tests, compliance checks, and migration paths**, see:
`/practitioner/human/guides/potm.guide.practice_levels_implementation.v1_0.md`

---

## Versioning & change log
- **v1.0** — Canonical definitions for P1–P4; trimmed doctrine file. Implementation details moved to companion guide.
