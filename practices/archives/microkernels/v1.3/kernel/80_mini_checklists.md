Recap: Minimal, low-tax steps before/after edits and for ongoing hygiene.

## Preflight (before any edit)
1) Fresh-read manifest (no cache); confirm SemVer + checksum.
2) Check WIP ≤ 3 active strands; if >3, queue or sunset.
3) Declare mode: sandbox/core; list sandbox item if sandbox.
4) Guardian scan: any tripwire fired? If yes, pause/narrow scope.
5) Backup manifest (timestamped).
6) Dry-run diff and expected SemVer bump.

## Edit Guardrails (during edit)
1) Keep changes within declared mode.
2) Kernel touch → add **Contrary Corner** + **Open Questions** notes.
3) Validate: section order, sandbox listing, checksums, SemVer.
4) Abort + rollback if validation fails.

## Postflight (after edit)
1) Atomic replace manifest; clear lock.
2) Append **ledger pointer** (date | version | checksum | note).
3) Add commit footer line inside manifest for quick audit.
4) If new models will be used, refresh primer/parts as needed.

## Drift Monitor (scheduled)
1) Compare manifest checksum vs last ledger pointer (daily/hourly).
2) If no aperture fired in 7 days → run a self-challenge (Contrary Corner).
3) Keep ritual tax ≤ 25–35% per session; exceed twice → automate or simplify.
