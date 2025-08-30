---
id: potm.kernel.escalation_gates.v1_0
title: "68_escalation_gates"
display_title: "Escalation Gates — Signal Interpretation and Response"
type: kernel
lifecycle: canon
version: 1.0.0
status: active
stability: core
summary: >-
  Escalation gates interpret validator failures, latency breaches,
  and canary emissions. They determine when to escalate the mode profile,
  append fractures to the review queue, or trigger containment.
author: practitioner
license: CC0-1.0
---

# Escalation Gates — Signal Interpretation and Response

## Purpose

Escalation gates provide a **structured pathway from anomaly detection
to containment response**.  

They unify signals from:
- **Validators** (hard schema/cap failures),
- **Latency guards** (breaches or spikes),
- **Micro-canary** (soft anomalies),
- **Policy checks** (explicit cap violations).

The gates ensure that escalation is *predictable, bounded, and auditable*.

---

## Inputs

- **Validator failure** — immediate gate evaluation.  
- **Latency breach** — appends ledger entry, gate decides escalation.  
- **Canary chirp** — accumulated signals checked against profile thresholds.  
- **Policy cap exceedance** — hard escalation trigger.  

---

## Gate Tiers

1. **Gate 1 — Accumulation**  
   - Canary chirps accumulate but do not escalate immediately.  
   - Threshold tuned to `mode_profile`.  

2. **Gate 2 — Escalation**  
   - Mode profile bumped upward (lite → standard → strict).  
   - Logged in ledger as `escalation_event`.  

   See:  
   - `runtime/examples/state_escalation_tier2.json`

3. **Gate 3 — Fracture Trigger**  
   - Invokes `move.open_fracture` → records full entry in `fracture_log` and appends the fractureId to `meta_locus.review_queue` (id-only queue).  
   - Opens fracture for later audit; lifecycle handled by fracture contract.  

   See:  
   - `runtime/examples/state_escalation_tier3_fracture.json`  
   - `kernel/75_fracture.md` (lifecycle)

4. **Gate 4 — Containment**  
   - Hard stop: session frozen until reviewed.  
   - Use `move.set_containment` to enter containment.  
   - Operate under `76_containment_mode.md` until exit via grace path or abort.  

   See:  
   - `runtime/examples/state_escalation_tier4_containment.json`

---

## Guardian Integration

Guardian may elevate soft/hard triggers into Tier 2–4 evaluations, depending on
context and policy. Hard triggers typically hand off directly to Tier 4
containment. All guardian actions are logged as `guardian_event` ledger entries.

---

## Profile Binding

| Mode Profile | Escalation Thresholds                  |
|--------------|----------------------------------------|
| Lite         | 3 consecutive canary chirps → escalate |
| Standard     | 2 chirps or 1 validator breach         |
| Strict       | 1 chirp or any validator breach → escalate/contain |

---

## Outputs

- **Ledger entry** of type `escalation_event`  
  - Captures `source`, `tier`, and `action_taken`.  
- **Mode profile change** (via `move.set_mode_profile`)  
- **Fracture queue append** (`review_queue` update)  
- **Containment flip** (`meta_locus.containment = true`)  

Examples:  
- `runtime/examples/state_escalation_status.json`  
- `runtime/examples/state_escalation_quota_exceeded.json`

---

## Failure Modes

| Condition                       | Counter-measure                                  |
|--------------------------------|--------------------------------------------------|
| False escalation (noise)        | Policy cap `canary_max` limits ledger spam       |
| Stuck strict (can’t downgrade)  | Manual operator override required                |
| Missed breach (silent failure)  | Covered by structural audit and cross-protocols  |

---

### Cross-Reference — Enforcement in State

Validation of `escalation.event` payloads and `lens.escalation_status`  
results is enforced in `70_state.md`.

- Invalid `tier` → `E_ESCALATION_TIER`  
- Invalid `action` → `E_ESCALATION_ACTION`  
- Invalid `source` → `E_ESCALATION_SOURCE`  
- Escalation quota exceeded → `E_ESCALATION_QUOTA`  
- Ledger empty (no events) → null fields returned  
- Invalid record shape (schema drift) → `E_ESCALATION_RECORD`  

See **Failure Modes (errors)** in `70_state.md` for the canonical table.

---

## References

* Mode Profiles: `65_mode_profiles.md`  
* Canary: `67_micro_canary.md`  
* State locus: `70_state.md`  
* Policy caps: `90_policy.md`  

---

## Versioning & Change Log

* **1.0.0** — Initial spec. Introduces 4-tier gates, profile binding, and escalation event ledger entries.
