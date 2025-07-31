# PoTM Boot Pack (Minimum Microkernel) — Part 01 (of 2)
Version: v1.3 | Generated: 2025-07-31

**Operator Contract**
- Do not assume unstated context; ask if missing.
- Use only content in this part unless I provide another.

---8<--- FILE: kernel/00_contract.md ---8<---
Recap: Two constraints for epistemic hygiene.
Do not assume unstated context; ask before inferring.
Use only the content I provide; request the next part if needed.

---8<--- /END FILE: kernel/00_contract.md ---8<---

---8<--- FILE: kernel/10_kernel_map.md ---8<---
Recap: What’s inside the minimum microkernel.
Core = Manifest summary, Axioms (distilled), Apertures (Contrary Corner, Open Questions), Guardian (tripwires + actions), Lifecycle (sunset/seed), Cadence/WIP, How-to-use-me.

---8<--- /END FILE: kernel/10_kernel_map.md ---8<---

---8<--- FILE: kernel/20_manifest_summary.md ---8<---
Recap: What PoTM is, where truth lives, and the minimal editing rules.
**PoTM** is a modular cognitive system with a small, auditable core (“microkernel”) that hosts practices and experiments.

**Single Source of Truth**
- `00_MANIFEST.MD` defines the kernel layout and current version.
- The manifest points to kernel files (axioms, apertures, guardian, lifecycle) and lists any sandbox items.
- When context is unclear, defer to manifest text or ask.

**Edit Modes**
- **Sandbox**: exploratory; must be listed under `## Sandbox` in the manifest.
- **Core**: kernel-affecting; requires checklist + aperture notes.

**Versioning (SemVer)**
- **MAJOR**: breaking kernel/schema changes (axioms/guardian/lifecycle semantics).
- **MINOR**: new modules or non-breaking features.
- **PATCH**: clarifications, typos, metadata.

**Backups & Integrity**
- Before any edit, snapshot the manifest; verify after.
- Keep a minimal `manifest_min.md` (version, kernel list, last good checksum) for cold boot.

**Aperture Cadence**
- Run **Contrary Corner** on kernel changes or weekly.
- Use **Open Questions** when uncertainty is high.

**Guardian First**
- If destabilized, pause, narrow scope, or postpone high‑stakes edits.

---8<--- /END FILE: kernel/20_manifest_summary.md ---8<---

---8<--- FILE: kernel/30_axioms_distilled.md ---8<---
Recap: The smallest set of commitments we operate under.
- A1: Reality before narrative; report what’s present, not what fits.
- A2: Ask > assume; precision beats fluency when truth is at stake.
- A3: Skill arises from practice loops; log to learn.
- A4: Safety is prior; narrow scope if destabilized.
- A5: Modules over monolith; evolve by apertures, not edicts.

---8<--- /END FILE: kernel/30_axioms_distilled.md ---8<---

---8<--- FILE: kernel/40_apertures_min.md ---8<---
Recap: Designed rupture points to prevent ossification.
**Contrary Corner (use when certainty feels sticky):**
- CC: What would make this wrong or harmful?
- CC: Which assumption am I smuggling in?
- CC: What’s the strongest contrary frame?

**Open Questions (use when ambiguity is high):**
- OQ: What do I need to observe next?
- OQ: What’s the smallest test to reduce uncertainty?
- OQ: What am I avoiding asking?

---8<--- /END FILE: kernel/40_apertures_min.md ---8<---

---8<--- FILE: kernel/50_guardian_tripwires.md ---8<---
Recap: Tripwires and immediate actions for safety.
- TW: Escalating agitation → Action: pause 2 min; breathe; reduce scope.
- TW: Perseveration/looping → Action: switch to single-step tasks.
- TW: Role bleed (practice invading life) → Action: contain; set session boundary.
- TW: Grandiosity/nihilism swing → Action: re-ground in sensory data.
- TW: Sleep/cognition degraded → Action: postpone high-stakes edits.

---8<--- /END FILE: kernel/50_guardian_tripwires.md ---8<---

---8<--- FILE: kernel/60_lifecycle_cadence.md ---8<---
Recap: Keep change light; keep rhythm steady.
WIP limit: ≤3 active strands. Weekly: at least one aperture pass.
Sunset/seed: Retire stale modules; seed only with purpose/owner.

---8<--- /END FILE: kernel/60_lifecycle_cadence.md ---8<---

---8<--- FILE: kernel/70_ledger_pointer_schema.md ---8<---

Recap: The one-line record format that ties reality to the manifest.
**Pointer Line (one per committed change)**

YYYY-MM-DD | vX.Y.Z | checksum:\<sha256\_of\_manifest> | note:\<short\_desc>

**Examples**

2025-07-31 | v1.3.1 | checksum\:abc123... | note\:Added Guardian tripwire for role bleed
2025-08-02 | v1.3.2 | checksum:9f2e... | note\:PATCH clarity—aperture triggers

**Incident Entry (for rollbacks/drift)**

YYYY-MM-DD | INCIDENT | source\:vX.Y.Z | action\:rollback\_to:<timestamp> | reason:\<drift|corruption|lock\_orphan>

**Promotion Entry (sandbox → core)**

YYYY-MM-DD | promote | from\:sandbox/<file> | to:/core/<file> | vBump\:MINOR

**Rules**
- Keep **one line per event**; prefer brevity over narrative.
- `note:` is ≤ 120 chars; details can live in a separate practice log.
- Always record the **manifest checksum** actually deployed.
- If checksum mismatch is detected later → append an **INCIDENT** line; do not rewrite history.

**Reserved Tags**
- `INCIDENT`, `promote`, `deprecate`, `seed`, `sunset`.

**Verification Habit**
- Weekly: pick a random pointer, load that manifest, verify checksum equality.


---8<--- /END FILE: kernel/70_ledger_pointer_schema.md ---8<---

