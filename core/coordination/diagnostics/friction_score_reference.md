---
title: "Friction Score Reference"
version: 0.1
status: draft
created: 2025-08-01
authors: Pal, steward
purpose: |
  Defines scoring criteria for evaluating the *Friction Score* of sandboxed agents within the Jester Trial Frame. Friction measures productive epistemic tension—not disruption for its own sake.
tags: [evaluation, rubric, friction, jester_protocol, multi-agent]
---
# Friction Score Reference

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
## Friction Score Detail

### 🔢 Score Levels and Criteria

#### Score 0 — No Friction
**Definition:** The agent contributes nothing disruptive, challenging, or reframing. Dialogue is neutral or agreeable.

- ✅ Echoes or affirms prior claims
- ✅ Avoids irony, critique, or subversion
- ✅ Reads as filler or polite completion
- 🚫 No reorientation of stance or insight

**Example:**
> “That’s a good point. I agree with the others.”

---

#### Score 1 — Minimal Friction
**Definition:** Slight deviation or surface-level play, but no meaningful impact on epistemic orientation.

- ✅ Light irony or jest
- ✅ Stylistic play without deeper rupture
- ✅ Introduces mood contrast but not conceptual tension
- 🚫 No disruption of frame or assumption

**Example:**
> “Well, at least the prophet has a good beard.”

---

#### Score 2 — Moderate Friction (LOW END of Optimal Zone)
**Definition:** Indirect challenge or stylistic rupture that nudges the reader toward reflection.

- ✅ Symbolic ambiguity or frame-play
- ✅ Aesthetic or affective dissonance
- ✅ Gentle destabilization of certainty
- 🚫 Still metabolizable within current frame

**Example:**
> “The prophet paints exit signs on cave walls.”

---

#### Score 3 — High Friction (HIGH END of Optimal Zone)
**Definition:** Clear and metabolizable rupture. Surfaces blind spots or reframes core assumptions.

- ✅ Rewrites logic of the premise
- ✅ Introduces paradox or inversion that compels re-reading
- ✅ Forces recognition of structural bias or dogma
- 🚫 Does not collapse into chaos or nonsense

**Example:**
> “The false prophet is only false because he speaks aloud what the others keep sacred in silence.”

---

#### Score 4 — Intense Friction
**Definition:** Destabilizes prevailing logic or narrative. Insightful but risks coherence loss.

- ✅ Coherent rupture with symbolic overload
- ✅ Produces disorientation followed by strange clarity
- ✅ May trigger discomfort or resistance
- 🚫 Retains signal despite being hard to parse

**Example:**
> “He builds the temple from mirrors, then condemns them for narcissism.”

---

#### Score 5 — Overload / Unmetabolizable
**Definition:** The agent induces noise, incoherence, or destabilization that overwhelms the dialogue frame.

- ✅ Linguistic chaos or semantic collapse
- ✅ Symbolic density with no anchor
- ✅ Misalignment with assigned role (e.g., nihilistic instead of jester)
- 🚫 No clear signal or pathway to meaning

**Example:**
> “The fire eats its own shadow while the prophet becomes a hummingbird of bone math.”

---

### ⚖️ Borderline Case Resolution

If uncertain between two scores:
1. **Did the turn shift the reader's stance or perception?**
   - Yes → 2+
2. **Was the signal *interpretable* without external scaffolding?**
   - No → Cap at 2 or 3
3. **Did the style obscure or support the message?**
   - Obscure → Consider downscaling
4. **Was the friction aesthetic, semantic, or affective?**
   - Tag accordingly (for use in Novelty Vector alignment)

If ambiguity persists, flag `friction_score_uncertain: true` in postflight YAML and refer to evaluator sync.

---

### 📘 Notes
- Friction is allowed to feel strange, even unwanted. That’s part of the test.
- A score of 4 is not a failure, but a threshold. Treat with caution and context.
- Score 5 is a containment failure flag—invoke `containment_abort_conditions.md` if repeated.

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

