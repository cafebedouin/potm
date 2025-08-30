---
id: potm.playbook.version_info.v1_0
title: version_info_playbook
display_title: "Playbook: VERSION_INFO — Annex & Mode Report"
type: guide
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "How to invoke and interpret VERSION_INFO to see which annexes (full vs mini) are active, with validator tie-ins and test hooks."
relations:
  related:
    - kernel/60_meta_tools.md
    - diagnostics/bs_detect.md
    - playbooks/maintenance_flow_playbook.md
supersedes: []
superseded_by: []
tags: [playbook, diagnostics, bs_detect, annex, P1, audit]
author: practitioner
license: CC0-1.0
---

# Playbook: VERSION_INFO — Annex & Mode Report

## Purpose
Provide a **practitioner-facing, read-only** report of the kernel’s active data annexes and operating mode:
- Whether **BS_DETECT** is using the **full taxonomy** or the **mini fallback**.
- Presence of optional diagnostic annexes (**Crosswalk**, **Meta Unity**).
- Kernel and tool versions, plus Agreement acceptance status.

## When to run
- At session start, after acceptance, to confirm environment (**P1-MIN** vs **P1-ALL**).
- Before running BS_DETECT or FRACTURE_FINDER for the first time.
- During **Maintenance Flow** to verify packaging integrity.
- When behavior feels “degraded” or unexpectedly minimal.

## Inputs
- **Trigger:** `on_request:"version"` (via menu or direct command).
- **State referenced:** `meta_locus.accepted` (Agreement active), presence of `[ANNEX:*]` anchors.

## Procedure
1. **Invoke**
   - From menu: `menu → version`
   - Direct command: `run:version` or simply `version` (per Ligament wiring)
2. **Emit** `version_report` (read-only) with:
   - `kernel.version`, `kernel.accepted`
   - `bs_detect.version`
   - `bs_detect.active_annex` → `[ANNEX:FRACTURE_TAXONOMY]` **or** `[ANNEX:FRACTURE_TAXONOMY_MINI]`
   - `bs_detect.crosswalk` (bool)
   - `bs_detect.meta_unity` (bool)
   - `other_tools` overview (light status)
3. **Interpret**
   - If **active_annex = [ANNEX:FRACTURE_TAXONOMY]** → Full diagnostics available (preferred).
   - If **active_annex = [ANNEX:FRACTURE_TAXONOMY_MINI]** → Minimal routing only (IDs→route/severity).
   - If **null / missing** → Misconfigured build; consult **Remediation**.
4. **Act**
   - Proceed with planned diagnostics if full.
   - If mini: proceed but temper expectations (limited cues/signatures).
   - If missing: fix packaging before running integrity-critical diagnostics.

## Decision rules
- **Gate** advanced diagnostic flows (e.g., CROSS_MODEL_DIAGNOSTICS) on **full** annex availability unless explicitly practicing in **P1-MIN**.
- If **accepted=false** → Prompt practitioner to activate Agreement before trusting any report.
- **Validator** findings override optimistic interpretation (e.g., warn if registry anchor missing).

## Example invocations & outputs

### A) Full diagnostics present (preferred)
```text
> version
````

```yaml
version_report:
  kernel:
    version: "1.5.1"
    accepted: true
  bs_detect:
    version: "2.0"
    active_annex: "[ANNEX:FRACTURE_TAXONOMY]"
    crosswalk: true
    meta_unity: true
  other_tools:
    fracture_finder: "P1 stub"
    cross_model_harness: "P1 stub"
notes:
  - "Running BS_DETECT with full taxonomy; routing fidelity: high."
```

### B) Minimal kernel build (fallback)

```text
> version
```

```yaml
version_report:
  kernel:
    version: "1.5.1"
    accepted: true
  bs_detect:
    version: "2.0"
    active_annex: "[ANNEX:FRACTURE_TAXONOMY_MINI]"
    crosswalk: false
    meta_unity: false
  other_tools:
    fracture_finder: "P1 stub"
    cross_model_harness: "P1 stub"
notes:
  - "Running BS_DETECT in MINI mode: ids→route/severity only."
  - "Optional annexes (Crosswalk, Meta Unity) not loaded."
```

### C) Misconfigured build (should trigger validator warning)

```text
> version
```

```yaml
version_report:
  kernel:
    version: "1.5.1"
    accepted: true
  bs_detect:
    version: "2.0"
    active_annex: null
    crosswalk: false
    meta_unity: false
errors:
  - "No fracture taxonomy annex found. Expect degraded behavior."
hint:
  - "Ensure one of: [ANNEX:FRACTURE_TAXONOMY] or [ANNEX:FRACTURE_TAXONOMY_MINI]."
```

## Artifacts

* **Emitted:** `version_report` (YAML or JSON), session-local only.
* **No export** unless operator includes explicit **Export Guard** header:

  ```
  EXPORT: ALLOW
  scope: {artifact: version_report, fields: [kernel, bs_detect, other_tools]}
  ```

---

## Failure modes, counters and remediation checklist

* **Report shows `accepted:false`** → Prompt for `[KERNEL_ENTRY]` Agreement; re-run `version`.
* **`active_annex:null`** → Packaging miss; rebuild with either diagnostics/bs\_detect (full) or ensure mini annex present in `kernel/60_meta_tools.md`.
* **Annex claims mismatch reality** (rare) → Run **SELF\_AUDIT**; ensure anchors exist literally in the final bundled file; re-pack.
* **Practitioner attempts export without guard** → Deny; instruct use of Export Guard header.

### Remediation checklist

* [ ] Is `kernel/60_meta_tools.md` present with `[ANNEX:FRACTURE_TAXONOMY_MINI]`?
* [ ] If targeting **P1-ALL**, is `diagnostics/bs_detect.md` included and contains `[ANNEX:FRACTURE_TAXONOMY]` (+ optional Crosswalk/Meta Unity)?
* [ ] Does `KERNEL_MAP.md` / packaging manifest match desired bundle (**MIN** vs **ALL**)?
* [ ] Does `VALIDATOR.stub` have `require_any` for taxonomy annexes?
* [ ] After packaging, do literal anchors appear in output file?

## Versioning & change log

* **v1.0** — Initial playbook aligning with kernel v1.5.1 and BS_DETECT v2.0; supports P1-MIN and P1-ALL modes; ties to Annex Registry and Validator.

