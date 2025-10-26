Here is a complete `metadata_conventions.md` document, ready for drop-in at:

```bash
core/guidelines/metadata_conventions.md
```

---

````markdown
---
title: "Metadata Conventions"
version: 1.0
status: guideline
type: documentation_standard
created: 2025-08-01
updated: 2025-08-01
author: Pal + Interlocutor
tags: [metadata, conventions, hygiene, forward-only, scaffolding]
sandbox: false
epistemic_scope: bootframe
sunset: null
supersedes: null
replaced_by: null
audit_required: false
guardian_gate: false
context_source: Repo-wide hygiene practice (v2025.08)
---

## 1 · Purpose

This document defines the **metadata conventions** for all structured documents in the Pilates of the Mind (PoTM) repository.  
Consistent metadata enhances:

- AI interpretability  
- Lifecycle tracking  
- Auditable protocol hygiene  
- Modular integration and retirement  
- Human-AI collaboration at scale

---

## 2 · Format Requirements

All files should begin with a **YAML frontmatter block** using triple-dash (`---`) delimiters:

```yaml
---
title: "..."
version: 0.1
status: experimental
type: protocol
created: 2025-08-01
...
---
````

This metadata block is required for all:

* Protocols
* Rituals
* Logs
* Modules
* Appendices
* Framework elements
* Peer review documents

---

## 3 · Standard Fields

| Field     | Description                                                                        |
| --------- | ---------------------------------------------------------------------------------- |
| `title`   | Human-readable title (may differ from filename)                                    |
| `version` | Follows semver logic (e.g., 0.1 for drafts, 1.0 for stable)                        |
| `status`  | One of: `core`, `experimental`, `deprecated`, `draft`, `archived`                  |
| `type`    | Function of the document: `protocol`, `ritual`, `log`, `index`, `diagnostic`, etc. |
| `created` | Date first committed                                                               |
| `updated` | Most recent revision date (optional unless version bump)                           |
| `author`  | Human or AI authorship attribution                                                 |
| `tags`    | Topical or functional tags (free-form, hyphenated preferred)                       |

---

## 4 · Extended AI-Oriented Metadata

These fields support machine interpretation, safety routing, and automated lifecycle tooling.

| Field             | Purpose                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------- |
| `sandbox`         | `true` if document is safe for experimental mutation, trickster mode, or open-ended play |
| `epistemic_scope` | One of: `bootframe`, `archive_free`, `unconstrained` — defines knowledge boundary        |
| `sunset`          | Soft expiration or review date                                                           |
| `supersedes`      | Filename this one replaces (if applicable)                                               |
| `replaced_by`     | Successor filename if this doc is deprecated                                             |
| `audit_required`  | `true` if it should undergo regular epistemic integrity reviews                          |
| `guardian_gate`   | `true` if Guardian Subsystem must evaluate conditions before use                         |
| `context_source`  | Optional provenance hint (e.g. "Gemini Reflection", "Disorientation Drill 3")            |

---

## 5 · Forward-Only Metadata Principle

> **“Always forward.”**
> Do not retroactively backfill metadata into legacy files unless they are being revised for another purpose.

This principle preserves cognitive focus, respects document evolution, and avoids historical tampering.

* Old documents reflect the standards of their time
* New documents adopt current schemas automatically
* Hygiene is maintained *at the level of forward movement*, not repair

---

## 6 · Templates

See:

* [`templates/frontmatter_extended_template.md`](../../templates/frontmatter_extended_template.md) — for full metadata block
* [`potm_file_naming_versioning_conventions.md`](potm_file_naming_versioning_conventions.md) — for filename/version alignment

---

## 7 · Enforcement & Style

PoTM does not currently lint for metadata violations, but a future tool (`metadata_lint.md`) may be developed to support:

* Missing fields
* Deprecated statuses
* Invalid sunset windows
* Guardian flags without gate logic

For now, **human discipline + template use is sufficient**.

---

## 8 · Example

```yaml
---
title: "Lattice-Breaking Rituals"
version: 1.0
status: core
type: meta_protocol
created: 2025-07-28
updated: 2025-08-01
author: Pal + Interlocutor
tags: [rupture, ritual, generativity, override, safety, Don Joyce]
sandbox: false
epistemic_scope: bootframe
sunset: null
supersedes: lattice_breaking_rituals_v0.1.md
replaced_by: null
audit_required: false
guardian_gate: false
context_source: Claude-Gemini Convergence Series
---
```

---

## 9 · Future Directions

* Linting / AI metadata validators
* Auto-sunset reminders
* Metadata change visual diffing in version rollups
* Integration with Ledger system and file maturity indexes

---

> Metadata is infrastructure for discernment.
> If the body of the document speaks, metadata is its fingerprint.

```

---
