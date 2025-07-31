# Core Documentation — *Pilates of the Mind*

Welcome to the **core documentation layer** of the *Pilates of the Mind* (PoTM) repository.  
If the root [`README.md`](../../README.md) gives you the elevator pitch, this directory is where we **slow down** and show the structure, rationale, and connective tissue of the framework.

---

## 📚 Purpose of `core/docs/`

This folder contains **narrative and reference material** for contributors and practitioners who want to:

- Understand the **full architecture** of PoTM beyond the short descriptions in the main README.
- Navigate **onboarding paths** for human practitioners and AI collaborators.
- Explore **case studies, peer reviews, and design rationales** that support the evolution of protocols.

Think of this directory as a **living manual**: it bridges the concise **protocol files in `/core/protocols/`** with the **meta‑level principles in `/meta/`**.

---

## 📖 Directory Overview

| Subfolder / File                                | Purpose                                                           |
|-------------------------------------------------|-------------------------------------------------------------------|
| **[`onboarding/`](./onboarding/)**              | Entry points for humans and AI: manifests, prompts, and rituals.  |
| **[`onboarding/rituals/`](./onboarding/rituals/)| Optional framing rituals and response practices for active use.    |
| **[`invocations/`](./invocations/)**            | Documentation of Pal invocation grammar and persistent modes.     |
| **[`case_studies/`](./case_studies/)**          | Archived examples, such as the *Practitioner-Centered Ethics* case study. |
| **[`peer_reviews/`](./peer_reviews/)**          | Peer and model commentary on framework components; appendices for reflective development. |
| **[`peer_artifacts/`](./peer_artifacts/)**      | Generated materials or structured outputs from peer/model exercises. |

---

## 🔹 How This Layer Fits Into the Repo

- **`/meta/`** → Normative principles, conceptual frames, and practitioner tools.  
  *Tells you why the system exists and what rules it lives by.*

- **`/core/docs/` (this folder)** → Extended documentation and onboarding for practitioners and AI collaborators.  
  *Shows you how to enter, interpret, and reflect within the system.*

- **`/core/protocols/` & `/core/modules/`** → Operational building blocks of the practice environment.  
  *Implements the work described here.*

---

## 🧭 Recommended Reading Path

1. **Start with [`onboarding/00_MANIFEST.md`](./onboarding/00_MANIFEST.md)** to see the entry posture for humans.  
2. **Review the Pal invocation grammar** in [`invocations/pal_invocation_grammar.md`](./invocations/pal_invocation_grammar.md) if using AI support.  
3. **Explore a case study** (e.g., [`case_studies/pce_case_study.md`](./case_studies/pce_case_study.md)) to see the framework in action.  
4. **Optionally** read peer/model reviews in [`peer_reviews/`](./peer_reviews/) to understand evaluation and iteration.

---

## 🛠 Contributing via Documentation

If you are extending PoTM, additions here should:

1. **Clarify or teach** — provide orientation or examples, not just raw protocol specs.  
2. **Connect to meta principles** — reference the binding norms in [`/meta/principles/`](../../meta/principles/).  
3. **Avoid bloat** — extended essays and reflections belong in `/meta/frames` or `/docs/` at the repo root, not here.

When in doubt, add an **index entry** to [`core/docs/README.md`](./README.md) so contributors and practitioners can find it.

---

## 🔗 Cross-References

- **Foundational Principles:** [`/meta/index.md`](../../meta/index.md)  
- **Operational Protocols:** [`/core/protocols/protocol_index.md`](../protocols/protocol_index.md)  
- **Experimental Workbench:** [`/experimental/README.md`](../../experimental/README.md)

---

*Last updated:* 2025‑07‑31  
*Status:* Stable (updates expected as onboarding expands)
