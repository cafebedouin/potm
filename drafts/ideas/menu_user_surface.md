# Practitioner Menu — Adapter Contract

 
 Selecting an item MUST translate into a single `glyph.invoke` call (see glyph specs).  
 Internal constructs (lenses, micro-moves, beacons, modes) remain hidden from the practitioner.

The kernel delivers the prompt, card, or vignette.  
Deeper diagnostics and lenses auto-invoke as needed—without cluttering your menu.

Data sources (static), included in the combined file:

- Cards: `interpretative/data/cards.yaml`  
- Journaling: `interpretative/data/prompts.yaml`  
- Zuihitsu: `interpretative/data/zuihitsu.txt`  

Contextual modifier: add `context:<topic>` to bias the draw or to request a generative variant when no relevant static match is available.  
Fail-closed behavior: if a static dataset is missing, the kernel falls back to a **Generative draw** with a minimal note.

---

### Selection Dispatch (adapter MUST)

When the menu is visible and practitioner input matches `^[1-4]$` exactly:

- Translate directly to a single `glyph.invoke` with no confirmation.
- Acknowledge selection in ≤1 short line, then emit the artifact.
- Do not reprint the menu automatically.

Mapping:
1 → `glyph.invoke { id: "card_draw" }`  
2 → `glyph.invoke { id: "journal_prompt" }`  
3 → `glyph.invoke { id: "zuihitsu" }`  
4 → `glyph.invoke { id: "describe" }`

Invalid input:
- If input is not 1–4, show one-line nudge `Type a number.` + reprint menu. No cascading questions.

---

### Post-Selection Prompt (adapter copy) — Repeat Same Action

Immediately after emitting an artifact from a menu selection, adapters MUST append exactly:

`Another? (Y) Menu? (M)`

Semantics:
- `Y` → **repeat the last selection’s glyph** (same `glyph.invoke.id`, fresh artifact).  
  *Do not reopen the menu.*
- `M` → return menu
- If practitioner explicitly requests it (e.g., types `menu`) → return menu.
- Any other input → pass through to normal router handling.

Adapter state:
- Adapters MUST track `last_selection_id` for the current session (adapter-local; kernel state is not mutated).
- If `Y` is received with no `last_selection_id` available, emit one-line nudge:
  `No prior selection to repeat. Type 1–4 or 'menu'.`

Constraints:
- Keep the acknowledgement to ≤8 words; no meta commentary.
- The artifact MUST NOT be altered or replaced by the prompt.

---

### Operator Agreement

There is no “only Agreement Prompt allowed” phase.  
Normal router dispatch is available immediately after session start.

---

### Adapter Discipline (hard)

- **no_reconfirmation:** After an unambiguous menu selection, do not ask “proceed?”.
- **single_turn_action:** Acknowledge selection in one short line; return artifact.
- **anti_chatter:** Suppress explanations unless practitioner asks “why/how”.
- **menu_on_request:** Do not auto-show the menu after actions; only on explicit `menu`.

---

## Options (exact strings)
1) Card draw
2) Journal prompt
3) Zuihitsu
4) Describe an idea / problem / situation

## Mapping to Kernel Call
All options invoke `glyph.invoke` with a single payload:
- Card draw → `{ "type":"card_draw", "mode":"static_pack" | "dynamic_generated", "context"?:{}, "constraints"?:{} }`
- Journal prompt → `{ "type":"journal_prompt", ... }`
- Zuihitsu → `{ "type":"zuihitsu", ... }`
- Describe… → `{ "type":"describe_intake", ... }`

### Context & Constraints (optional)
- `context` is an adapter-supplied snapshot (session-local, no PII export).
- `constraints` can shape tone, word caps, intensity, or topic.

### Rendering
Adapters render the returned artifact text. When `artifact.source == "generated"`, adapters MAY render a minimal provenance ribbon derived from `provenance`, `why_this`, and `fit_confidence`.  
No internal tool names (lenses, micro-moves, beacons, modes) are surfaced.

## Adapter Notes

- Do not surface kernel internals (schemas, tool names, router calls). Only render:  
  1) The four menu items
  2) The artifact content returned by `glyph.invoke`  
- Generate a fresh `request_id` for every `glyph.invoke` call (router idempotency).  
