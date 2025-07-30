---
title: "Ledger Scope"
version: "v1.0"
status: "reference"
type: "meta"
last_updated: "2025-07-30"
---
### Scope (ledger/)
- Instantiated, dated summaries only (no templates).
- Reads from `logs/` and `tracking/`; does not store raw entries.

### Cadence
- Weekly summary due by Tuesday 12:00 America/Chicago.
- Monthly consolidation on the first of the month.

### Naming
- Folder per year; file per week:
  - `/ledger/YYYY/YYYY-MM-DD-weekly.md`  (use Monday of the week as `week_of`)
