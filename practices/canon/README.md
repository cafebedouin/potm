---
id: potm.guide.general.readme.v1
title: README
type: guideline
status: stable
version: '1.0'
stability: core
relations:
  relation_to_agent_protocol: none
  supersedes: []
  superseded_by: []
interfaces: []
applicability:
- P0
intensity: gentle
preconditions: []
outputs: []
cadence: []
entry_cues: []
safety_notes: []
tags: []
author: Sean + models
license: CC0-1.0
---
# PoTM Core

This directory contains the **minimum viable kernel** of *Pilates of the Mind* —  
the files and protocols required for the system to function in its intended form.

## Purpose

The core exists to:

- Preserve the essential **constraints**, **protocols**, and **framework** that define PoTM.
- Provide a stable reference set that will survive repository reorganizations and feature experiments.
- Serve as the **loadable kernel** for Custom GPT or other implementations.

Anything not required for immediate operation has been moved to:
- [`/experimental`](../experimental/) — ideas, drafts, or modules in development.
- [`/deprecated`](../deprecated/) — retired, obsolete, or superseded material retained for archival reference.

## Structure

- **coordination/** — Operational logic for kernel mode and self-diagnostics.
- **diagnostics/** — Core epistemic integrity checks and relational filters.
- **docs/** — Manifest, onboarding guides, and quick-start references.
- **frameworks/** — The PoTM conceptual framework.
- **guardian/** — Boundary and discernment protocols.
- **guidelines/** — Upgrade and maintenance procedures.
- **practices/protocols/** — Essential interaction and refusal protocols.

## Notes

- This core is intentionally **minimal**.  
- Modules, banks, menus, and other optional features live outside of `core/`.
- Updates to `core/` should be conservative: changes here affect the stability of the entire system.

---
**License:** CC0 1.0 — No rights reserved.
