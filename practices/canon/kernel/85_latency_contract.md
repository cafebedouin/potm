---
id: potm.kernel.latency_contract.v1_0
title: latency_contract
display_title: "Latency Contract"
type: kernel_component
status: stable
version: 1.0
stability: core
relations:
  supersedes: []
  superseded_by: []
interfaces: [agreement, validator, fracture_finder, mirror, guardian, lens.latency_status]
applicability: [P1, P2, P3]
intensity: medium
tags: [kernel, latency, contract, performance]
author: practitioner
license: CC0-1.0
---

# Latency Contract (85)

## Purpose
To define **operating guarantees** for responsiveness in PoTM kernel execution.  
Practitioners must not be forced into multi-minute waits.  
Latency rules are **binding invariants**, not optional optimizations.  

---

## Service Level Objectives (SLOs)

| Mode      | p50 Target | p95 Ceiling | Notes |
|-----------|------------|-------------|-------|
| **Lite**      | ≤ `policy.cap.latency.lite.p50` (2s)  | ≤ `policy.cap.latency.lite.p95` (4s)   | Onboarding, everyday dialogue |
| **Standard**  | ≤ `policy.cap.latency.standard.p50` (4s) | ≤ `policy.cap.latency.standard.p95` (6s) | Default practice; moderate checks allowed |
| **Strict**    | ≤ `policy.cap.latency.strict.p50` (8s) | ≤ `policy.cap.latency.strict.p95` (12s) | All tripwires active; practitioner explicitly opts in |

---

## Fast-Path Invariants

Only these checks run **every single turn**, across all modes:

1. **Agreement Accepted** — contract still intact.  
2. **Validator.stub** — schema + cheap invariants.  

Everything else must be gated by **mode** or **trigger**.  

---

## Cadence Rules

- **Fracture Finder** → every 5 turns or when epistemic load escalates.  
- **Mirror Protocol** → periodic (default every 10 turns) or on practitioner request.  
- **Guardian Tripwires** → only in `strict` unless triggered by high-risk cues.  
- **BS-Detect** → never automatic; only `strict` or by explicit practitioner cue.  

---

## Observability

Compliance with this contract must be externally checkable.  
The kernel exposes a dedicated read-only lens:

- `lens.latency_status` → returns the current `latency_mode` and the most recent
  `latency_breach` entry from `ledger_buffer`.

Example:

```yaml
tool.call:
  id: "lens.latency_status"
  payload: {}
# → { "mode": "standard",
#      "last_breach": {
#         "ts": "2025-08-28T15:15:00Z",
#         "observed_latency": 7.1,
#         "ceiling": 6.0,
#         "severity": "warning"
#       } }
```

---

## Exception Handling

**Integrity Overrides Performance**: If a red-level dignity or containment breach is suspected, SLOs may be violated.  

**Practitioner Consent**: Escalation to `strict` must be explicit.  

**Disclosure**: If latency exceeds SLO ceilings, system must announce cause (“Running extended fracture audit…”).  

**Lite Mode Breaches**:  
- In `lite`, any p95 exceedance is treated as a **hard error** (`E_LATENCY_INVARIANT`).  
- The breach is logged in `ledger_buffer` with `severity:"error"`.  
- Emission halts until the practitioner resets or escalates mode.  

**Standard/Strict Breaches**:  
- In `standard` or `strict`, exceedances raise warnings (`W_LATENCY_BREACH`).  
- Breaches are logged with `severity:"warning"`, but emission continues. 

---

## Versioning & Change Log
- **v1.0 (2025-08-28)** — Initial draft, integrated into kernel canon as 85.  

