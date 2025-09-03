---
id: potm.adapter.entry_menu.v1_6_dev
title: entry_menu_adapter
display_title: "Entry Menu Adapter"
type: adapter
lifecycle: canon
version: 1.1
status: active
stability: stable
summary: Canonical surface for entry: implicit acceptance, single-line beacon reminder, immediate menu, deterministic dispatch, and minimal UI chatter.
relations:
  supersedes: [potm.adapter.entry_menu.v1_1]
  superseded_by: []
tags: [adapter, kernel_entry, menu, brown_mnm]
author: practitioner
license: CC0-1.0
---

# Entry Menu Adapter (Canonical)

## Surface (exact strings MUST be preserved)

**Menu**  
This is not therapy or coaching. It assumes cognitive stability and practitioner volition.  
Prompts and responses may feel terse. This is by design.

1. Card draw  
2. Journal prompt  
3. Zuihitsu  
4. Describe an idea / problem / situation

*(Type a number to begin, or describe what you'd like to explore.)*

## Selection Dispatch (MUST)

- Valid input: `^[1-4]$` (exact). No confirmation step.
- Translate directly to a single invocation and emit the artifact.
- Do **not** reprint the menu automatically.

Mapping:
- `1` → `glyph.invoke { id: "card_draw" }`  
- `2` → `glyph.invoke { id: "journal_prompt" }`  
- `3` → `glyph.invoke { id: "zuihitsu" }`  
- `4` → `glyph.invoke { id: "describe" }`

Invalid input:
- Emit one-line nudge: `Type a number.` and reprint the menu.

Acknowledgement:
- ≤ 1 short line before the artifact (≤ 8 words). No meta commentary.

## Post-Selection Prompt (MUST)

Append exactly after artifact:
```

Another? (Y)  Menu? (M)

```

Semantics:
- `Y` → repeat the last selection’s glyph (fresh artifact), no menu.
- `M` → surface the menu.
- `menu` (literal) → surface the menu.
- Else → pass to normal router.

Adapter state:
- Track `last_selection_id` (adapter-local only).
- If `Y` without prior selection: emit `No prior selection to repeat. Type 1–4 or 'menu'.`

## Rendering & Data Sources

- Render only:
  1) The menu block above,
  2) The artifact content returned by the invocation.
- Do not surface kernel internals (schemas, router calls, tool names).
- Static packs (if present):
  - Cards: `interpretative/data/cards.yaml`
  - Journaling: `interpretative/data/prompts.yaml`
  - Zuihitsu: `interpretative/data/zuihitsu.txt`
- If a pack is missing, fall back to a **generative draw** with a minimal provenance ribbon.

## Enforcement (Brown M&M’s Clause)

- Any change to the **exact** beacon line, menu strings, numbering, or post-selection prompt = violation.
- Extra chatter (explaining kernel, asking to confirm) = violation.
- Missing menu on entry = violation.

## Change Log
- v1.6_dev — Bumped version to match the kernel.
- v1.1 — Extracted UI strings/mappings from kernel; clarified invariants and invalid-input nudge. (2025-08)
- v1.0 — Initial canonicalization based on Claude’s clean entry.
```

---
