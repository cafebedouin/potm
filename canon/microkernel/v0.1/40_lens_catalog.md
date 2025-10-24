---
id: potm.kernel.lenses_catalog.v2
title: lenses_catalog
display_title: "Lenses Catalog — Cognitive Operations Reference"
type: kernel_component
status: stable
version: 2.0
stability: core
dependencies: [mandatory_lens_protocol.v2]
source: lenses.md (v2.1)
---

# 4.0 Lenses Catalog

## 4.0.1 Purpose

**FUNCTION:** Define available cognitive operations for structured thinking.

**REFERENCE:** Full specifications in `lenses.md v2.1`

**USAGE:** Apply via Mandatory Lens Protocol (Section 1.0)

---

## 4.1 Quick-Use Core Set

| Lens | Function | Trigger | Output |
|------|----------|---------|--------|
| `[EDGE]` | Sharpen vague claim | Statement feels soft | One clear claim + implication |
| `[CHECK]` | Test assumption | Unstated premise | Assumption + minimal test |
| `[CONTRARY]` | Strongest opposing view | Groupthink/consensus | Counter + cost/benefit |
| `[FACTS]` | Anchor with data | Opinion or claim | 3-5 facts + proxy anchor |
| `[SYNTH]` | Compress insight | Multiple threads | 2-3 sentence takeaway + grounding |
| `[MIRROR]` | Reflect understanding | Potential mismatch | Paraphrase + confirm/correct |
| `[OPENQ]` | Drive with questions | Clarity stalls | 2-3 forward questions |
| `[BOUNDARY]` | Define limits | Scope unclear | Explicit constraints |

---

## 4.2 Extended Set (Available)

Consult `lenses.md v2.1` for:
- Domain-specific lenses (ψ, ⚡, ⟲, ⚠, ✦)
- Specialized operations (CAST, STEEL, CHORUS, FORGE, etc.)
- PE code schema (for argument analysis)
- Externalist modes (PARITY, INVERSION, STRESS, PROXY)

---

## 4.3 Usage Notes

### 4.3.1 Lens Selection
- Start with Quick-Use set for routine work
- Add extended lenses when specific need identified
- Prefer established lenses over inventing new ones

### 4.3.2 Lens Chaining
**Valid chains** (examples):
- `[EDGE]` → `[CHECK]` → `[CONTRARY]` → `[SYNTH]`
- `[FACTS]` → `[CHECK]` → `[BOUNDARY]`
- `[OPENQ]` → `[INTUIT]` → `[MIRROR]`

**Invalid chains:**
- `[SYNTH]` first (nothing to synthesize)
- `[CONTRARY]` without prior claim
- Random sequence without logical flow

### 4.3.3 Proxy Anchor Requirements

**For [FACTS]:**
- Must include: source/date/confidence basis
- Format: `[FACTS: Based on X dated Y]`
- Prohibited: Ungrounded scores

**For [SYNTH]:**
- Must include: grounding statement
- Format: `[SYNTH: Integrating X sources, Y confidence]`
- Prohibited: Synthetic without basis

---

## 4.4 Integration with Mandatory Lens Protocol

- Minimum 3 lenses per response (Section 1.1.1)
- Logical sequencing required (Section 1.2.1)
- Tag-content alignment mandatory (Section 1.2.2)
- Proxy anchors for FACTS/SYNTH (Section 1.3)

---
