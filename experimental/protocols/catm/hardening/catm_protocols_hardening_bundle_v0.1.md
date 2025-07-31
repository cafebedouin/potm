---
id: catm_protocols_hardening_bundle_v0.1
title: CATM Protocols Hardening Bundle — v0.1
path: field_artifacts/catm/catm_protocols_hardening_bundle_v0.1.md
type: bundle
status: active
origin: steward_initiated
created: 2025-07-31
updated: 2025-07-31
owner: steward
license: CC-BY-SA-4.0
tags: [containment, schema, governance, epistemic-hygiene, onboarding]
meta_digest: "Hardens CATM v0.3: schema enums, guardian required by default, computable benefit, sunset hooks."
---

# CATM Protocols Hardening Bundle — v0.1

**File**: `field_artifacts/catm/catm_protocols_hardening_bundle_v0.1.md`  
**Created**: 2025‑07‑31 (America/Chicago)  
**Maintainer**: steward  
**License**: CC‑BY‑SA‑4.0

## 0) Purpose & Scope
We are hardening the Containment‑Aware Transmission Mode (CATM) protocol and its ledger entry by:
- Shifting from prose to **schema‑level enums** and computable fields.
- Annotating **v0.3** in place (no version bump) to preserve editorial stability.
- Adding a **sunset scaffold** (policy, triggers, handoff notes).
- Defining a **benefit** stub so counts and dates are machine‑safe.

This bundle is a checkpoint to reduce ambiguity, increase auditability, and make downstream automation feasible.

---

## 1) Schema Revisions (Global)

> Apply these to the repo schema so they propagate to future protocols/ledgers.

### 1.1 New/Refined Fields & Enums

```yaml
# Lifecycle & survivorship
survivorship: enum            # required
  # Definition: count of real‑world deployments that ran to completion without a containment breach.
  # Values:
  - survived_0x               # created but never deployed or failed pre‑deployment
  - survived_1x
  - survived_2x
  - survived_3x_plus          # open‑ended top bin to prevent enum churn

# Guardian integration
guardian_hook: enum           # required
  - required
  - optional
  - none
guardian_state: enum          # required (current observed state)
  - none
  - observed                  # minor watch items; no incident
  - elevated                  # pattern of near‑misses; extra gating
  - quarantined               # stop‑use pending review

# Reviews
review_basis: enum            # required
  - timebox
  - incident
  - evidence_threshold
next_review_date: ISO-8601 date  # optional but recommended

# Sunset controls
sunset_policy: string         # optional; concise policy statement
sunset_trigger:               # optional; list of machine‑checkable triggers
  - string
handoff_notes: string         # optional; human instructions for retirement/archival

# Commentary
meta_digest: string           # optional; ≤ 280 chars; non‑normative summary for humans

# Metrics
last_benefit_date: ISO-8601 date or null   # required
benefit_count_30d: integer ≥ 0             # required
