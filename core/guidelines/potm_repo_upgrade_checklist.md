---
title: "PoTM Repo Upgrade Checklist"
version: 1.0
status: stable
type: maintainer_guideline
created: 2025-07-31
tags: [repo hygiene, versioning, promotions, documentation integrity]
---

## 🎯 Purpose

This checklist ensures consistency and traceability when promoting, deprecating, or substantially revising documents in the *Pilates of the Mind* repository. It formalizes the steps to preserve symbolic integrity and maintain clean provenance across time.

---

## ✅ Standard Promotion Pathway  
_From Experimental to Core_

1. **Finalize Content**
   - Confirm conceptual stability, stylistic polish, and PoTM-aligned coherence.

2. **Rename File**
   - Remove version suffix → `name_v0.9.md` → `name.md`

3. **Move to Stable Folder**
   - `/experimental/` → appropriate subfolder under `/core/`, `/frameworks/`, etc.

4. **Update Frontmatter**
   - Set `status: stable`
   - Remove version (or update if retaining `version: 1.0`)
   - Refresh `updated:` timestamp

5. **Archive Prior Canonical (If Applicable)**
   - Rename current canonical → `name_v1.0.md`
   - Move to `/deprecated/` or `core/archive/`

6. **Update Manifest**
   - Add or revise line in `guidelines/00_MANIFEST.md`

7. **Log in Ledger**
   - Add a short entry to current week's `ledger/YYYY-MM-DD.md`
   - Example: _“Promoted `metabolic_membrane_v0.9.md` → `core/metabolic_membrane.md` (2025-07-31)”_

8. **Run Hygiene Check (Optional)**
   - Execute `tools/repo_hygiene_check_stub.py` to validate structure

---

## 🔄 Deprecation Pathway  
_When replacing or retiring an existing file_

1. **Rename Canonical File**
   - Add version suffix → `name.md` → `name_v1.0.md`

2. **Move to Archive**
   - Place in `/deprecated/` or sub-archive folder

3. **Update Frontmatter**
   - Set `status: deprecated`
   - Preserve last `version:` and update `updated:` timestamp

4. **Revise Manifest**
   - Update row in `00_MANIFEST.md` to reflect new location/status

5. **Log in Ledger**
   - Record deprecation with reason if available (e.g. replaced by new model)

---

## 🧪 New Experimental Drafts

1. **Use Proper Naming**
   - `name_v0.X.md` with no missing version number

2. **Place in `/experimental/`**
   - Use clear subfolders (e.g. `/experimental/frameworks/`)

3. **Add Frontmatter**
   - Set `status: experimental`, `version: 0.X`, and full timestamps

4. **Declare Intent (Optional)**
   - Add a short note to the weekly ledger describing the purpose of draft

---

## 📎 Related Documents

- `guidelines/repo_file_conventions_v1.1.md`
- `guidelines/00_MANIFEST.md`
- `ledger/weekly-template.md`
- `tools/repo_hygiene_check_stub.py`

---

By following this checklist, contributors help maintain PoTM’s membrane hygiene—keeping ideas alive, traceable, and structurally trustworthy across their lifecycle.
