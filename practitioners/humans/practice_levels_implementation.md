---
id: potm.guide.practice_levels_implementation.v1_0
title: practice_levels_implementation
display_title: "Practice Levels (P1–P4) Implementation Guide"
type: guide
lifecycle: active
version: 1.0
status: stable
summary: "Practical guidance for classifying, testing, and migrating systems between Practice Levels P1–P4."
relations:
  supersedes: []
  superseded_by: []
  related: [potm.meta.practice_levels.v1_0]
tags: [levels, maturity, capability, kernel_scope, governance, implementation, testing, migration]
author: practitioner
license: CC0-1.0
---

# Practice Levels (P1–P4) Implementation Guide

## Purpose
This guide provides the practical **tools and procedures** necessary to classify, test, and manage the migration of systems through the defined Practice Levels (P1-P4). It serves as the companion to the **Practice Levels (P1-P4) doctrine**, which defines *what each level means*.

---

## Audience
- Engineers and developers implementing kernels/modules.
- Architects designing system deployments.
- Testers and auditors verifying level compliance.
- Project managers planning system evolution.

---

## Classifying a System (Applying Boundary Tests)

To classify a system, apply the formal boundary tests defined in the `potm.meta.practice_levels.v1_0` doctrine document.

### P1 — Tool Mode Boundary Test
- **Test:** Does the system remember or act without an explicit, current user prompt?
- **Result:** If **yes**, it is *not* P1. If **no**, it remains P1.

### P2 — Agent Mode Boundary Test
- **Test:** Does the system adapt its behavior across sessions for the same user or team, **and** can it initiate bounded actions (e.g., offers, reminders) under doctrine?
- **Result:** If **yes**, it is P2. If **no**, it is P1.

### P3 — Mediator Mode Boundary Test
- **Test:** Does the system coordinate between distinct actors (users or agents) with shared state (e.g., a shared ledger or workspace)?
- **Result:** If **yes**, it is P3. If **no**, it is P2.

### P4 — Federated Mesh Boundary Test
- **Test:** Does the system operate across organizational membranes, and does it do so with composable, enforceable policy (e.g., federation treaties, portable consent)?
- **Result:** If **yes**, it is P4. If **no**, it is P3.

---

## Compliance Checklist (Quick Scan)

Use this checklist for a rapid assessment of a system's adherence to its declared Practice Level.

- [ ] Kernel/module declares its **intended Practice Level** and matching capability flags (e.g., `capability.memory=durable|session`, `capability.autonomy=none|bounded|orchestrated`).
- [ ] No feature or behavior observed violates the **prohibitions** of the declared level.
- [ ] System logs, disclosures, and user-facing messages clearly match the declared level (e.g., a P1 system prominently displays a "runs in P1 tool mode" disclaimer).
- [ ] All handoffs, escalations, or data exchanges utilize protocols appropriate for the declared level (e.g., P3 requires immutable, auditable logs for cross-role actions).
- [ ] System version is noted, and clear deprecation paths are defined for future upgrades or level transitions.

---

## Migration Path (Upgrading Without Rewrite)

Follow these steps to facilitate a controlled transition between Practice Levels without requiring a complete system overhaul.

1.  **Separate Form from Substrate:** Design and implement P2+ (Agent Mode and above) and federation features as **optional, modular components**. This allows a core kernel to remain P1-capable while extensions enable higher levels.
2.  **Declare Capability Flags:** Implement clear, discoverable **capability flags** within the system's metadata or configuration. Examples include:
    * `capability.memory`: `session` (P1), `durable` (P2+)
    * `capability.autonomy`: `none` (P1), `bounded` (P2), `orchestrated` (P3), `distributed` (P4)
    * `capability.multi_party`: `no` (P1/P2), `single_team` (P2/P3), `cross_org` (P4)
3.  **Promotion Checklist (Iterative Upgrade):** Introduce new capabilities one requirement at a time, ensuring each step is audited and validated before proceeding. This methodical approach minimizes unexpected behavioral changes and new risks.
    * **P1 → P2 Transition Steps:**
        * Introduce session persistence for user preferences.
        * Implement controlled auto-tuning mechanisms.
        * Add scheduled or background prompts (always with explicit consent gates).
        * Conduct **consent and transparency audits**.
    * **P2 → P3 Transition Steps:**
        * Implement shared workspace or ledger capabilities for multiple users/roles.
        * Develop formal mediation or coordination protocols.
        * Conduct **auditability and permissions audits**.
    * **P3 → P4 Transition Steps:**
        * Enable cross-organizational data exchange and state synchronization.
        * Implement federated policy enforcement mechanisms.
        * Establish and integrate with formal inter-organizational treaties for data lineage and governance.
        * Conduct **interoperability and policy portability audits**.

---

## Examples (Grounding for Implementation)

These examples illustrate how real-world systems map to the Practice Levels and can guide implementation decisions.

* **Custom GPT used by many people, each in siloed, unremembered sessions:** **P1**. Implementation ensures no user data persists or influences future sessions.
* **Single-user persistent application that remembers presets, offers proactive follow-ups (e.g., "Would you like to continue from where you left off?"), and learns basic preferences:** **P2**. Implementation includes user-specific databases, clear consent prompts for learning, and user-configurable limits on proactive behavior.
* **Team assistant coordinating tasks across multiple teammates with a shared task board, assigning actions, and logging progress for all to see:** **P3**. Implementation requires a shared database, explicit role-based access control, and immutable transaction logs for all assignments and completions.
* **Network of assistants exchanging sensitive project lineage and compliance data across different company departments or external partners under formal data sharing agreements:** **P4**. Implementation necessitates robust encryption, federated identity management, auditable policy engines, and contractually binding data governance frameworks.

---

## Versioning & Change Log
- **v1.0** — Initial release of the Implementation Guide; details on classification, compliance, and migration pathways extracted from the main `practice_levels` doctrine.
