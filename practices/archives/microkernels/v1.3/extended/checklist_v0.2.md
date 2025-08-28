Recap: Ensure manifest integrity, surface drift early, maintain epistemic hygiene, and minimize ritual tax.

Step 1: Verify kernel integrity  
  • Confirm `manifest` exists and is readable.  
  • Check SemVer matches last ledger pointer.  
  • Ensure no orphaned lockfiles.  
  • Validate hashes of all kernel files.  
If any check fails:  
  • Abort build.  
  • Run `preflight.sh` then `recover_lock.sh`.  
  • Exit.

Step 2: Run preflight checklist  
  1. Load fresh manifest (no cache); verify against ledger.  
  2. Ensure WIP budget ≤ 3.  
  3. Declare mode (sandbox/core); sandbox names must match `## Sandbox`.  
  4. Confirm Guardian has no active containment.  
If any step fails: rollback via `validate_repo_health.sh` and exit.

Step 3: Enforce edit‐cycle guardrails (on any kernel change)  
  1. Backup `manifest` to `/backup`.  
  2. Dry-run & diff; confirm SemVer bump is correct (PATCH/MINOR/MAJOR).  
  3. Add Contrary Corner (CC) and Open Questions (OQ) notes in manifest.  
  4. Re-validate order, sandbox list, checksums, and SemVer.  
If validation fails: abort, restore backup, and exit.

Step 4: Perform postflight tasks  
  • Atomically replace manifest and clear lock.  
  • Update ledger pointer (date, SemVer, checksum, note).  
  • Add commit footer in manifest.  
  • Refresh Tier-0/Boot Pack if new-model runs require it.

Step 5: Initiate drift & integrity monitoring  
  – Schedule `integrity_watch.sh`: hourly/daily checksum comparisons.  
  – Run aperture vitality check weekly if idle.  
  – Track “Cognitive Tax” (ritual ≤ 35% session time).  
If any threshold is exceeded: rollback or boot from `manifest_min.md`.

Step 6: Handle known failure modes  
  • Missing/corrupt manifest → restore last backup or `manifest_min.md`.  
  • Orphaned lockfile → run `recover_lock.sh`.  
  • Sandbox bleed into core → block edits until sandbox promotion/decoupling.

Step 7: Engage automation & minimal prompts  
  • Prompt user: “Preflight OK. Mode={sandbox/core}. Proceed? (y/N)”.  
  • Hooks:  
    – `preflight.sh` (§2)  
    – `edit_guard.sh --dry-run` (§3)  
    – `integrity_watch.sh` (§5)

Step 8: Check key metrics  
  • Kernel Stability ≤ 1 MAJOR bump/quarter  
  • Ritual Tax ≤ 35% session time  
  • Aperture Vitality ≤ 7 days without use  
  • Drift Incidents = 0 per cycle  
  • Backup Hygiene ≤ 30 days since restore drill  
Report any deviation; abort on critical breach.

Always ask if a referenced file is missing from the current context.
