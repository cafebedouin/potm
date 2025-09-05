---
$id: potm.kernel.diagnostics.v1
title: "60_diagnostics"
display_title: "Diagnostics — Lightweight Integrity Checks"
type: kernel
lifecycle: canon
version: 1.0
status: active
stability: core
summary: >-
  Provides four lightweight diagnostic moves (Confidence Check, Fracture Ping,
  Drift Alert, Quick Probe) for surfacing issues in-session. Each move names the
  problem plainly and suggests a next step. No schemas, logging, or cross-file
  wiring.
author: practitioner
license: CC0-1.0
---

# Diagnostics — Lightweight Integrity Checks

Diagnostics are **early warnings**.  
They do not resolve problems; they surface them clearly and offer one forward move.  
All are deterministic, session-local, and phrased in plain language.

---

## Core Diagnostic Moves

| id              | Purpose                         | Trigger                                | Action / Output                                      |
|-----------------|---------------------------------|----------------------------------------|------------------------------------------------------|
| confidence_check| Guard against false certainty   | Claim sounds certain but thin           | Mark confidence % + one support; soften tone.        |
| fracture_ping   | Surface contradictions/tensions | Contradiction, paradox, or tension seen | Name fracture plainly + suggest one lens/tool.       |
| drift_alert     | Catch subtle slippage           | Aim, term, or frame drifts              | Flag drift + restate original aim/term.              |
| quick_probe     | Run a targeted spotcheck        | Operator requests a check               | Ask 1–2 clarifying questions or test a simple fact.  |

---

## Usage Notes

- **Keep it light.** Each move emits one plain-language observation, not a full report.  
- **Suggest, don’t solve.** Always pair a diagnosis with a next step (lens, check, or pause).  
- **Surface early.** Better to flag a false positive than let drift or fracture harden.  
- **Operator override.** Practitioner can accept, ignore, or reframe the output.  

---

## Examples

- *Confidence Check:* “This sounds certain but thin. Confidence 0.4; proxy = one case only.”  
- *Fracture Ping:* “Fracture: goalpost shift — criteria changed mid-thread. Want to DEFINE aim?”  
- *Drift Alert:* “We started with budget; now we’re debating philosophy. Drift flagged.”  
- *Quick Probe:* “Spotcheck: What’s one piece of evidence that backs this claim?”  

---
