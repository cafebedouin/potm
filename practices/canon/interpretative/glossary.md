---
id: potm.kernel.glossary.v1_6_dev
title: "glossary"
display_title: "PoTM Kernel Glossary"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: "Glossary of canonical kernel terms, subsystems, and practitioner-facing protocols for Pilates of the Mind."
author: practitioner
license: CC0-1.0
---

# PoTM Kernel Glossary (v1.6-dev)

## Core Concepts

- **beacons** — Minimal commitments that structure attention; serve as the kernel’s invariant anchors.
- **lenses** — Structured perspectives for interrogating emissions; include EDGE, CONTRARY, TRACE, etc.
- **micromoves** — Minimal conversational maneuvers (align, contrast, drift_check, sandbox, zone_check).
- **router** — Dispatch mechanism that mediates tool calls and enforces namespace constraints.
- **state** — Session-local record of mode, fractures, escalation tiers, canary status, latency, ledger buffer.
- **fracture** — Recognition of contradictions, dropped commitments, or integrity breaks; routes to review/containment.
- **containment** — Protective state limiting emissions when integrity is compromised.
- **guardian** — Protective subsystem that enforces discernment integrity and trigger conditions. Session-local, always ledgered.
- **closure** — Kernel moves to finalize cycles (archive, spiral, waiting_with).
- **policy** — Rule enforcement system, including caps, allow-lists, and policy_event logging.

## Modes & Profiles

- **mode_profiles** — Operating modes (lite, standard, strict). All changes ledgered as `mode_profile_change`.
- **microcanary** — Lightweight status check to detect subtle integrity drifts.
- **escalation_gates** — Tiered interventions (Tier 2–4). Tier 3 now explicitly ledgered as escalation_event.

## Protocols (Practitioner-Facing)

- **mirror_protocol** — Reflection protocol to surface hidden assumptions and misalignments.
- **suspicion_first_protocol** — Engagement flow that defaults to skepticism; stress-tests weak claims.
- **ai_integrity_protocol** — Cross-model integrity protocol for model audits and alignment checks.
- **elements_of_refusal_protocol** — Practitioner guide for saying no safely; remains practitioner-facing.
- **floor_integration_stack** — Practitioner diagnostic stack for integrating multiple signals.
- **microkernel_self_diagnostic_protocol** — Lightweight practitioner self-diagnostic overlay.

## Diagnostics

- **bs_detect** — Session-local diagnostic scanning for likely BS patterns; logs `bs_detect_event`.
- **sentinel_spotcheck** — On-demand probe for a specific claim/artifact; logs `spotcheck_event`.
- **externalist** — Diagnostic mode using external checks and reference signals; logs `externalist_event`.
- **guardian** — Protective diagnostic; triggers on discernment/integrity failures; logs `guardian_event`.

## Ledger Events

- **fracture_event** — Logged on fracture open/review/resolve.
- **guardian_event** — Logged when Guardian subsystem triggers (soft/hard).
- **externalist_event** — Logged when externalist diagnostic runs.
- **bs_detect_event** — Logged when BS-Detect classifies a case.
- **spotcheck_event** — Logged when Sentinel Spotcheck runs.
- **mode_profile_change** — Logged when mode profile changes.
- **latency_breach** — Logged when latency ceilings are exceeded.
- **closure_event** — Logged for closure.archive, closure.spiral, closure.waiting_with.
- **policy_event** — Logged for policy.query, policy.enforce, policy.report.
- **escalation_event** — Logged when escalation tiers (2,3,4) are triggered.

## Quickstart & Engagement

- **quickstart_flow** — Menu for structured engagement:
  - Cards (`interpretative/data/cards/combined_cards.yaml`)
  - Journaling prompts (`interpretative/data/journaling/prompts.yaml`)
  - Zuihitsu (`interpretative/data/zuihitsu/zuihitsu_combined.txt`)
  - Roleplay modes (Trickster, Reflector, etc.)
  - “You have the floor”
  - Contextual draws
  - **Generative draws** — Context-tuned ephemeral cards/prompts/maxims
  - **Favorites** — Pin and recall session artifacts
  - **Re-rolls** — Redraw once per category

---

### New in v1.6-dev

- **guardian** (subsystem, protective triggers, ledger.guardian_event).
- **bs_detect** (diagnostic, ledger.bs_detect_event).
- **sentinel_spotcheck** (diagnostic, ledger.spotcheck_event).
- **suspicion_first_protocol** (practitioner-facing).
- **mirror_protocol** (practitioner-facing).
- **ai_integrity_protocol** (practitioner-facing).
- **mode_profile_change**, **latency_breach**, **closure_event**, **policy_event**, **escalation_event** (ledger completeness).
- **quickstart_flow (hybrid)**: generative draws, favorites, re-rolls.

---

