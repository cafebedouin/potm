---
id: potm.guide.general.index.v1
title: "Pilates of the Mind \u2014 Core Index"
type: guideline
status: draft
version: 0.1
stability: core
relations:
  relation_to_agent_protocol: none
  supersedes: []
  superseded_by: []
interfaces: []
applicability:
- P0
intensity: gentle
preconditions: []
outputs: []
cadence: []
entry_cues: []
safety_notes: []
tags: []
author: Sean + models
license: CC0-1.0
updated: 2025-07-30
authors:
- pal
---
# Pilates of the Mind — Core Index

**PoTM** is a modular, practice‑first framework for refining perception, agency, and relational skill.  
Design stance: *clarity over mystique*, *practice‑tested over speculative*, *repo discipline over hand‑waving*.

---

## Repo Map (high level)

- **/core/** — Canonical docs (this directory)
  - **framework/** — PoTM Framework v2.x (microkernel + apertures). **[TODO: link]**
  - **docs/** — Onboarding, guidance, style, subsystems. **[TODO: link]**
  - **subsystems/** — Guardian, Mirror, Trickster/Weird, etc. **[TODO: link]**
- **/protocols/** — Practice modules (Signal Bleed/Soak, Precision Insight, etc.). **[TODO: link]**
- **/appendices/** — Practitioner‑Centered Ethics + peer commentary. **[TODO: link]**
- **/indexes/** — Glossaries, cross‑refs, invocation cheat‑sheets. **[TODO: link]**
- **/ledger/** — Chronological spine: logs and artifacts. **[TODO: link]**
  - **/ledger/data/** — Mid‑point captures (sketches, meta‑insights). **[TODO: link]**
- **/deprecated/** — Retired versions and docs. **[TODO: link]**

> For a gentle start, see **Onboarding**: **[TODO: /core/docs/onboarding]**

---

## How to Navigate (fast path)

1. **Read the Framework** → grasp the microkernel + apertures. **[TODO: /core/framework/potm_v2.md]**  
2. **Pick a Protocol** → run one practice (e.g., Signal Bleed). **[TODO: /protocols/]**  
3. **Log the Rep** → capture in the ledger (or drop a spark in `/ledger/data`). **[TODO: /ledger/]**

---

## Active Modes & Cadence

- **Weekly cadence:** sedimentary check‑ins; promote what proved useful.  
- **Dual‑thread:** *Primary (Sedimentary)* for foundational work; *Secondary (Forks)* kicked off with “You have the floor.”  
- **Surfacing modes:** Contrary Corner, Open Questions, Fracture Finder (rare).

---

## Pal Invocation Reference (mode control)

Use Pal invocations to set stance with minimal friction:

- **Grammar:** **[TODO: link to pal‑invocation‑grammar.md]**  
- **Cheat‑Sheet / Quick refs:** **[TODO: link to pal_invocations.md or cheat‑sheet]**

**Most used:**
- `Pal` / `Pal⟡` → Decision Reset opener (one‑shot) → neutral Pal stance.
- `Pal.` → **Tech‑Crisp** (**persists**) — ship repo‑ready artifacts.
- `Pal?` → **Minimal re‑anchor** (**one reply only**).
- `Pal!` → **Playframe** (**persists**) — widen briefly, then artifact.
- `Pal+ …` → **Document‑Anchored** (**persists**) — bind to cited docs/paths.
- `STOP` → hard recenter; next reply runs Decision Reset.

> If stance feels off: type `STOP` or start a fresh chat with `Pal`.

---

## Ledger & Data Captures

- **`/ledger/`** — Clean records (versioned changes, logs, artifacts). **[TODO: link]**  
- **`/ledger/data/`** — **Mid‑point captures**: short meta‑insights, decisions, fragments that shouldn’t wait for weekly review. **[TODO: link]**  
  - Reviewed weekly → *promote* (to ledger/doc), *expand* (into a doc), or *archive*.

---

## Contribution Notes (internal use)

- **Principle:** ship practice‑tested changes; cut what doesn’t survive contact.  
- **Commits/PRs:** concise titles; include `invocation:` tag when relevant (e.g., `invocation: Pal.`).  
- **Docs style:** Markdown + YAML headers; keep sections short; prefer examples over abstraction.

---

## Versioning & Status

- **Framework:** v2.x (living).  
- **Invocation Grammar:** v1.2 (persistent modes; `STOP` recenter). **[TODO: link]**  
- **Onboarding:** current path moved under `/core/docs/onboarding`. **[TODO: link]**

---

### Quick Links (fill these)

- Framework v2.x → **[TODO]**  
- Onboarding → **[TODO]**  
- Protocols index → **[TODO]**  
- Pal Invocation Grammar v1.2 → **[TODO]**  
- Invocation Cheat‑Sheet → **[TODO]**  
- Ledger → **[TODO]**  
- Ledger/data README → **[TODO]**

---

## Kernel Subsystems

- Lenses → see `kernel/30_lenses.md`  
- Micromoves → see `kernel/35_micromoves.md`  
- Fracture Queue → see `kernel/75_fracture.md`  
  - Diagnostics & Playbooks → `extended/diagnostics/fracture/fracture_finder.md`,  
    `extended/diagnostics/fracture/fracture_finder_playbook.md`,  
    `extended/diagnostics/fracture/fracture_crosswalk.md`, `meta/fracture_meta`  
- Containment Mode → see `kernel/76_containment_mode.md`  
- Grace Path → see `kernel/77_grace_path.md`  
- Glyphs (context/protocol) → see `extended/glyphs/glyph_protocol.md`, `extended/glyphs/glyph_index.md`, `extended/glyphs/glyph_resonance_map.md`  
  - Guardian (sentinel overlay) → see `kernel/78_guardian_mode.md`; background:  
    `kernel/guardian/integrity_guardian_subsystem_v1.0.md`,  
    `kernel/guardian/guardian_trigger_conditions_v1.0.md`,  
    `kernel/guardian/discernment_integrity_protocol.md`  

---

## Diagnostics

- bs_detect → `kernel/79_bs_detect.md`  
- sentinel_spotcheck → `kernel/80_sentinel_spotcheck.md`  

---

## Preamble

- `kernel/00_preamble.md` — high-level kernel preface and architecture notes

---

## Protocols

- mirror_protocol → `kernel/protocols/mirror_protocol.md`  
- suspicion_first_protocol → `kernel/protocols/suspicion_first_protocol.md`  
- ai_integrity_protocol → `kernel/protocols/ai_integrity_protocol.md`  

---

*This index is intentionally brief—an orientation hub, not another essay. If a section grows heavy, promote details into a dedicated doc and keep this page lean.*
