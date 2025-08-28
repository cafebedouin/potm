---
id: potm.meta.practice_levels.v1_0
title: practice_levels
display_title: "Practice Levels (P1–P4)"
type: doctrine
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "Canonical definitions and boundary tests for P1–P4: what each level permits, forbids, and implies for kernel design."
relations:
  supersedes: []
  superseded_by: []
tags: [levels, maturity, capability, kernel_scope, governance]
author: practitioner
license: CC0-1.0
---

# Practice Levels (P1–P4)

## Purpose
Establish clear, substrate-agnostic definitions for **P1–P4** so protocols can declare applicability and engineers can judge whether a deployment’s **capabilities** and **constraints** match the intended level.

## Scope & audience
- Designers of kernels/modules
- Practitioners selecting deployment modes
- Reviewers enforcing integrity and safety gates

---

## The levels at a glance

| Level | Essence | Memory | Agency | Multi-party | Autonomy | Typical substrate | Kernel stance |
|------:|---------|--------|--------|-------------|----------|-------------------|---------------|
| **P1** | **Tool** | Ephemeral (session-local) | None (reactive only) | No | None | Chatbox / CLI / doc-guided | Lean onboarding toolbox |
| **P2** | **Apprentice Agent** | Durable per user/team | Limited (offers, routing) | Optional (one team) | Bounded (scheduled/triggered) | Persistent service (single tenant) | Relational charter + memory |
| **P3** | **Mediator / Orchestrator** | Shared, partitioned | Coordinating across roles/agents | Yes (multi-team) | Event-driven workflows | Multi-agent runtime | Governance + roles + ledgers |
| **P4** | **Federated Mesh** | Cross-org lineage | Policy-aware, adaptive | Yes (cross-org) | Distributed, policy-gated | Federated platforms | Treaties, interop, audit fabric |

---

## Formal definitions & hard boundaries

### P1 — Tool Mode
- **Prohibits:** cross-session personalization by default; proactive nudges; automated handoffs; shared state.
- **Allows:** declarative presets chosen manually; session-local notes; minimal event tokens (e.g., `fracture_detected`).
- **Boundary test:** If it **remembers or acts without an explicit prompt**, it’s *not* P1.

### P2 — Agent Mode
- **Requires:** durable per-user/team memory; explicit role/consent; limited proactive behaviors (offers, reminders) under doctrine.
- **Prohibits:** cross-team sharing by default; unsupervised escalation; opaque adaptation.
- **Boundary test:** If it **adapts across sessions for the same user/team** and can **initiate bounded actions**, it’s P2.

### P3 — Mediator Mode
- **Requires:** shared ledgers; role & permission models; inter-agent protocols; auditability of handoffs.
- **Prohibits:** uncontrolled data blending; unlogged cross-role actions.
- **Boundary test:** If it **coordinates between distinct actors** with **shared state**, it’s P3.

### P4 — Federated Mesh
- **Requires:** inter-org trust fabric; policy/consent portability; lineage & deprecation paths across boundaries.
- **Prohibits:** breaking federation policies; unverifiable claims.
- **Boundary test:** If it **operates across organizational membranes** with **composable policy**, it’s P4.

---

## Triggers that bump a system up a level

- **P1 → P2:** any persistence auto-applied next session; auto-tuning; scheduled prompts; background jobs.
- **P2 → P3:** shared workspace/ledger used by multiple roles; mediated negotiations; cross-agent orchestration.
- **P3 → P4:** cross-org state exchange; federated policy enforcement; external lineage requirements.

---

## Anti-patterns (reject at review)

- **P1 with hidden memory:** storing preferences implicitly and reusing them next session.
- **P2 without doctrine:** proactive nudges with no refusal/consent gates.
- **P3 without audit:** multi-party handoffs lacking immutable logs.
- **P4 without treaties:** federation by ad-hoc API contracts only.

---

## Design guidance by level

### Kernel shape
- **P1:** menu + micro-moves + minimal tokens; pointers to practitioner guides. No schedulers.
- **P2:** add role charter, memory schema, consent gates, escalation ladders.
- **P3:** add workspace model, permissions, conflict/mediation protocols, shared ledger.
- **P4:** add federation treaties, lineage exchange, interop constraints.

### Safety & integrity
- **P1:** refusal rules, claim hygiene, session disclaimer (“runs in P1 tool mode”).
- **P2:** data minimization, adaptive transparency (“why this nudge”), user override logs.
- **P3:** separation of concerns, least privilege, tamper-evident logs.
- **P4:** policy portability, compliance anchors, cross-org dispute resolution.

---

## Examples (grounding)

- **Custom GPT used by many people, each in siloed sessions:** **P1**.
- **Single-user persistent app that remembers presets and offers follow-ups:** **P2**.
- **Team assistant coordinating tasks across multiple teammates with a shared board:** **P3**.
- **Network of assistants exchanging lineage across organizations under policy:** **P4**.

---

## Migration path (upgrade without rewrite)

1. **Separate form from substrate:** keep P2+/federation features as optional modules.
2. **Declare capability flags:** `capability.memory=durable|session`, `capability.autonomy=none|bounded|orchestrated`.
3. **Promotion checklist:** introduce one requirement at a time (memory → consent → proactive → multi-party → federation), with audits at each step.

---

## Compliance checklist (quick scan)

- [ ] Kernel declares **intended level** and matching capability flags.
- [ ] No feature violates the **prohibitions** of that level.
- [ ] Logs & disclosures match level (e.g., P1 disclaimer present).
- [ ] Handoffs/escalations use level-appropriate protocols.
- [ ] Version noted; deprecation paths defined for upgrades.

---

## Versioning & change log
- **v1.0** — First canonical definition of P1–P4; adds boundaries, triggers, anti-patterns, and compliance checklist.
