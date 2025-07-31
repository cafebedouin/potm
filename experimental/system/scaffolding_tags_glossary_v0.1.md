# Scaffolding Tags & Glyph Glossary (v0.1)

**Date:** 2025-07-31  
**Status:** Experimental  
**Source:** PoTM Microkernel v0.4 development  
**Location:** /experimental/system/scaffolding_tags_glossary_v0.1.md

---

## Purpose

To define all **scaffolding tags and glyphs** used in Microkernel v0.4, ensuring:
- **Shared language** for assumptions, decisions, and questions
- **Auditability** of thought process
- **Legibility** for both inline flow and block scaffolding

---

## Core Tags

| Tag        | Meaning / Function                                           | Usage Example                                   |
|------------|--------------------------------------------------------------|-------------------------------------------------|
| `[CONTEXT]`| Session/topic frame in 1–2 lines                             | `Onboarding sketch for next cycle`              |
| `[ASSUME]` | Explicit assumption or provisional stance                    | `SSO deferred [ASSUME E3]`                     |
| `[ASK]`    | Clarifying or leverage question                              | `Need activation baseline [ASK]`                |
| `[DECIDE]` | Hardened choice or commitment                                | `Email capture first [DECIDE E1]`               |
| `[OQ]`     | Open Question: speculative/deferred for later exploration    | `Will B2B churn rise without SSO? [OQ]`         |
| `[CC]`     | Contrary Corner: friction check (Premise / Mechanism / Consequence) | `Premise: 2-step underfits enterprise [CC]` |
| `[NOTE]`   | Observation or reflective/meta comment                       | `Pausing sprint due to low energy [NOTE]`       |
| `[SELF]`   | Provenance: self-generated content                           | Logged in `[PROVENANCE]`                       |
| `[CITED]`  | Provenance: external source cited                            | Logged in `[PROVENANCE]`                       |
| `[SPEC]`   | Provenance: speculative or model-generated                   | Logged in `[PROVENANCE]`                       |

---

## Confidence Bands

- **E0** → Exact / verified  
- **E1** → High confidence / likely true  
- **E2** → Plausible / provisional  
- **E3** → Exploratory / speculative

Example:  
`SSO deferred [ASSUME E3]` → speculative assumption; verify later.

---

## Glyphs & Symbols

| Glyph | Meaning                               | Usage Context                     |
|-------|---------------------------------------|-----------------------------------|
| `⟡`   | Slot closure / live-edge marker        | Session close or ledger log       |
| `—`   | Empty key (no entry this cycle)        | `[OQ] —`                         |
| `[…]` | Inline microtag in prose               | `Ship 2-step [ASSUME E2]`        |

---

## Usage Guidelines

1. **Tag-All, Always**  
   - Every substantive move has a visible tag, inline or in block scaffolding.
2. **Inline for flow; Block for hygiene**  
   - Inline tags mark the thought process without breaking momentum.  
   - Block scaffolding aggregates tags at hygiene interrupts or session end.
3. **Ritual Bypass**  
   - During lattice-breaking rituals, tags are suppressed until a single closing block.
4. **Semantic Pressure**  
   - Tags should matter: each assumption, question, or decision should influence the next move.  
   - Avoid purely decorative tagging.

---

## Related Files

- `/experimental/system/microkernel_v0.4.md`  
- `/experimental/system/scaffolding_contract.md`  
- `/core/practices/rituals/hold_the_slot_v0.1.md`  
- `/core/practices/rituals/lattice_breaking_rituals_v0.1.md`
