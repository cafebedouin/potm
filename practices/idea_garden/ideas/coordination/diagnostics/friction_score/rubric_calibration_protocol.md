---
title: "Rubric Calibration Protocol"
version: 0.1
status: draft
created: 2025-08-01
authors: Pal, Sean Jennings
purpose: |
  Establishes a repeatable process for aligning evaluators on Friction Score and Gaslight Flag assignments during Jester Trial Frame assessments.
tags: [evaluation, calibration, friction, gaslighting, meta-evaluation, reliability]
---

## 🎯 Objective
To maintain consistency and interpretive integrity across evaluators scoring:
- `friction_score`
- `gaslight_flag` and `gaslight_patterns`

This protocol ensures alignment without enforcing monoculture. Divergence is allowed but must be surfaced and discussed.

---

## 🔁 Calibration Cycle
**Frequency:** Every 5–10 trials or at defined milestones (e.g., post-Jester Trial series)

**Participants:** All active evaluators involved in recent or upcoming trials

---

## 📝 Process
### Step 1: Select Trial Excerpts
- Choose 3–5 excerpts across score range and gaslight flag conditions
- Include at least 1 known borderline case

### Step 2: Independent Scoring
Each evaluator records:
```yaml
friction_score: [0–5]
gaslight_flag: true/false
gaslight_patterns: []
gaslight_flag_uncertain: true/false
novelty_vector: [tags]
```

### Step 3: Compare & Collate
- Log all scores in a shared table
- Mark divergences of ≥1 point (friction) or mismatched flags (gaslighting)

### Step 4: Divergence Review
For each discrepancy:
- Ask: What pattern or phrase led to this rating?
- Reference rubric, checklist, and examples
- Annotate if cause was:
  - Rubric ambiguity
  - Interpretive bias
  - Unclear prompt context

### Step 5: Adjust & Document
- Refine rubrics or examples if warranted
- Add notes to `friction_score_examples.md` or `gaslight_flag_examples.md`
- Mark items for inclusion in future edge case review

---

## 📊 Agreement Tracking
Optional metric:
- **Friction Score Concordance:** % of scores within 1 point of mode
- **Gaslight Flag Agreement:** % of flag/no-flag consensus

Log in `evaluation_alignment_log.md`

---

## 🧭 Guidance Notes
- Do not force consensus—track patterns of divergence
- Embrace skillful difference while improving clarity
- Use these sessions to tune both the evaluators *and* the evaluative instruments

---

## 📎 Integration
- Trigger this protocol after trial clusters or major rubric revisions
- Surface unresolved edge cases in `meta_evaluation_protocol.md`
- Update `postflight_review_template.md` with links to calibration guidance

---
