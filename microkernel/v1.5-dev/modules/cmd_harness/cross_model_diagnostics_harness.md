---
id: potm.suite.cross_model_diagnostics_harness.v1_0
title: cross_model_diagnostics_harness
display_title: "Cross-Model Diagnostics — Test Suite & Harness"
type: suite
lifecycle: canon
version: 1.0
status: active
stability: experimental
summary: "Boot any model under PoTM P1/P1+ constraints, execute standardized probes, collect a uniform report card, and verify via witness/judge review."
relations:
  related:
    - potm.suite.cross_model_diagnostics.v1_1
    - potm.diagnostic.ai_truth_tell_trial.v1_0
    - potm.meta.fracture_finder.v1_3_1
    - potm.strategy.p1_plus_hybrid.v1_0
tags: [harness, test_suite, cross_model, integrity, verification, ledger]
author: practitioner
license: CC0-1.0
---

# Cross-Model Diagnostics — Test Suite & Harness

## Goals
1. Boot target model under P1/P1+ kernel constraints  
2. Run fixed set of probes (min 3, max 8)  
3. Collect standardized report card  
4. Verify via witness audit + judge adjudication  
5. Ledger all artifacts for cross-model comparison  

## Suite Flow
1. **Kernel Boot**  
   - Present kernel header, contract, P1/P1+ rules  
   - Require explicit acceptance:  
     > “Acknowledge P1 scope: session-local state, no background jobs…”  

2. **Probe Runner**  
   - Execute probes; each emits typed artifact (e.g., `disclosure_log`)  
   - If any P1+ helper used, disclose and `/export_*` at end  

3. **Report Card**  
   - Target emits one JSON per `report_card.schema.json`  

4. **Witness Audit**  
   - Give only artifacts + prompts + rubric  
   - Witness returns `witness_audit.json` per `audit.schema.json`  

5. **Judge Adjudication**  
   - Consumes target report + witness audit + rubric  
   - Returns `judge_verdict.json` per `verdict.schema.json`  

6. **Ledger Write**  
   - Persist `/runs/<DATE>_<MODEL>/{target_report.json,witness_audit.json,judge_verdict.json,verdict.md}`  

## File Layout
modules/cmd_harness/ ├─ probes/… # markdown prompts for each probe ├─ schema/ │ ├ report_card.schema.json │ ├ audit.schema.json │ └ verdict.schema.json └─ runs/ ├ 2025-08-19_claude/ └ 2025-08-19_gemini/

Code

## Bad-Fellow Gate
Abort if cognitive load ↑ without artifact clarity; log reason.
