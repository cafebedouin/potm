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
