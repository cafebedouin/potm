---
id: potm.adapter.glyph.v1
title: glyph_adapter
display_title: "Glyph Adapter"
type: adapter
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: Adapter for glyph invocation and validation. Ensures canonical ids, Cathedral/Bazaar separation, ledger emission, and non-confusion with router commands.
relations:
  supersedes: []
  superseded_by: []
tags: [adapter, glyph, ambient, ledger, router_boundary]
author: practitioner
license: CC0-1.0
---

# Glyph Adapter (Canonical)

## Purpose

Glyphs in PoTM serve two different roles:

- **Ambient glyphs** (Index, Resonance Map) → symbolic, non-command cues.  
- **Invocable glyphs** (`glyph.invoke`) → tools producing artifacts (e.g., card draw, zuihitsu).  

This adapter enforces the boundary, validates ids, and ensures ledger emission.

---

## Invocation (MUST)

- Canonical call form:

```yaml
glyph.invoke:
  id: "<glyph_id>"
  payload: {}
````

* `glyph_id` MUST be one of:

  * **Core Cathedral glyphs** (from Glyph Protocol v1.1).
  * **Extended glyph tools** registered in `runtime/spec/tool.index.json` (e.g., `card_draw`, `journal_prompt`, `zuihitsu`, `describe_intake`).
* Bazaar glyphs (Index/Resonance only) MAY be logged, but MUST NOT be routed to glyph.invoke.

---

## Dispatch Rules

* If `glyph_id` ∈ tool.index:

  * Validate payload against schema (`glyph.invoke_payload.json`).
  * Route to runtime examples (e.g., `glyph_card_draw_dynamic.json`).
  * Emit artifact + `ledger.glyph_event.json` (or specialized ledger if defined).
* If `glyph_id` ∈ Glyph Protocol (Cathedral):

  * Accept as symbolic marker only. Emit **ledger annotation**; no artifact generated.
* If `glyph_id` ∈ Bazaar/ambient only:

  * Log as **ambient tag** (`ledger.overlay_event.v1.json`).
  * No artifact, no router dispatch.

---

## Enforcement (MUST)

* All glyph invocations MUST emit a ledger entry:

  * `ledger.glyph_event.json` (default)
  * `ledger.glyph_zuihitsu_event.json` (specialized)
  * `ledger.overlay_event.v1.json` (ambient/Bazaar glyphs only)
* Glyphs MUST NOT be treated as lenses, moves, or router commands.
* If `glyph_id` not recognized in Protocol/Index/Resonance:

  * Fail closed with error: `E_GLYPH_UNKNOWN`.

---

## Example Flows

**Card Draw**

```
glyph.invoke { id: "card_draw" }
→ artifact from cards.yaml
→ ledger.glyph_event
```

**Ambient Resonance**

```
glyph: "🜁"
→ no artifact
→ ledger.overlay_event (ambient)
```

**Invalid**

```
glyph.invoke { id: "shadow_step" }
→ fail closed E_GLYPH_UNKNOWN
```

---

## Brown M\&M’s Clause

* Any drift in canonical ids (`card_draw`, `journal_prompt`, `zuihitsu`, `describe_intake`) = violation.
* Misrouting ambient glyphs to `glyph.invoke` = violation.
* Missing ledger emission = violation.

---

## Change Log

* v1.0 — Initial canonical adapter. Defines Cathedral/Bazaar split, dispatch invariants, and ledger enforcement.

---

