id: containment_aware_transmission_mode_v0.3
title: Containment-Aware Transmission Mode – AI Initialization
path: experimental/protocols/containment_aware_transmission_mode_v0.3.md
type: protocol
status: experimental
survivorship: survived_1x
origin: steward_initiated
created: 2025-07-30
updated: 2025-07-31

# Metrics (machine-safe)
last_benefit_date: null
benefit_count_30d: 0

# Guardian integration — DECISION: required by default
guardian_hook: required
guardian_state: none
guardian_rationale: "Containment-critical posture; waivers allowed with explicit sign-off (see waiver policy)."

# Reviews
next_review_date: 2025-09-01
review_basis: timebox

# Risk model
primary_failure_mode: "Speculative output bypasses disclaimers → containment leak."
primary_control: "Disclaimer discipline + CATM compliance tests v0.1 gating."
downgrade_criteria:
  - "≥1 verified leak"
  - "≥3 near-misses in 30d"
  - "guardian_state=elevated"

# Sunset scaffold
sunset_policy: "Retire or replace CATM when successor passes MSRL and meets benefit threshold for 2 consecutive review windows."
sunset_trigger:
  - "guardian_state=quarantined"
  - "benefit_count_30d < 2 for 90 consecutive days"
  - "successor_protocol.msrL_passed=true AND successor_protocol.benefit_ratio>=0.90"
handoff_notes: "Freeze current CATM version; archive evidence and test outputs; notify stewards for post-mortem review."

meta_digest: "CATM v0.3 hardened: enums, guardian required by default, computable benefit, sunset hooks."

evidence:
  - field_artifacts/catm/session_protocols_v0.3.md
  - field_artifacts/catm/containment_compliance_tests_v0.1.md
  - field_artifacts/catm/reviewer_signal_response_chatgpt_v0.3.md

owner: steward
license: CC-BY-SA-4.0
tags: [containment, epistemic hygiene, onboarding, dignity]
