---
id: potm.kernel.micro_canary.v1_0
title: "67_micro_canary"
display_title: "Micro-Canary — Early Anomaly Sensor"
type: kernel
lifecycle: canon
version: 1.0.0
status: active
stability: core
summary: >-
  Provides lightweight anomaly detection before hard invariants are breached.  
  The micro-canary emits soft warnings into the ledger, escalates only via  
  escalation gates, and tunes its sensitivity according to the active mode profile.
author: practitioner
license: CC0-1.0
---

# Micro-Canary — Early Anomaly Sensor

## Purpose

The micro-canary functions as an **early warning system**.  
Where validators enforce hard schema or cap failures, the canary watches for **softer anomalies**:  
unexpected patterns, near-misses, or repeated weak signals that often precede failure.

Its purpose is not to halt execution, but to *chirp early* and feed escalation gates with enough signal to prevent silent drift.

---

## Detection Categories

- **Schema near-miss**  
  Inputs structurally valid but suspicious (e.g. repeated optional fields missing).  

- **Unusual latency pattern**  
  Spikes that don’t breach hard caps but deviate significantly from baseline.  

- **Drift pattern**  
  Repeated small deviations that alone are benign but collectively concerning.  

- **Unknown/other**  
  Anomalies not covered but surfaced by external diagnostic lenses.

---

## Sensitivity (Profile-Tuned)

| Profile   | Sensitivity            | Chirp Threshold |
|-----------|------------------------|-----------------|
| Lite      | Low — alert only on repeated anomalies | 3 consecutive |
| Standard  | Medium — chirp on pattern deviation   | 2 consecutive |
| Strict    | High — chirp on single anomaly        | 1 event       |

Sensitivity is bound to `mode_profile` (see `65_mode_profiles.md`).  

---

## Outputs

- **Ledger entry** of type `canary_report` with fields:  
  - `signal`: enum {schema_near_miss, unusual_latency, drift_pattern, unknown}  
  - `severity`: {warning|error}  
  - `mode_profile`: profile active at time of detection  
  - `ts`: ISO-8601 timestamp  

- **Escalation gates** may consume canary outputs to trigger mode escalation or fracture creation.

---

## Switching Logic

- Canary emits only **soft warnings**; it never halts flow.  
- Escalation gates interpret frequency/severity.  
- Can be temporarily silenced by policy (`policy.cap.canary_squelch = true`).  

---

## Failure Modes

| Condition                     | Counter-measure                       |
|-------------------------------|---------------------------------------|
| False positives (noise)       | Squelch via policy cap; tune severity |
| Silent canary (no emission)   | Covered by structural audit protocol  |
| Overload (spam emissions)     | Gate by `policy.cap.ledger_max`       |

---

### Cross-Reference — Enforcement in State

Validation of `canary.report` payloads and errors is enforced in `70_state.md`.

- Invalid `signal` → `E_CANARY_SIGNAL`  
- Invalid `severity` → `E_CANARY_SEVERITY`  
- Missing required field → `E_PAYLOAD`  

See **Failure Modes (errors)** in `70_state.md` for the canonical table.

---

## References

* Profiles: `65_mode_profiles.md`  
* State locus: `70_state.md`  
* Escalation gates: `68_escalation_gates.md` (forthcoming)  
* Policy integration: `90_policy.md`  

---

## Versioning & Change Log

* **1.0.0** — Initial spec. Introduces anomaly categories, profile-tuned sensitivity, and ledger reporting.
