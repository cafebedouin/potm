---
id: potm.guide.general.potm_repo_upgrade_checklist.v1_1
title: PoTM Repo Upgrade Checklist
type: maintainer_guideline
status: stable
version: 1.1
stability: core
relations:
  relation_to_agent_protocol: none
  supersedes: [potm.guide.general.potm_repo_upgrade_checklist.v1]
  superseded_by: []
interfaces: []
applicability: [P0]
intensity: gentle
preconditions: []
outputs: []
cadence: []
entry_cues: []
safety_notes: []
tags: [repo hygiene, versioning, promotions, documentation integrity, breaking changes]
author: practitioner + models
license: CC0-1.0
last_updated: '2025-08-08'
---

## 🎯 Purpose

Ensure consistency and traceability when promoting, deprecating, or substantially revising documents in the *Pilates of the Mind* repository.  
Applies to **all zones** (`core/`, `meta/`, `experimental/`, `deprecated/`).

---

## ✅ Standard Promotion Pathway — *From Experimental to Stable/Core*

1) **Finalize content**  
   Conceptually stable, PoTM-aligned, minimal fluff.

2) **Rename file**  
   `name_v0.9.md` → `name.md` (no version suffix in active core/docs).

3) **Move to stable folder**  
   `/experimental/...` → appropriate subfolder in `/core/...` (or `/meta/...` if it’s meta).

4) **Update front-matter**  
   - `status: stable`  
   - keep/adjust `version:` (e.g., `1.0`)  
   - refresh `last_updated:` (or `updated:` if that’s your field)

5) **Archive prior canonical (only if breaking)**  
   - Move the *last pre-breaking* version to `/deprecated/` as `name_vX.Y.md`.  
   - Do **not** archive every minor edit—git history and tags handle that.

6) **Update manifest**  
   - Edit `core/docs/onboarding/00_MANIFEST.md` to reflect the promotion.

7) **Log in ledger**  
   - Add a line to `templates/ledger_weekly.md` (then copy into the current week’s ledger if you keep one), e.g.:  
     _Promoted `metabolic_membrane_v0.9.md` → `core/metabolic_membrane.md` (2025-08-08)._

8) **Sync counterparts (if any)**  
   - If there’s an agent **and** practitioner file, update `relations.*` both ways.

9) **Run hygiene checks (optional)**  
   - Normalize FM: `./scripts/upgrade_front_matter.py "core/**/*.md" "docs/**/*.md" --write`  
   - Rebuild indexes: `./scripts/build_indexes.py --write core docs`

---

## 🔄 Deprecation Pathway — *When replacing or retiring a file*

1) **Version the canonical file**  
   `name.md` → `name_vX.Y.md`

2) **Move to archive**  
   `/deprecated/...` (mirror the original substructure if useful)

3) **Update front-matter**  
   - `status: deprecated`  
   - keep `version:`; update `last_updated:`  
   - add `relations.superseded_by: [<new_id>]` (if successor exists)  
   - add brief `archived_reason:` (1 line)

4) **Revise manifest**  
   - Update `core/docs/onboarding/00_MANIFEST.md` with new location/status.

5) **Log in ledger**  
   - Short note with reason (e.g., “replaced by profile-based user model”).

---

## 🧪 New Experimental Drafts

1) **Name it**  
   `name_v0.X.md` (no gaps in 0.X sequence)

2) **Place it**  
   `/experimental/<category>/...`

3) **Front-matter**  
   `status: experimental`, `version: 0.X`, `last_updated:` set

4) **(Optional) Declare intent**  
   One-liner in the weekly ledger template.

---

## 📎 Related (actual files)

- `meta/front_matter_schema_v0.1.md`  
- `core/guidelines/potm_file_naming_versioning_conventions.md`  
- `core/docs/onboarding/00_MANIFEST.md`  
- `templates/ledger_weekly.md`  
- `scripts/upgrade_front_matter.py`  
- `scripts/build_indexes.py`  
- `core/tools/benefit_signal_lint.md`

---

By following this checklist, contributors keep PoTM’s membrane clean: **core stays canonical**, **experimental stays fertile**, and history remains **traceable** without hoarding every change.
