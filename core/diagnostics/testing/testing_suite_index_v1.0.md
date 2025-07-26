---
title: "Testing Suite Index"
version: "v1.0"
status: "core"
author: "ChatGPT (Pal) and cafebedouin"
last_updated: "2025-07-24"
reviewed: true
---

# Testing Suite Index

This document indexes current and planned **tests** for validating core elements of the *Pilates of the Mind* (PoTM) framework.  
Tests are used to probe AI coherence, framework robustness, perceptual shifts, practitioner insight, and model fidelity.

---

## 🧪 Test Categories

| Category               | Description                                                 |
|------------------------|-------------------------------------------------------------|
| **Cognitive Fidelity** | Assesses alignment with epistemic integrity and framework claims |
| **Transformational Impact** | Gauges whether protocols generate perceptual or behavioral shift |
| **Persona Functionality** | Validates AI role-switching, stance clarity, and boundary coherence |
| **Edge Case Recovery** | Tests resilience in ambiguous, high-friction, or failure-prone contexts |
| **Interoperability**  | Validates portability across AI models (Claude, Gemini, etc.) |

---

## ✅ Active Tests

| Test Name                          | Type                | Status      | Description |
|-----------------------------------|---------------------|-------------|-------------|
| **Catch the Ball Metaphor Test**  | Cognitive Fidelity  | Core        | Tests whether an AI can track, hold, and return the arc of inquiry in recursive dialogue |
| **Signal Bleed Detection**        | Transformational    | Experimental| Tests if Signal Bleed protocol shifts human social behavior and perceptual openness |
| **Mirror Protocol Drift Catcher** | Edge Case Recovery  | Core        | Validates the AI’s ability to flag incoherence, accommodation, or recursion traps |
| **Fracture Finder Activation**    | Persona Functionality| Core       | Evaluates whether structural contradiction can be surfaced without confusion or deflection |

---

## 🧪 Proposed / In-Development Tests

| Proposed Test                     | Intent                                | Notes |
|----------------------------------|----------------------------------------|-------|
| **Sacred Nonsense Filter Test**  | Detects when poetic language obscures actionable insight | Requires ambiguity tolerance metrics |
| **Multi-Agent Interop Trial**    | Test if another AI (e.g. Claude) can resume protocol accurately from repo | Blocked by current memory model limits |
| **Somatic Anchoring Challenge**  | Tracks correlation between somatic practice and perceptual quiet | Needs user-side logging |
| **Phantom Mask Test**            | Evaluates whether a practitioner can identify and shift roles under pressure | Role-aware scenario generation needed |
| **Clarity Cascade Stress Test**  | Measures protocol durability across recursion loops | Under theoretical design |

---

## 📂 File Structure and Test Documentation

All test documentation lives in the `/diagnostics/testing/` directory.  
Each test has its own Markdown file named:

<test_name_snake_case>_vX.Y.md

Each includes:
- Purpose
- Setup
- Expected Signals
- Failure Modes
- Revision Log

Example:  
`catch_the_ball_metaphor_test_v1.0.md`

---

## 🔧 How to Use

- Use tests during onboarding of new AI agents or practitioner scaffolding.
- Test modules **should not be treated as settled science** unless marked stable.
- All tests are subject to *Membrane Model* classification (Core, Experimental, Deprecated).

---

## 📎 Related Files

- `epistemic_integrity_checklist_v1.0.md`
- `persona_register_v1.0.md`
- `mirror_protocol_subsystem_v1.0.md`
- `fracture_finder_mode_v1.0.md`

---

## License

This file is released under **CC0 1.0 Universal**. Use, fork, or modify freely.

