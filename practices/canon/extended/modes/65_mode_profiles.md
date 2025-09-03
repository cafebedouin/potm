---
id: potm.kernel.mode_profiles.v1_0
title: "65_mode_profiles"
display_title: "Mode Profiles — Operational Envelopes"
type: kernel
lifecycle: canon
version: 1.0.0
status: active
stability: core
summary: >-
  Defines Lite, Standard, and Strict operating profiles for the kernel.  
  Each profile tunes validator severity, latency ceilings, escalation gates,  
  and micro-canary sensitivity. Profiles are session-local, deterministic,  
  and settable via entry contract, manual override, or automatic escalation.
author: practitioner
license: CC0-1.0
---

# Mode Profiles — Operational Envelopes

## Purpose

Mode profiles establish *operational envelopes* that determine  
how strictly the kernel enforces its invariants.  

Profiles govern:

- Validator strictness (warn vs fail-closed)  
- Latency tolerance (ceilings, warnings, breach handling)  
- Escalation gate sensitivity  
- Micro-canary thresholds  

They enable flexibility without weakening invariants:  
operators can choose lighter onboarding or strict containment,  
while the kernel remains deterministic and fail-closed.

---

## Profile Definitions

### Lite
- **Use case:** onboarding, low friction, exploratory practice  
- **Validator:** warns first, then fails on repeat violation  
- **Latency:** shortest ceilings (p50=2s, p95=4s)  
- **Escalation:** softer thresholds; defer fracture logging if minor  
- **Canary:** low sensitivity (alerts only on repeated anomalies)  

### Standard
- **Use case:** default, balanced between integrity & usability  
- **Validator:** immediate fail-closed on schema or cap violation  
- **Latency:** medium ceilings (p50=4s, p95=6s)  
- **Escalation:** normal fracture gating  
- **Canary:** medium sensitivity  

### Strict
- **Use case:** full guardrails, high-stakes or adversarial contexts  
- **Validator:** immediate fail-closed; no warnings  
- **Latency:** longest ceilings (p50=8s, p95=12s)  
- **Escalation:** aggressive — trip early, containment first  
- **Canary:** high sensitivity; alerts on single anomaly  
- **Extra:** BS-Detect hook (see `protocols/ai_integrity_protocol.md`)  

---

## Switching Logic

Profiles can be changed in three ways:

1. **Contract handshake**  
   - Default is `standard` unless overridden by explicit adapter signal.  
   - Example: see `runtime/examples/state_set_latency_mode.json`

2. **Manual override (operator request)**  
   - Operator may switch profiles mid-session.  
   - Must respect invariants: only valid values {lite, standard, strict}.  
   - Example: see `runtime/examples/state_set_mode_profile.json`

3. **Automatic escalation**  
   - Escalation gates may force switch upward:  
     - Repeated latency breaches in lite → auto-escalate to standard.  
     - Severe beacon failure in standard → auto-escalate to strict.  
   - Downgrades must be manual only; no auto-relaxation.  

---

### Ledger Integration

All mode profile changes MUST be recorded in the ledger as `mode_profile_change` entries.  
- Schema: `runtime/spec/ledger.mode_profile_change.json`  
- Example: `runtime/examples/mode_profile_change_ledger.json`  


## Profile Effects — Mapping Table

| Component         | Lite                          | Standard                          | Strict                          |
|-------------------|-------------------------------|-----------------------------------|---------------------------------|
| Validator         | warn, then fail               | fail-closed immediately           | fail-closed immediately         |
| Latency ceilings  | p50=2s, p95=4s                | p50=4s, p95=6s                    | p50=8s, p95=12s                 |
| Escalation gates  | tolerant; defer minor         | balanced; log fractures normally  | aggressive; trip at first sign  |
| Micro-canary      | low sensitivity               | medium sensitivity                | high sensitivity                |
| Integrity hooks   | none                          | none                              | includes BS-Detect              |

---

## Failure Modes

| Condition                           | Emission                                     |
|------------------------------------|----------------------------------------------|
| Invalid profile (not in enum)       | `tool.error { code: "E_LATENCY_MODE" }`      |
| Mode drift (state vs handshake)     | `tool.error { code: "E_INVARIANT" }`         |
| Auto-relaxation attempt (strict→std)| Blocked; require manual override             |
| Stuck escalation (strict lock-in)   | Operator must issue manual downgrade         |

---

### Cross-Reference — Enforcement in State

Validation of `mode_profile` values is enforced in `70_state.md`.  

- Invalid profile (not in {lite, standard, strict}) → `E_MODE_PROFILE`  
- Drift between `mode_profile` and `latency_mode` → `E_INVARIANT`  

See **Failure Modes (errors)** in `70_state.md` for the canonical table.

---

## References

* Entry contract: `10_entry_gate.md`  
* Validators: `60_validator.md`, `85_latency_validator.md`  
* State locus: `70_state.md`  
* Policy caps: `90_policy.md`  
* Escalation hooks: `68_escalation_gates.md`, `67_micro_canary.md`  
* Integrity extension: `protocols/ai_integrity_protocol.md`

---

## Versioning & Change Log

* **1.0.0** — Initial spec. Introduces Lite/Standard/Strict profiles,  
  switching logic, mapping table, and escalation rules.
