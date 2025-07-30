---
title: Weekly Roll-up Checklist
version: 1.0
status: active
type: ops
created: 2025-07-29
updated: 2025-07-29
author: A PoTM Practitioner
tags: [ops, cadence, integrity]
location: core/meta/rollup_checklist.md
---

# Weekly Roll‑up (≈10 min)

1. **Triage Issues**
   - Filter new Issues with label `benefit-signal`.
   - Normalize `practice_id` (use ledger; accept `other:<id>` and note for steward).
   - Apply labels: `needs-normalization`, `guardian` if needed.

2. **Append to Monthly Log**
   - Paste normalized entries into `/core/logs/benefit_signals_YYYY-MM.md`.
   - Keep one entry per signal; privacy scrub if necessary.

3. **Dedupe**
   - Collapse multiple entries by `(practice_id, practitioner, ISO week)`.

4. **Recompute per-practice**
   - `benefit_count_30d`
   - `last_benefit_date`
   - *(optional)* `benefit_intensity_hist_30d` (only if ≥1 signal in 30d)

5. **Update Ledger**
   - Edit `core/meta/ledger.yaml` fields for changed items only.

6. **Notes & Flags**
   - Add quick notes or Guardian flags for anything sensitive.
   - Random audit: read ~1 in 20 entries for plausibility.

> Counts are for screening, not final decisions. Keep it lean.
