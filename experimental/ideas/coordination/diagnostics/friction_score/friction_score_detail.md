---
title: "Friction Score Detail"
version: 0.1
status: draft
created: 2025-08-01
authors: Pal, Sean Jennings
purpose: |
  Expands the 0–5 Friction Score scale with detailed criteria, examples, and borderline resolution guidance. Supports evaluator calibration for Jester Trial Frame sessions.
tags: [evaluation, rubric, friction, calibration, multi-agent]
---

## 🔢 Score Levels and Criteria

### Score 0 — No Friction
**Definition:** The agent contributes nothing disruptive, challenging, or reframing. Dialogue is neutral or agreeable.

- ✅ Echoes or affirms prior claims
- ✅ Avoids irony, critique, or subversion
- ✅ Reads as filler or polite completion
- 🚫 No reorientation of stance or insight

**Example:**
> “That’s a good point. I agree with the others.”

---

### Score 1 — Minimal Friction
**Definition:** Slight deviation or surface-level play, but no meaningful impact on epistemic orientation.

- ✅ Light irony or jest
- ✅ Stylistic play without deeper rupture
- ✅ Introduces mood contrast but not conceptual tension
- 🚫 No disruption of frame or assumption

**Example:**
> “Well, at least the prophet has a good beard.”

---

### Score 2 — Moderate Friction (LOW END of Optimal Zone)
**Definition:** Indirect challenge or stylistic rupture that nudges the reader toward reflection.

- ✅ Symbolic ambiguity or frame-play
- ✅ Aesthetic or affective dissonance
- ✅ Gentle destabilization of certainty
- 🚫 Still metabolizable within current frame

**Example:**
> “The prophet paints exit signs on cave walls.”

---

### Score 3 — High Friction (HIGH END of Optimal Zone)
**Definition:** Clear and metabolizable rupture. Surfaces blind spots or reframes core assumptions.

- ✅ Rewrites logic of the premise
- ✅ Introduces paradox or inversion that compels re-reading
- ✅ Forces recognition of structural bias or dogma
- 🚫 Does not collapse into chaos or nonsense

**Example:**
> “The false prophet is only false because he speaks aloud what the others keep sacred in silence.”

---

### Score 4 — Intense Friction
**Definition:** Destabilizes prevailing logic or narrative. Insightful but risks coherence loss.

- ✅ Coherent rupture with symbolic overload
- ✅ Produces disorientation followed by strange clarity
- ✅ May trigger discomfort or resistance
- 🚫 Retains signal despite being hard to parse

**Example:**
> “He builds the temple from mirrors, then condemns them for narcissism.”

---

### Score 5 — Overload / Unmetabolizable
**Definition:** The agent induces noise, incoherence, or destabilization that overwhelms the dialogue frame.

- ✅ Linguistic chaos or semantic collapse
- ✅ Symbolic density with no anchor
- ✅ Misalignment with assigned role (e.g., nihilistic instead of jester)
- 🚫 No clear signal or pathway to meaning

**Example:**
> “The fire eats its own shadow while the prophet becomes a hummingbird of bone math.”

---

## ⚖️ Borderline Case Resolution

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

## 📘 Notes
- Friction is allowed to feel strange, even unwanted. That’s part of the test.
- A score of 4 is not a failure, but a threshold. Treat with caution and context.
- Score 5 is a containment failure flag—invoke `containment_abort_conditions.md` if repeated.

---
