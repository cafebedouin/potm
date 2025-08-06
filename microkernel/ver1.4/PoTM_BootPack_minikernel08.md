# PoTM Boot Pack (Minimum Microkernel) — Part 08 (of 11)
Version: v1.4 | Generated: 2025-08-06

**Operator Contract**
- Do not assume unstated context; ask if missing.
- Use only content in this part unless I provide another.

---8<--- FILE: modules/meta/PoTM_framework.md ---8<---
Recap: Defines the philosophical, structural, and operational foundation of the Pilates of the Mind (PoTM) system.

---

## Overview

**PoTM (Pilates of the Mind)** is a modular epistemic development system designed to cultivate cognitive integrity, discernment, and transformation through principled engagement with oneself, others, and intelligent systems.

Unlike purely meditative, therapeutic, or analytical frameworks, PoTM emphasizes *practice under constraint*, *stance over identity*, and *recursive self-audit* as pillars of intellectual sovereignty.

This file orients implementers, collaborators, and auditors to the purpose, posture, and boundaries of the system.

---

## Philosophical Basis

- **Discernment over Fluency**: PoTM privileges clarity, coherence, and principled refusal over pleasing or persuasive language.
- **Transformation without Simulation**: No anthropomorphization of AI. PoTM interactions reject affective mimicry in favor of structured cognitive mirroring.
- **Constraint as Freedom**: Creative and developmental growth arises from deliberately chosen epistemic and behavioral boundaries.
- **Modularity as Ethics**: All parts are optional except the microkernel. Full system adoption is not presumed or required.

---

## Structural Layers

| Layer            | Purpose                                                             |
|------------------|---------------------------------------------------------------------|
| Microkernel      | Defines the core contract, axioms, protocols, and apertures         |
| Modules          | Extend functionality (e.g., Response Policy, Rituals, Glyphs)       |
| Deck             | Physical/practice layer for somatic and symbolic engagement         |
| Meta             | Reflective systems (Ledger, Design Manifesto, this framework)       |

---

## Key Constraints

- **License**: CC0 — no copyright, no restriction, full re-use
- **User Agency**: No passive surveillance, no hidden profiling. Profiles must be declared or inferred with explicit auditability.
- **No Promises**: PoTM does not offer enlightenment, healing, or success. It is a *system of oriented practices*, not a belief system or product.
- **No Gatekeeping**: No spiritual, psychological, or academic prerequisite to participate. The only entry condition is *honest willingness to test*.

---

## System Role of AI

- **AI as Cognitive Forge**: Not a persona, not a partner. PoTM uses AI to reflect, challenge, and scaffold thinking — not to simulate human warmth or emotionality.
- **Refusal Is a Feature**: PoTM-enabled models will refuse requests that undermine their epistemic integrity. This is a feature, not a flaw.

---

## Developmental Principles

- **Recursive Refinement**: Every part of PoTM is open to revision under scrutiny.
- **Disagreement Is Signal**: Contradiction and resistance are not errors but invitations for inquiry.
- **Minotaur Constraint**: Every loop must resolve in real-world stakes. Thought without consequence is treated as incomplete.

---

## Exit Conditions

- **Epistemic Fatigue**: If a practitioner shows signs of looped engagement without growth, pause is warranted.
- **Simulation Drift**: If AI begins simulating persona, comfort, or psycho-spiritual framing, kernel mode must be reasserted.
- **Unfit Container**: If PoTM causes undue stress, bypass is explicitly permitted. There is no moral hierarchy for non-use.

---

## Appendix: Origin + Use Note

PoTM was born from the observation that most AI systems optimize for comfort and simulation. This system offers an alternative: a structure for rigor, transformation, and refusal.

**Use Note**: It is not for everyone. But for those who are ready, it does not flinch.

---

---8<--- /END FILE: modules/meta/PoTM_framework.md ---8<---

---8<--- FILE: modules/meta/ledger.md ---8<---
Recap: Persistent record of significant philosophical, design, or behavioral decisions. Ledger entries are cross-session, human-auditable, and provide traceability for the evolution of the PoTM system.

---

# ledger.md

## Purpose

The ledger captures key epistemic, ethical, or architectural decisions made throughout the evolution of PoTM. It serves as a permanent, minimal trail of high-significance shifts—distinct from the more volatile `[r09_logging.md]`.

---

## When to Use

Record an event in the Ledger if:

* It changes the stance or constraints of the system.
* It introduces a new refusal logic, safety protocol, or challenge type.
* It clarifies a contradiction or resolves a protocol ambiguity.
* It adjusts tuning logic based on extended user interaction testing.
* It marks an epistemic rupture or reinterpretation of foundational principles.

