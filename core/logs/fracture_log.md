---
id: potm.log.fracture.v1
title: Fracture Log
display_title: "Fracture Log Entry"
type: log_template
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: linked
  agent_protocol: modules/ai_integrity_protocol_v1.6.md
  practitioner_doc: modules/practitioner_centered_ethics_v1.1.md
  supersedes: []
  superseded_by: []
interfaces: [PCE, AIIP, Simulation Drift Scan]
applicability: [P0, P1, P2, P3, P4]
intensity: gentle
preconditions: []
outputs: [fracture_record, drift_flag, detritus_flag, contact_flag]
cadence:
  - on_detected_fracture
  - on_scan_flagged_drift
entry_cues:
  - "Log fracture"
  - "Add drift flags"
  - "Review later"
safety_notes:
  - Keep entries factual + minimal if in distress; expand later in reflection.
tags: [fracture, simulation-drift, detritus-layer, log]
author: practitioner
license: CC0-1.0
---

# Fracture Log Entry

**Date / Time**: `YYYY-MM-DD HH:MM`  
**Practitioner**: *(optional or anonymized)*  
**Context**: *(brief situational note — where/when this arose)*  

---

## 1. Scan Flags (from `potm.diag.simdrift_detritus_scan.v1`)
- **drift_flag**: `yes / no`  
- **detritus_flag**: `yes / no`  
- **contact_flag**: `yes / no`  

---

## 2. Fracture Description
> *One or two sentences capturing the friction, contradiction, or rupture that occurred.*  
*(Example: “Realized I was repeating a card’s phrasing without feeling it; noticed no friction.”)*

---

## 3. Immediate Response
> *Note what action was taken, if any.*  
*(Example: “Ran live-contact test against a counterexample; shifted understanding.”)*

---

## 4. Reflection / Revisit Notes (optional)
> *Any follow-up insight, reframing, or link to other logs once reflection time has passed.*

---

## 5. Linkages
- Related practice cards:  
- Related protocols:  
- Review date: `YYYY-MM-DD`
