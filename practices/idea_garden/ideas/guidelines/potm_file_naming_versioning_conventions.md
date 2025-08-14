---
title: "PoTM File Naming & Versioning Conventions"
version: 1.1
status: stable
type: guideline
created: 2025-07-31
updated: 2025-07-31
tags: [naming, versioning, conventions, repo hygiene, metadata]
---

## 🧭 Purpose

This guideline defines a self-describing naming system for *Pilates of the Mind* (PoTM) documents. It encodes document **maturity**, **version lineage**, and **placement logic** into the filename itself—enabling consistent human usage and automated tooling.

---

## 🧬 Core Naming Pattern

```

{name}\_v{X.Y\[.Z]}.md    → versioned
{name}.md               → canonical

````

- `X.Y[.Z]` follows **semantic versioning** (SemVer) where:
  - `X` = major revision (structural change, meaning shift)
  - `Y` = minor revision (content addition, refinement)
  - `Z` = optional patch/hotfix (typo, metadata, link fix)

---

## 🗂 Placement by Version

| Filename Pattern          | Meaning                    | Folder             | Frontmatter Status   |
|---------------------------|----------------------------|--------------------|----------------------|
| `_vX.Y` where `X` < 1     | Experimental / Draft       | `/experimental/`   | `status: experimental` |
| No version (e.g. `foo.md`)| Canonical Stable Version   | `/core/`, etc.     | `status: stable`     |
| `_vX.Y` where `X` ≥ 1     | Archived / Deprecated      | `/deprecated/`     | `status: deprecated` |

---

## 🧹 Filename Hygiene Rules

- Use **lowercase with underscores**: `snake_case.md`
- Avoid:
  - spaces
  - hyphens (`-`)
  - CamelCase
  - leading/trailing underscores or double underscores (`__foo`)
- Asset files follow similar naming, e.g.:
  - `membrane_illustration_v1.0.png`
  - `signal_log_asset1_v0.2.csv`

---

## 📁 Directory Scoping (Extended Table)

| Domain         | Folder           | Notes                          |
|----------------|------------------|--------------------------------|
| Core ideas     | `/core/`         | Canonical documents            |
| Experiments    | `/experimental/` | Early-stage drafts             |
| Deprecated     | `/deprecated/`   | Superseded or frozen content   |
| Frameworks     | `/frameworks/`   | Conceptual skeletons           |
| Practices      | `/practices/`    | Repeatable actions or drills   |
| Logs           | `/logs/`         | Practice records, journals     |
| Tools          | `/tools/`        | Scripts, checkers, utilities   |
| Meta           | `/meta/`         | Reflections, origin texts      |
| Guidelines     | `/guidelines/`   | Repo usage and governance      |

---

## 🧪 Promotion Lifecycle

```text
/experimental/ → /core/ → /deprecated/
   v0.X             ↥           v1.X+
````

**Checklist for Promotion**:

1. Finalize content → bump version (optional)
2. Rename: remove version suffix → `name.md`
3. Move to appropriate core subfolder
4. Update frontmatter: `status: stable`, bump `updated:`
5. Archive old canonical: `name_v1.0.md` → `/deprecated/`
6. Update:

   * `docs/onboarding/00_MANIFEST.md`
   * `ledger/weekly-entry.md` or equivalent

---

## 📑 Recommended Frontmatter

```yaml
---
title: "Human-Friendly Title"
version: 0.9
status: experimental
type: protocol | drill | framework | ...
created: 2025-07-20
updated: 2025-07-31
tags: [clarity, resilience, diagnostic]
---
```

---

## 🔁 Manifest & Ledger Cross-Reference

* **Manifest**: Tracks current file status, placement, and maturity.
* **Ledger**: Captures file movement or update events (e.g. promotions, refactors).
* **This guideline assumes** all filename version bumps are reflected in both.

---

## 🧰 Future Automation

Suggested tool: `/tools/repo_hygiene_check.py` (or `.R`)

**Features**:

* Validate filename ↔ frontmatter ↔ folder alignment
* Detect misplacements (e.g. `v0.3` in `/core/`)
* Auto-suggest changelog entries
* Highlight stale drafts or silent promotions

---

## 📌 Example Mappings

| Filename                 | Folder           | Status       | Manifest Entry              |
| ------------------------ | ---------------- | ------------ | --------------------------- |
| `membrane_model_v0.3.md` | `/experimental/` | experimental | experimental/frameworks/... |
| `membrane_model.md`      | `/core/`         | stable       | core/frameworks/...         |
| `membrane_model_v1.0.md` | `/deprecated/`   | deprecated   | deprecated/frameworks/...   |

---

## 📎 See Also

* `docs//00_manifest.md`
* `templates/ledger-weekly.md`
* `tools/repo_hygiene_check_stub.py`

---
