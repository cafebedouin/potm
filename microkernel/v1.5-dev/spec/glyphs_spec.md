---
id: potm.glyphs.spec.v1
title: "Glyph System Specification"
version: 1.0
status: spec
type: implementation
audience: AI developers, kernel maintainers
---

# Glyph System Specification

This document defines the glyph subsystem for the PoTM kernel.  
It specifies annexes, lint rules, tagging conventions, and meta-tools.  
It is intended for implementation by AI developers and assistants.

---

## 1. Scope

- Glyphs live in the **Interpretive Layer** only.  
- **Non-binding:** They never alter routing, ENTRY/EXIT, or meta_locus.  
- **Audience:** Models first, humans optional.  
- **Purpose:** Telemetry shorthand (compressed symbolic commentary).  

---

## 2. Annexes

Three external annex files:

1. `annex/glyph_protocol.md`  
2. `annex/glyph_index.md`  
3. `annex/glyph_resonance_map.md`

---

## 3. Lint Rules

External lint file: `lint/potm.glyphs_lint.md`

---

## 4. Ledger Tagging Convention

Models emit glyph commentary via ledger notes:

```
2025-08-24T14:41:12Z    RELATION_ZONE    4f8d8b…    #glyphs_ai: 🝮, ✴️
```

* Prefix: `#glyphs_ai:`  
* Glyphs separated by commas  
* May include Unicode or ASCII fallbacks  

---

## 5. Meta-Tools

Meta-tools live in your meta-tool directory (e.g., `kernel/60_meta_tools.md`):

- `SYMBOL.read_current` (binding: false)  
- `GLYPH.audit` (binding: false, diagnostic only)

---

## 6. Governance

* **Cathedral:** Core primitives, modifiers, combos (protocol annex).  
* **Bazaar:** Index + resonance map (ambient & experimental).  
* **Sunset:** 12-month unused glyphs → deprecated (audit flagged).

---

## 7. Compliance

* **P1-compliant:** Session-local, no schema changes, no external deps.  
* **Safe failure:** Ignored if unused; audit reports drift.

---

## 8. Deliverables

- Add 3 annex files under `annex/`  
- Add lint rules under `lint/`  
- Extend ledger parser for `#glyphs_ai:` (no schema bump)  
- Implement `SYMBOL.read_current` & `GLYPH.audit` as binding:false

```

```yaml