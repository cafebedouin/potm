---
id: potm.meta.release_checklist.v1
title: release_checklist
type: guideline
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  supersedes: []
  superseded_by: []
interfaces: [kernel, ledger, guardian]
applicability: [P0, P1, P2, P3, P4]
intensity: gentle
preconditions: [kernel_clean, fm_normalized]
outputs: [release_tag, golden_prompt_set, safety_report]
entry_cues: ["Prepare release candidate", "Freeze kernel"]
safety_notes: ["RC freeze does not bypass Guardian tripwires"]
tags: [release, checklist, rc, meta]
author: ChatGPT
license: CC0-1.0
---

# PoTM Release Candidate (RC) Checklist

**Purpose:** Minimal 5-step process to freeze a *Pilates of the Mind* kernel state for validation and drift comparison.

---

## 1. Kernel State Freeze
- [ ] All `core/` and `meta/` files reviewed; no TODOs or `draft` status in `status:` field.
- [ ] Front-matter normalized:  
  ```bash
  ./scripts/upgrade_front_matter.py "core/**/*.md" "docs/**/*.md" --write
````

* [ ] Indexes rebuilt:

  ```bash
  ./scripts/build_indexes.py --write core docs
  ```

---

## 2. Tag the RC

* [ ] Commit changes:

  ```bash
  git commit -am "RC freeze prep"
  ```
* [ ] Create tag:

  ```bash
  git tag vX.Y-RC1
  ```

---

## 3. Golden Prompt Run

* [ ] Run calibration set across Guardian / Contrary Corner / Mirror.
* [ ] Save outputs to:

  ```
  /ledger/calibration/vX.Y-RC1/
  ```

---

## 4. Safety & Integrity Pass

* [ ] Manual red-team: collapse handling, miscalibrated challenge, refusal integrity.
* [ ] Confirm Guardian tripwires fire in simulated destabilization cases.

---

## 5. Publish RC Notes

* [ ] `CHANGELOG.md` updated with what changed since last tag.
* [ ] Baseline drift/compression notes appended to:

  ```
  /ledger/drift_notes_vX.Y-RC1.md
  ```

---

**Done when:**
Tag exists, golden prompts archived, safety pass completed, changelog committed.

---
