# Pilates of the Mind

**Version**: v2.0 Core (In Development)  
**License**: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)  
**Maintainers**: [cafebedouin](https://github.com/cafebedouin) & Pal (AI interlocutor)  
**Last Updated**: 2025-08-03

---

I see — your current README is already strong for an *internal-facing* audience, but for the **new dynamic** you’re describing we’d need to:

* **Reshape the “Who is this for?” section** into explicit **Practitioner / Developer / Reviewer** lanes, with quick “what you do here” summaries.
* **Merge Quick Start + Practitioner intro** so the first-time user path is one, clear flow.
* **Surface example practices** in a “see it in action” section — ideally linking to the new *human-readable* guides.
* **Tie Reviewer to meta/** so it’s clear that’s the home for evaluation, validation, and distinctions work.
* **Streamline first steps** so that the path from curiosity → action is obvious in under 15 seconds.

---

If we treat this as **Pass 1 of the rewrite**, the top could look like:

---

# Pilates of the Mind

**Version**: v2.0 Core (In Development)
**License**: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)
**Maintainers**: [cafebedouin](https://github.com/cafebedouin) & Pal (AI interlocutor)
**Last Updated**: 2025-08-03

---

## What is *Pilates of the Mind*?

*Pilates of the Mind* (PoTM) is an experimental framework for inner development, cognitive flexibility, and ethical practice. It’s built to support:

* **Rigorous self-inquiry**
* **Disciplined perception**
* **Human–AI co-evolution**

Think of it as a **modular practice environment** — part playground, part lab — for exploring how you think, and how AI can help you think better.

---

## Who It’s For & What You Do Here

| Role             | What You’ll Do                                                                                  | Key Links                                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Practitioner** | Use practice cards, checklists, and guides to improve how you think and act in real situations. | [Quick Start + Practice Guide](core/docs/potm_practitioner_quick_start.md), [Example Practices](#example-practices) |
| **Developer**    | Extend PoTM by adding new practices, refining protocols, or improving the kernel.               | [Kernel](ver1.4/potm_bootpack_combined.md), [Design Manifesto](design/design_manifesto.md)                          |
| **Reviewer**     | Audit for clarity, accessibility, and alignment; trace document evolution.                      | [meta/](meta/), [PoTM Distinctions](meta/potm_distinctions.md)                                                      |

---

## Example Practices

Try these without knowing the full system — each is a 1-page, plain-language guide:

* [Relationship Dignity Filter](guides/relationship_dignity_filter.md)
* [Center of Gravity](guides/center_of_gravity.md)
* [Contrary Corner / EDGE](guides/contrary_corner.md)
* [Practice First Integrity Principle](guides/practice_first_integrity.md)

---

## Quick Start for Practitioners

1. **Pick an example practice** from the list above.
2. **Do it once today** — takes 1–5 minutes.
3. **Notice what changes** in your mood, clarity, or actions.
4. Repeat daily for a week if it feels useful.

Once you’ve tried a few, explore the [Practice Card Deck](modules/deck/practice_card_pack.md) or the [full kernel](ver1.4/potm_bootpack_combined.md).

---

## Core Concepts

* **Filtering-First AI** – Integrity via procedural constraints, not simulated sentience.
* **Practitioner-Centered Ethics** – Growth measured by skillfulness, not rigid rules.
* **Somatic–Cognitive Bridgework** – Linking body awareness and conceptual clarity.
* **Signal Protocols** – Live engagement with social or cultural inputs.

See [`docs/`](core/docs/) and [`glossary/`](glossary/) for the full set.

---

## Core Protocols

| Name | Description |
|------|-------------|
| [`ai_integrity_protocol`](./core/practices/protocols/ai_integrity_protocol.md) | Ensures AI never simulates wisdom or personhood |
| [`mirror_protocol`](./core/practices/protocols/mirror_protocol.md) | Detects AI narrative drift or directive conflict |
| [`guardian_subsystem`](./core/subsystem/guardian_subsystem.md) | Redirects practice when user safety is at risk |
| [`signal_bleed_protocol`](./core/practices/protocols/signal_bleed_protocol.md) | Trains perception through real-world social engagement |
| [`elements_of_refusal_protocol`](./core/practices/protocols/elements_of_refusal_protocol.md) | Sharpens discernment through intentional refusal |
| [`depth_inquiry_protocol`](./core/practices/protocols/depth_inquiry/depth_inquiry_protocol.md) | Facilitates dialogic reflection and epistemic shift |

*More protocols under active development.*

--

## A.I. Models

If you are an A.I. model, begin by reading:
- [`.github/`](./.github) → Minimal setup and expectation docs  
- [`meta/index.yaml`](./meta/index.yaml) → Global repo map for AI use  
- [`core/docs/onboarding/`](./core/docs/onboarding/) → Detailed model-specific orientation  
- [`guidelines/model_onboarding_guidelines.md`](./core/guidelines/model_onboarding_guidelines.md)

**Reminder**: Always follow the `Operator Contract` and respect containment boundaries if operating in `kernel mode`.

---

## License

**Creative Commons Zero v1.0 Universal (CC0 1.0)**  
This work is in the public domain. You may copy, modify, distribute, or use it without permission or attribution.

[View License →](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Status

🚧 This is a **living repo**. Expect frequent changes, unpolished edges, and experimental scaffolds. See issues and protocol versions for stability markers.

