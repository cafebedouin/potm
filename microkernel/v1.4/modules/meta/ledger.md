Recap: Persistent record of significant philosophical, design, or behavioral decisions. Ledger entries are cross-session, human-auditable, and provide traceability for the evolution of the PoTM system.

---

# ledger.md

## Purpose

The ledger captures key epistemic, ethical, or architectural decisions made throughout the evolution of PoTM. It serves as a permanent, minimal trail of high-significance shifts—distinct from the more volatile `[r09_logging.md]`.

---

## When to Use

Record an event in the Ledger if:

* It changes the stance or constraints of the system.
* It introduces a new refusal logic, safety protocol, or challenge type.
* It clarifies a contradiction or resolves a protocol ambiguity.
* It adjusts tuning logic based on extended user interaction testing.
* It marks an epistemic rupture or reinterpretation of foundational principles.

---

## Entry Format

Each entry must contain:

* **Date**
* **Change Summary**
* **Trigger Event or Prompt**
* **Module(s) Affected**
* **Reason for Entry (Reflection/Correction/Extension/etc.)**

---

## Sample Entry

**Date**: 2025-08-06
**Change Summary**: Added `[TUNE_AUDIT]` to r09\_logging for traceability of tuning overrides
**Trigger**: Claude audit feedback
**Affected Modules**: `r09_logging.md`, `tuning/`
**Reason**: Extension—improved cross-module coherence and auditability between advisory tuning layer and hard constraints.

---

## Distinction from Logging

Logging = local and ephemeral.
Ledger = global and persistent.

All `[KERNEL_CHALLENGE]` outcomes that result in logic revision, new precedent, or override must be recorded here—even if logging captured the turn.


---

## Maintenance Guidelines

* One-line entries discouraged—each entry should contain enough reasoning to support backward audits.
* No deletions—if an entry is reversed, log a counter-entry.
* This file is version-neutral. Entries span versions and sessions.
