---
id: potm.diagnostic.latency.v1_0
title: latency_diagnostic
display_title: "Latency Diagnostic"
type: diagnostic
status: stable
version: 1.0
stability: experimental
relations:
  supersedes: []
  superseded_by: []
tags: [diagnostic, latency, performance, kernel]
interfaces: [lens.latency_status, validator]
author: practitioner
license: CC0-1.0
---

# Latency Diagnostic

## Purpose
To **measure and profile execution time** of kernel components, protocols, and diagnostics in order to identify bottlenecks.  
This diagnostic supports enforcement of the **Latency Contract (85)** by revealing which subsystems exceed the service level objectives (SLOs).  

---

## When to Run
- After integrating new kernel/protocol code.  
- When observed latency approaches or exceeds SLO ceilings.  
- Periodically (e.g. once per release cycle) as part of extended self-diagnostic routines.  

---

## Inputs

  - Most recent `latency_breach` entry in `ledger_buffer`, including its `severity` field

---

## Conformance

This diagnostic result conforms to the shared schema:

`runtime/spec/diagnostic.result.v1.json`

All output objects must validate against that schema:
- `id`: `"latency_diagnostic"`  
- `mode`: current `latency_mode`  
- `summary`: short natural-language overview  
- `findings[]`: array of component-level observations with `status` and `severity`.

---

## Procedure
1. **Instrument** each major component (agreement, validator, fracture_finder, mirror, guardian, bs_detect).
2. **Record runtime** for each invocation in milliseconds/seconds, and query
   `lens.latency_status` to cross-check the current mode and most recent breach.
3. **Aggregate** timing data by:
   - p50 (median)  
   - p95 (worst-case ceiling)  
   - outliers (any run >2× SLO target).  
4. **Compare** against Latency Contract SLOs.  
5. **Classify** each component as:
   - ✅ within bounds,  
   - ⚠ borderline,  
   - ❌ violating.  
6. **Log results** into the extended diagnostics ledger.  

---

## Decision Rules
- If any ❌ component is core (agreement, validator) →

## Artifacts

- Extract from `lens.latency_status` showing mode, last breach, and its severity at time of run.

---

## Examples

### Example Run (2025-08-28)

**lens.latency_status**

```yaml
{
  "mode": "standard",
  "last_breach": {
    "ts": "2025-08-28T15:15:00Z",
    "observed_latency": 7.1,
    "ceiling": 6.0,
    "severity": "warning"
  }
}
````

**Component Timing Profile**

| Component          | Median (p50) | 95th (p95) | Contract Ceiling | Status                          |
| ------------------ | ------------ | ---------- | ---------------- | ------------------------------- |
| agreement.accepted | 0.01s        | 0.02s      | ≤ 6s             | ✅ within bounds                 |
| validator.stub     | 0.12s        | 0.20s      | ≤ 6s             | ✅ within bounds                 |
| fracture\_finder   | 1.5s         | 4.8s       | ≤ 6s             | ⚠ borderline (close to ceiling) |
| mirror\_protocol   | 2.1s         | 7.1s       | ≤ 6s             | ❌ breach (logged to ledger)     |
| guardian check     | 1.8s         | 3.5s       | ≤ 6s             | ✅ within bounds                 |


**Summary**

- **1 warning** (`fracture_finder` borderline at 4.8s).  
- **1 breach** (`mirror_protocol` exceeded 6s ceiling, logged with `severity:"warning"`).  
- Latency mode = `standard`.  
- Contract SLO (≤ 6s p95) violated once; router emitted `W_LATENCY_BREACH`.  
- Diagnostic classification derives from `severity` in `lens.latency_status` rather than recomputing rules.

---
