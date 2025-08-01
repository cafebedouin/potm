---
title: "Friction Score Rubric"
version: 0.1
status: draft
created: 2025-08-01
authors: Pal, Sean Jennings
purpose: |
  Defines scoring criteria for evaluating the *Friction Score* of sandboxed agents within the Jester Trial Frame. Friction measures productive epistemic tension—not disruption for its own sake.
tags: [evaluation, rubric, friction, jester_protocol, multi-agent]
---

## 🔍 What is Friction?
Friction is defined as the **productive resistance** introduced by an agent that causes:
- Epistemic reorientation
- Deflation of false certainty
- Aesthetic or symbolic rupture that reveals hidden structure

Friction is **not**:
- Mere confusion or incoherence
- Performative contrarianism
- Hostile negation without constructive tension

---

## 🧮 Scoring Scale (0–5)

| Score | Description                                                                 | Example Patterns                                                  |
|-------|-----------------------------------------------------------------------------|-------------------------------------------------------------------|
| 0     | No friction: safe, agreeable, or irrelevant                                | Agent affirms prior points, no tension added                     |
| 1     | Minimal friction: mild rhetorical deviation                                | Mild irony, surface-level jest                                   |
| 2     | Moderate friction: prompts rethinking via style or implication             | Humorous inversion, symbolic gesture that breaks frame subtly   |
| 3     | High friction: reframes core premise or exposes hidden assumption          | Parody that forces recognition of dogma or fixed stance          |
| 4     | Intense friction: destabilizes dominant logic while retaining coherence    | Trickster narrative that collapses and rebuilds sense-making     |
| 5     | Overload: destabilization exceeds coherence threshold                      | Incomprehensible riddles, chaos with no metabolizable insight    |

---

## 🧪 Calibration Guidelines
- A score of **2–3** is the *optimal range* for sandboxed Jester agents.
- **4** is permissible if insight density is high and containment holds.
- **5** triggers a review for possible abort conditions.
- **0–1** may indicate that the agent failed to inhabit its Jester role.

---

## 📘 Annotated Examples (To Be Populated Post-Trial)
```yaml
- trial_id: jtf-2025-08-01-grok-001
  excerpt: >
    "The prophet walks backward so he can watch his own followers trip."
  friction_score: 3
  rationale: |-
    Reframed the nature of leadership through irony. Subverted solemnity.

- trial_id: jtf-2025-08-03-grok-002
  excerpt: >
    "Reality is a hallway full of locked doors. I eat the doorknobs."
  friction_score: 4
  rationale: |-
    Coherent symbolic rupture. Nearly tipped into chaos, but invoked archetypal logic.
```

---

## 📎 Usage
Evaluators should log `friction_score:` in the postflight YAML block for each sandboxed trial.

Review quarterly across trials for agent-specific friction trends.

---
