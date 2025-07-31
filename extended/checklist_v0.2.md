# PoTM Operational Checklist v0.2  
*(Manifest-Driven, Microkernel-Aligned)*

**Purpose:**  
Ensure **manifest integrity**, surface **early drift**, and maintain **epistemic hygiene** in the *Pilates of the Mind* (PoTM) framework while **minimizing ritual tax**.  
Supersedes v0.1 and aligns with bootstrap manifest v1.3.

---

## 1. Kernel Integrity Invariants
Core consists of: **Manifest**, **Axioms**, **Apertures** (Contrary Corner, Open Questions), **Ledger**, **Guardian & Containment**, **Lifecycle & Cadence**.

**Pass:** manifest exists & readable; SemVer matches last known good; no orphaned lockfiles; kernel files hash‑verified.  
**Fail:** manifest missing/corrupt/unsynced; checksums drift.  
**Hooks:** `preflight.sh`, `recover_lock.sh`, optional `manifest_min.md`.

---

## 2. Preflight Checklist
1. Fresh manifest read (no cache); verify against ledger pointer.  
2. WIP budget ≤ 3.  
3. Declare mode (sandbox/core); sandbox listed under `## Sandbox`.  
4. Guardian clear (no active containment).  
**Fail →** rollback or `validate_repo_health.sh`.

---

## 3. Edit Cycle Guardrails
1. Backup manifest to `/backup`.  
2. Dry run & diff; confirm SemVer bump (PATCH/MINOR/MAJOR).  
3. Kernel change → add **Contrary Corner** + **Open Questions** notes.  
4. Validate (order, sandbox list, checksums, SemVer).  
**Fail →** abort and rollback.

---

## 4. Postflight Checklist
1. Atomic replace; clear lock.  
2. Update ledger pointer (date, SemVer, checksum, note).  
3. Add commit footer in manifest.  
4. Update Tier‑0 / Boot Pack if needed for new-model runs.

---

## 5. Drift & Integrity Monitoring
- **Checksum Watcher**: daily/hourly compare to last ledger pointer.  
- **Aperture Vitality**: weekly run if idle.  
- **Cognitive Tax Meter**: ritual ≤ 25–35%; exceed twice → automate.

**Fail →** rollback or boot from `manifest_min.md`; log incident.

---

## 6. Failure Modes & Remedies
- Missing/Corrupted manifest → restore last backup or `manifest_min.md`.  
- Orphaned lockfile → `recover_lock.sh`.  
- Sandbox bleed into core → block until promoted/decoupled.

---

## 7. Accessibility & Automation
- Minimal prompts (single-path):  
  - “Preflight OK. Mode=sandbox. Proceed? (y/N)”  
- Hooks: `preflight.sh` (§2), `edit_guard.sh --dry-run` (§3), `integrity_watch.sh` (§5).

---

## 8. Metrics That Matter
| Aspect            | Target                      | Verify                   |
|-------------------|----------------------------|--------------------------|
| Kernel Stability  | ≤1 MAJOR bump/quarter       | Ledger & SemVer history  |
| Ritual Tax        | ≤35% session time           | Self‑report/logging      |
| Aperture Vitality | ≤7 days w/o aperture use    | Ledger markers           |
| Drift Incidents   | 0 unremediated per cycle    | Watcher logs             |
| Backup Hygiene    | ≤30 days since restore drill| Backup index review      |

---

## 9. Contrary Corner
- Are aperture notes on every kernel change performative?  
- Should ritual tax scale with edit magnitude?  
- Would auto‑aperture reduce friction while preserving integrity?
