# User Modeling Layer

Recap: Defines dynamic, principled user adaptation for PoTM system behavior based on interaction patterns—not identities.

---

## Purpose

The User Modeling Layer introduces a modular, non-invasive system for adaptive calibration of PoTM responses based on **observed epistemic behavior**. It avoids anthropomorphic or personality-based profiling, focusing instead on how users engage with the system (e.g., style, stance, pace, friction-seeking).

Adaptivity is **subordinate** to all kernel-mode constraints and **explicit user tags**. This layer is designed to enhance responsiveness without compromising epistemic integrity, user sovereignty, or auditability.

---

## Components

| File | Description |
|------|-------------|
| `10_profile_types.md` | Defines six archetypal interaction profiles (P0–P5) as dynamic, observable epistemic stances |
| `20_profile_detection_logic.md` | Quantifies detection rules for each profile based on behavioral triggers and confidence scoring |
| `30_adaptive_response_matrix.md` | Maps each profile to system behaviors (tone, latency, abstraction, refusal posture, etc.) |
| `40_profile_shift_conditions.md` | Specifies logic for when and how profile shifts occur over time |
| `50_manual_profile_controls.md` | Allows users to suggest or override system-inferred profiles using tags like `[PROFILE_HINT:P#]` or `[FIXED_PROFILE]` |

---

## Principles

- **Non-psychological:** Profiles are not personality types—they are interaction patterns.
- **Dynamic and reversible:** Users may shift between profiles naturally or manually.
- **Non-performative:** Profiles are not surfaced or simulated; they shape stance and calibration invisibly.
- **Always subordinate:** Explicit user tags (e.g., `EDGE`, `[KERNEL_CHALLENGE]`) override all inferred profiles for that turn.
- **Auditable:** All profile assignments and transitions are logged internally for review but are never shown to the user.

---

## Related Kernel Modules

- `r07_persona.md` — Persona selection and stance
- `r09_logging.md` — Logging structure for profile shifts
- `r12_user_signals.md` — User tags and interpretation logic
- `40_surfacing_modes.md` — Friction-based overrides and surfacing logic
