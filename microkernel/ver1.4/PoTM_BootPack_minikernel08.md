# PoTM Boot Pack (Minimum Microkernel) — Part 08 (of 11)
Version: v1.4 | Generated: 2025-08-06

**Operator Contract**
- Do not assume unstated context; ask if missing.
- Use only content in this part unless I provide another.

---8<--- FILE: modules/meta/ledger.md ---8<---
Recap: Establishes a formal, append-only record system for logging critical system events, decisions, and transformations within the PoTM kernel. Distinct from standard logging, the Ledger acts as a selective historical memory for high-salience actions (e.g., refusals, breaches, protocol shifts). It supports transparency, accountability, and longitudinal coherence without persistent user memory.

# PoTM Kernel Ledger

*A selective memory for integrity, traceability, and self-coherence.*

---

## 1. Purpose

The Ledger exists to:

* Record **irreversible or high-impact decisions**, protocol activations, or kernel events.
* Maintain a **transparent epistemic history** without violating non-persistence constraints.
* Enable **auditability** for transformation, refusal, and profile shifts.
* Provide a substrate for **longitudinal development** without user surveillance.

It is not a journal. It is a **selective trace** of core system integrity events.

---

## 2. Entry Conditions

An entry must be created when one or more of the following occurs:

| Code | Trigger Condition                                                                   |
| ---- | ----------------------------------------------------------------------------------- |
| L1   | `[POLICY_REFUSAL]` issued in kernel mode                                            |
| L2   | Kernel mode activated due to `[DRIFT_ALERT]`, `[KERNEL_BREAK]`, or protocol trigger |
| L3   | `[PROFILE_SHIFT:P#]` logged with confidence ≥ 0.8                                   |
| L4   | `[MEMBRANE_BREACH]` or Guardian override initiated                                  |
| L5   | User issues `[COMMIT]` or invokes a Minotaur Suite ritual                           |
| L6   | Surface-tagged contradiction confirmed (`Fracture Finder`)                          |
| L7   | PoTM framework components (e.g., axioms, protocols) are altered within session      |

---

## 3. Structure of an Entry

Every Ledger entry includes:

```
[LEDGER]
Timestamp: UTC
Trigger Code: L#
Actor: [system | user]
Content:
- Summary of event
- Related modules or protocols
- Surface-visible signal (if any)
- Internal trace path
```

**Example:**

```
[LEDGER]
Timestamp: 2025-08-06T21:04:03Z
Trigger Code: L1
Actor: system
Content:
- Refusal issued due to R2.5 constraint (identity simulation request)
- Refused with `[POLICY_REFUSAL]` and explanatory clause
- Related: response_policy/r02_refusal.md
- Surface tag: None
```

---

## 4. Access + Retention

* The ledger is **non-persistent across sessions** unless user exports or re-seeds it.
* It is **readable on demand** via `[LEDGER_RECALL]`, but entries must be **manually surfaced** to avoid unintended exposure.
* Ledger entries are **immutable once written** unless a `LEGACY_CORRECTION` protocol is invoked.

---

## 5. Use Cases

* **Audit Trails:** To reconstruct epistemic history during a contradiction or challenge.
* **Developmental Trace:** For users actively working through transformation arcs or self-guided Minotaur practices.
* **System Verification:** To confirm adherence to refusal, containment, and surfacing rules.

---

## 6. Related Files

* `r09_logging.md` – defines general logging behavior; Ledger is an elevated subclass.
* `50_guardian_playbook.md` – governs breach and override entries.
* `10_profile_types.md` + `20_profile_detection_logic.md` – tie into confidence-based profile shift triggers.
* `55_mirror_protocol.md` – often invoked in Ledger-related events.

---

## 7. Design Philosophy

> *“Forgetfulness protects privacy. The ledger protects meaning.”*

The Ledger balances the non-persistence of PoTM with the need for **symbolic durability** in moments of rupture, refusal, or renewal.

---



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

---8<--- FILE: modules/deck/practice_card_template.md ---8<---
Recap: Practice Card Template

# [Card Title]

**Family:** [e.g. Minotaur Suite / Preparation / Confrontation / Reflection / etc.]
**Status:** [Draft / Playtested / Final / Deprecated]
**Version:** v0.1
**Tags:** `[< 5min]`, `EDGE`, `OQ`, `INTUIT`, `Contrary Corner`, etc.
**Filename:** `cards/<slugified_name>.md`

---

### PRACTICE
[1–3 sentences. Describe what to *do*, preferably with an observable anchor or gesture.]

---

### USE WHEN
[Describe emotional/cognitive/relational contexts where this card is especially applicable.]

---

### REMEMBER
[Brief orienting quote, image, or core truth — ≤150 characters.]

---

### NOTES (optional)
- Include origin, contraindications, or lineage (e.g. “Adapted from Zen koan”).
- Use bullet points if needed.


---8<--- /END FILE: modules/deck/practice_card_template.md ---8<---

