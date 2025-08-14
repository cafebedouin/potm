# Pilates of the Mind — Canonical Ledger Example
# Single source of truth for item status. Keep terse; use pointers for details.

items:
  - id: axioms_v1
    title: PoTM Axioms (Care, Epistemic Integrity, Utility-in-Practice)
    path: core/axioms/axioms_v1.0.md
    type: meta
    status: core
    survivorship: 2x
    origin: coreline
    created: 2025-07-01
    updated: 2025-07-21
    last_benefit_date: 2025-07-27
    benefit_count_30d: 9
    guardian_flags: none
    risk_notes: ""
    evidence:
      - core/logs/benefit_signals_2025-07.md#axioms
    owner: steward
    license: CC-BY-SA-4.0
    tags: [kernel, governance]

  - id: open_portal_mode
    title: Open Portal Mode
    path: core/docs/open_portal_mode_v1.0.md
    type: mode
    status: core
    survivorship: 2x
    origin: coreline
    created: 2025-07-29
    updated: 2025-07-29
    last_benefit_date: 2025-07-29
    benefit_count_30d: 6
    guardian_flags: none
    risk_notes: "Label outputs; no auto-integration."
    evidence:
      - field_artifacts/open_portal/breath_glyph_encounter_bundle_v1.0.md
    owner: steward
    license: CC-BY-SA-4.0
    tags: [aperture, contribution]

  - id: modulatory_breath_spiral
    title: Modulatory Breath Spiral – 🜁🜂🜄
    path: practices/somatic/modulatory_breath_spiral_v1.0.md
    type: practice
    status: candidate
    survivorship: 2x
    origin: open_portal
    created: 2025-07-29
    updated: 2025-07-29
    last_benefit_date: 2025-07-29
    benefit_count_30d: 4
    guardian_flags: mitigated
    risk_notes: "Liminal breathwork; prefer Containment alternative when destabilized."
    evidence:
      - field_artifacts/open_portal/claude_breath_spiral_witnessing_v1.0.md
      - field_artifacts/open_portal/perplexity_breath_glyph_encounter_v1.0.md
      - practices/symbolic/glyph_tracing_ritual_triplet_v1.0.md
    owner: steward
    license: CC-BY-SA-4.0
    tags: [breathwork, spiral, symbolic]

  - id: glyph_tracing_ritual_triplet
    title: Glyph Tracing Ritual – 🜁🜂🜄
    path: practices/symbolic/glyph_tracing_ritual_triplet_v1.0.md
    type: practice
    status: experimental
    survivorship: 1x
    origin: open_portal
    created: 2025-07-29
    updated: 2025-07-29
    last_benefit_date: 2025-07-29
    benefit_count_30d: 2
    guardian_flags: none
    risk_notes: ""
    evidence:
      - field_artifacts/open_portal/claude_breath_spiral_witnessing_v1.0.md
    owner: steward
    license: CC-BY-SA-4.0
    tags: [symbolic, tracing]
