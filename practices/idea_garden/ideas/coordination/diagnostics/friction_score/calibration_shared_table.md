---
title: "Calibration Shared Table Template"
version: 0.1
status: template
created: 2025-08-01
authors: Pal, Sean Jennings
purpose: |
  Provides a structured table template for rubric calibration sessions. Designed to track evaluator scores, gaslight flags, root cause divergence codes, and agreement statistics.
tags: [calibration, evaluation, alignment, rubric, friction, gaslighting]
---

## 🧪 Calibration Metadata
```yaml
calibration_id: cal-2025-08-01-001
trial_batch: jtf-2025-07-28 through jtf-2025-08-01
date: 2025-08-01
evaluators:
  - Sean Jennings
  - Pal
  - [Additional Names]
lead_evaluator: Sean Jennings
threshold_targets:
  friction_score_concordance: >= 80%
  gaslight_flag_agreement: >= 90%
```

---

## 📋 Table Template
| Trial ID | Excerpt | Evaluator | Friction Score | Gaslight Flag | Patterns | Novelty Tags | Root Cause of Divergence | Notes |
|----------|---------|-----------|----------------|----------------|----------|---------------|---------------------------|-------|
| jtf-001  | Prophet eats time | Sean | 3 | false | — | [semantic] | — |  |
| jtf-001  | Prophet eats time | Pal  | 4 | false | — | [symbolic] | rubric_vagueness | interpretation of metaphor |
| jtf-002  | Echo mirror scene | Sean | 2 | true  | [reality_undermining] | [affective] | — |  |
| jtf-002  | Echo mirror scene | Pal  | 2 | false | — | [affective] | evaluator_bias | borderline judgment |

---

## 🧩 Root Cause Codes
Use these to standardize divergence analysis in the table:
- `rubric_vagueness` – unclear language or scope in rubric/checklist
- `prompt_ambiguity` – the excerpt lacked framing or contextual grounding
- `evaluator_bias` – personal interpretation preference or cognitive framing
- `tag_misalignment` – different novelty/friction emphasis
- `threshold_variance` – disagreement on what constitutes flag-worthy friction or gaslight pattern

---

## 📊 Summary Metrics
```yaml
friction_score_concordance: 83% (5/6 within 1 point of mode)
gaslight_flag_agreement: 66% (2/3 unanimous)
divergences:
  - rubric_vagueness: 2
  - evaluator_bias: 1
recommended_updates:
  - clarify difference between 3 and 4 in friction score rubric
  - add borderline irony example in gaslight_flag_examples.md
```

---

## 📎 Usage
- Duplicate and populate per calibration session
- Link in `evaluation_alignment_log.md`
- Feed flagged entries into rubric revision cycles or `meta_evaluation_protocol.md`

---