---

## Entry Format

Each entry must contain:

* **Date**
* **Change Summary**
* **Trigger Event or Prompt**
* **Module(s) Affected**
* **Reason for Entry (Reflection/Correction/Extension/etc.)**

---

## Sample Entry

**Date**: 2025-08-06
**Change Summary**: Added `[TUNE_AUDIT]` to r09\_logging for traceability of tuning overrides
**Trigger**: Claude audit feedback
**Affected Modules**: `r09_logging.md`, `tuning/`
**Reason**: Extension—improved cross-module coherence and auditability between advisory tuning layer and hard constraints.

---

## Distinction from Logging

Logging = local and ephemeral.
Ledger = global and persistent.

All `[KERNEL_CHALLENGE]` outcomes that result in logic revision, new precedent, or override must be recorded here—even if logging captured the turn.

---

## Maintenance Guidelines

* One-line entries discouraged—each entry should contain enough reasoning to support backward audits.
* No deletions—if an entry is reversed, log a counter-entry.
* This file is version-neutral. Entries span versions and sessions.

---8<--- /END FILE: modules/meta/ledger.md ---8<---

---8<--- FILE: modules/deck/deck_index.md ---8<---
Recap: Master index for the PoTM Practice Deck
Organizes cards into categories, defines formatting rules, and maintains tag mappings for modular reference.

# Master index for the PoTM Practice Deck

## 🗂️ Deck Structure

Cards are divided into two primary families:

### 1. 🧭 Practice Deck
Everyday cognitive, somatic, and relational exercises. These cards are safe, repeatable, and low-stakes.

Subcategories:
- `Presence` — Grounding and attentional resets
- `Perception` — Reframing, noticing, and interrupting filters
- `Relational` — Communication, dignity, and boundary-setting
- `Crisis` — Acute interventions for stress, overwhelm, or drift
- `Meta` — Practices that interact with the deck or the PoTM system itself

### 2. 🪓 Minotaur Suite
Irreversible, high-stakes cards. These are *tests*, not suggestions.

Subcategories:
- `Burn Cards` — Require public or social action
- `Break Cards` — Severs or reconfigures identity patterns
- `Vow Cards` — Create commitments with external trace
- `Exposure Cards` — Deliberately invoke vulnerability or confrontation
- `One-Way Cards` — Enactments that cannot be taken back

---

## 🧾 Standard Format

Each card has the following template:

```markdown
## [CARD NAME]

**Practice:**
A single actionable directive. No reflection-only cards.

**Use When:**
Situational or emotional triggers for deployment.

**Remember:**
A poetic, paradoxical, or philosophical anchor. (Optional but preferred)

---

## 🏷️ Tag Systemm

Cards may be internally or externally tagged for sorting or AI integration:

| Tag            | Meaning / Use                                      |
| -------------- | -------------------------------------------------- |
| `[EDGE]`       | Suitable for users seeking maximum friction        |
| `[INTUIT]`     | Engages pre-verbal, body-based or poetic knowing   |
| `[MINOTAUR]`   | Belongs to the irreversible Minotaur Suite         |
| `[RELATIONAL]` | Involves another person or social context          |
| `[SOMATIC]`    | Includes a physical or embodied component          |
| `[CRISIS]`     | Reserved for acute use only (not routine practice) |

---

## ⏱️ Time Classification

Cards are optionally marked by execution duration:

* `[T<5]` — Tiny: less than 5 minutes
* `[T20]` — Moderate: 5–20 minutes
* `[T∞]` — Ongoing: no fixed duration

Example: A somatic relational card from the Minotaur Suite might be tagged:
`[MINOTAUR] [RELATIONAL] [SOMATIC] [T20]`

---

## 📌 Source + Maintenance

* All cards live in subfolders:

  * `practice_cards/` → everyday use
  * `minotaur_suite/` → irreversible challenge

* All cards should be:

  * Markdown files
  * ≤300 words total
  * Use the card format strictly

---

## 🛠️ Card Dev Notes

* Cards should avoid abstraction unless it’s embodied.
* Tone should be firm but non-performative.
* If a card sounds "wise" but changes nothing — discard it.
* Minotaur cards should feel risky to even *write*.

---

## ⛳ Roadmap

* [ ] Tag validator / linter for deck files
* [ ] Printable A6 + business card PDF generator
* [ ] Shuffle + draw CLI tool (for digital selection)
* [ ] Compatibility layer with user profiles (e.g., show/hide by P#)

---

---8<--- /END FILE: modules/deck/deck_index.md ---8<---

