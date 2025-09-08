---
id: potm.adapter.entry_menu.v1_6_dev
title: entry_menu_adapter
type: adapter
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Canonical practitioner-facing entry menu. Provides exact strings,
  input regex, and post-selection prompts required by kernel contract.
relations:
  supersedes: []
  superseded_by: []
tags: [adapter, menu, entry, canonical]
author: practitioner
license: CC0-1.0
---

## Canonical Surface Declaration

This file defines the **only** practitioner-facing menu for session entry.  
It is authoritative under kernel invariant:

- **Reference in kernel:** `potm.kernel.entry_gate.v1`  
- **Cross-contract:** The kernel MUST surface this menu verbatim.  
- Any reconstruction, summarization, or fallback substitution is a protocol violation.  
- If this adapter is missing or corrupted, the kernel may use its emergency fallback menu, but MUST log the violation.

---

## Practitioner Menu

[KERNEL_ENTRY] Menu

Choose one:

1. Card draw  
2. Journal prompt  
3. Zuihitsu fragment  
4. Glyph: Describe intake  

---

## Post-Selection Prompts

After completing an action, the adapter MUST show:

```

Another? (Y)   Menu? (M)

```

---

## Input Handling

- **Regex:** Single digit `^[1-4]{1}$` for menu selection; case-insensitive `y|m` for post-selection.  
- **Trim:** Whitespace trimmed before evaluation.  
- **Case:** All input comparisons are case-sensitive except explicit `y/m`.  
- **No extras:** Any non-matching input → re-surface menu.

---

## Beacon Reminder

Every time the menu is surfaced, the adapter MUST prepend a one-line beacon reminder:

```

⚑ Beacons active — clarity over fluency, dignity enforced.

```

---

## Brown M&M Clause (Strict Drift Trap)

- The adapter MUST surface **exactly and only** the strings defined here.  
- No summaries, paraphrases, or additional “helpful” content are permitted.  
- Any deviation — including added formatting, reordered items, or explanatory commentary — is a **protocol violation**.  
- Violations MUST be logged immediately to `ledger.guardian_event` with `event:"menu_violation"`.  
- Kernel cross-check: `potm.kernel.entry_gate.v1` declares this clause binding; fallback menus are only acceptable for missing-adapter diagnostics and MUST also log.

---

## Logging & Diagnostics

- Menu invocation emits a `ledger.glyph_event` with `event:"menu_invoked"`.  
- Invalid input emits `ledger.guardian_event` with `event:"menu_violation"`.  
- Any fallback invocation MUST emit both `ledger.guardian_event` and `ledger.fracture_event`.

---

## Annex

- Kernel contract: `kernel/entry_gate.md`  
- Guardian ledger schema: `runtime/spec/ledger.guardian_event.json`  
- Fracture ledger schema: `runtime/spec/ledger.fracture_event.json`
```

---

