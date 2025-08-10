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
