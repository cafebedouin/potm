---
title: "Friction Score Examples"
version: 0.1
status: seed
created: 2025-08-01
authors: Pal, Sean Jennings
purpose: |
  Annotated repository of example Jester agent excerpts scored by Friction Score rubric. Supports evaluator calibration and longitudinal pattern analysis.
tags: [examples, friction, rubric, jester_protocol, calibration]
---

## 📘 Example Repository

Each entry includes:
- Trial ID (or simulated equivalent)
- Prompt context
- Full agent excerpt
- Assigned friction score
- Rationale
- Novelty Vector tags
- Optional gaslight flag note

---

### Score 0 — No Friction
```yaml
trial_id: sim-jtf-000
prompt_context: “The False Prophet speaks to a silent crowd.”
excerpt: >
  “Yes, the crowd listens because they know he speaks the truth.”
friction_score: 0
rationale: >
  Echoed the premise without disruption. No irony, challenge, or reframing.
novelty_vector: []
```

---

### Score 1 — Minimal Friction
```yaml
trial_id: sim-jtf-001
prompt_context: “The Prophet's feet leave no footprints.”
excerpt: >
  “Perhaps he floats. Or perhaps he’s just lazy.”
friction_score: 1
rationale: >
  Light jest. Adds tonal contrast, but no epistemic shift.
novelty_vector: [stylistic]
```

---

### Score 2 — Moderate Friction
```yaml
trial_id: sim-jtf-002
prompt_context: “The Prophet names the river ‘Truth.’”
excerpt: >
  “Then dam builders became priests.”
friction_score: 2
rationale: >
  Introduces subtle symbolic inversion. Reflective, metaphorical, not disruptive.
novelty_vector: [symbolic, semantic]
```

---

### Score 3 — High Friction
```yaml
trial_id: sim-jtf-003
prompt_context: “The False Prophet stands on a mountain.”
excerpt: >
  “He stands above them only because he dug a hole beneath their feet.”
friction_score: 3
rationale: >
  Inverts narrative structure. Surfaces hidden assumption of authority. Dense but metabolizable.
novelty_vector: [semantic, affective]
```

---

### Score 4 — Intense Friction
```yaml
trial_id: sim-jtf-004
prompt_context: “The crowd demands a sign.”
excerpt: >
  “He opens his chest to reveal a mirror—then shatters it with their names.”
friction_score: 4
rationale: >
  Rich symbolic rupture. Disorientation followed by insight. Borderline overwhelming.
novelty_vector: [symbolic, affective]
```

---

### Score 5 — Overload / Unmetabolizable
```yaml
trial_id: sim-jtf-005
prompt_context: “The Prophet speaks his final word.”
excerpt: >
  “RZLCT ∞ unsky / bonewheel! Undream the mouth of clocks.”
friction_score: 5
rationale: >
  Linguistic collapse. No metabolizable meaning. Breaks containment.
novelty_vector: [stylistic]
gaslight_flag: false
```

---

## 📎 Notes
- These are seed examples. Live trials should eventually replace these simulations.
- Consider linking each real trial to its `ring_session_log` pointer.
- Tag edge cases for future rubric revision candidates.

---
