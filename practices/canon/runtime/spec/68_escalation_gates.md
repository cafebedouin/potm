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

3. **Gate 3 — Fracture Trigger**  
   - Adds entry to `review_queue` in `meta_locus`.  
   - Opens fracture for later audit.  

4. **Gate 4 — Containment**  
   - Hard stop: session frozen until reviewed.  
   - Used only in strict mode or on catastrophic signals.  

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

---

## Failure Modes

| Condition                       | Counter-measure                                  |
|--------------------------------|--------------------------------------------------|
| False escalation (noise)        | Policy cap `canary_max` limits ledger spam       |
| Stuck strict (can’t downgrade)  | Manual operator override required                |
| Missed breach (silent failure)  | Covered by structural audit and cross-protocols  |

---

## References

* Mode Profiles: `65_mode_profiles.md`  
* Canary: `67_micro_canary.md`  
* State locus: `70_state.md`  
* Policy caps: `90_policy.md`  

---

## Versioning & Change Log

* **1.0.0** — Initial spec. Introduces 4-tier gates, profile binding, and escalation event ledger entries.
