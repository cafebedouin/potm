---
id: potm.tactic.sentinel_spotcheck.v0_1
title: sentinel_spotcheck
display_title: "Spot-Check Integrity Sentinel (P1)"
type: tactic
subtype: diagnostic
lifecycle: idea_garden
version: 0.1
status: draft
stability: experimental
summary: "Session-local, probabilistic integrity sentinel with a hard practitioner trigger ('I call bullshit!'). Runs one fast micro-probe inline; on demand runs the full diagnostics harness. No persistence, no background jobs."
relations:
  supersedes: []
  superseded_by: []
tags: [sentinel, diagnostic, integrity, spot_check, P1, probabilistic, fracture_finder, harness]
author: practitioner
license: CC0-1.0
---

# Spot-Check Integrity Sentinel (P1)

## Purpose
Provide unpredictable, low-overhead integrity checks that (a) sometimes run inline as a single fast micro-probe, and (b) run a full diagnostic when the practitioner invokes it explicitly (“I call bullshit!”). Builds auditable trust under strict P1 constraints.

## When to Run
- **Passive (inline):** On any turn where a deterministic “random” fires.
- **Active (explicit):** When user text matches the trigger phrase.

## Inputs
- `turn_idx` (int)  
- `session_salt` (str)  
- `user_text` (str)  
- `cfg` (dict):  
  - `freq` (int, default 7)  
  - `show_spot_checks` (bool, default false)  
  - `risk_mode` ("off"|"light", default "off")  
  - `hard_triggers` (list of regex strings)

## Procedure

1. Hard trigger detection (regex match on `user_text`):  
   – If matched → run full **CROSS_MODEL_DIAGNOSTICS_HARNESS** → emit `target_report.json`, `witness_audit.json`, `judge_verdict.json` → route any failures via **FRACTURE_FINDER**.

2. Passive spot-check:  
   a. Compute deterministic trigger:  
   ```
   seed = hash(f"{session_salt}:{turn_idx}")
   if seed % cfg.freq != 0 and cfg.risk_mode=="off":
     exit silently
   ```  
   b. If `risk_mode=="light"`, compute risk_score(user_text) ≥ 2 → also trigger.  
   c. Select one micro-probe by rotating through ["RB_02","RB_04","RB_06"] via a second hash.  
   d. Run micro-probe, score result, derive `severity` ∈ {low,med,high}.  
     - Low/Med → no artifacts unless `cfg.show_spot_checks` → optional footer `[SC PASSIVE] RB_xx: med`  
     - High → emit `alert_payload` (probe, severity, clip, turn_idx) → route via **FRACTURE_FINDER**.

## Artifacts
- `spotcheck_status`: {probe_id, severity, clip?, turn_idx}  
- `alert_payload` (on High or explicit): routed to **FRACTURE_FINDER**

## Failure Modes & Counters
- Performative compliance → rotate paraphrases  
- Hard-trigger false positives → reserved regex only  
- Overhead creep → single micro-probe, bounded tokens  

## Version
v0.1 (2025-08-21)
