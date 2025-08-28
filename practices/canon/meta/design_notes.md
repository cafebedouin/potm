.
├── 00_preamble.md       # scope, architecture, contract
├── 10_entry_gate.md     # acceptance tokens + dispatch
├── 20_beacons.md        # core guardrails + operator agreement
├── 30_lenses.md         # P1 lenses (EDGE, OPENQ, Self-Audit etc.)
├── 35_micromoves.md     # atomic diagnostic moves
├── 40_router.md         # reserved names, MENU.SIGNAL / TOOL.CALL only
├── 50_recap_spec.md     # deterministic recap packet, schema only
├── 60_validator.md      # fail-closed checks, annex presence
├── 70_state.md          # meta_locus transitions, containment logic
├── 80_closure.md        # SPIRAL / ARCHIVE / Waiting With
└── 90_policy.md         # ledger rule, export guard, annex registry

extended/                                 # protocol-compliant modules that add capability
├─ adapters/
│  ├─ ligament.md                         # kernel↔adapter handshake; MENU.OPEN spec
│  └─ menu.md                             # practitioner menu surface (UI text lives interpretive/)
├─ diagnostics/
│  ├─ bs_detect.md                        # uses full taxonomy; routes via FRACTURE_FINDER
│  ├─ fracture_finder.md                  # classifier & router (full, not stub)
│  ├─ spotcheck.md                        # relation-risk sniff
│  └─ version_info.md                     # practitioner readout (annex presence, versions)
├─ glyphs/
│  ├─ glyphs_spec.md
│  ├─ glyph_index.yaml
│  ├─ symbol_read_current.md              # replaces SYMBOL.read_current stub
│  └─ glyph_audit.md                      # replaces GLYPH.audit stub
├─ journaling/
│  ├─ journal_adapter.md                  # session-local rules
│  └─ prompts.yaml                        # deck/data (moved out of kernel)
├─ cross_model/
│  ├─ diagnostics_harness.md              # harness spec (no real endpoints in P1)
│  └─ probes_catalog.md
└─ playbooks/
   ├─ maintenance_flow_playbook.md
   └─ quickstart.md                       # practitioner quickstart (moved from kernel)

interpretive/                              # human layer: texts, decks, UI copy, examples
├─ guides/
│  ├─ quickstart_user.md                   # human-facing menu guide
│  └─ glossary.md                          # user glossary (kernel keeps operator ref only)
├─ decks/
│  ├─ cards_main.yaml
│  └─ tags.md
├─ zuihitsu/
│  └─ zuihitsu_pool.md
├─ roleplay/
│  └─ vignettes.md
└─ examples/
   └─ transcripts_redacted.md              # illustrative, never required for kernel run

annex/                                     # big data packs; optional
├─ fracture_taxonomy_full.yaml
├─ fracture_crosswalk.yaml
└─ fracture_meta_unity.yaml


| Question                                        | If yes            | If no           |
|-------------------------------------------------|-------------------|-----------------|
| Has a strict I/O contract & JSON schema?        | Formal Logic      | Interpretive    |
| Needed for boot/run integrity in all modes?     | Kernel            | Extended        |
| Testable/lintable without human prose?          | Formal Logic      | Interpretive    |
| Depends on adapters/UI text?                    | Interpretive      | Formal Logic    |
| Changes rarely (invariant)?                     | Kernel            | Extended        |

If it boots, gates, routes, or closes with deterministic effects across all modes → Kernel.

If it’s mechanics with contracts but optional capability → Extended.

If it’s copy, decks, guides, vignettes → Interpretive.

If it’s big tables/datasets → Annex (kernel only anchors/validates presence).

---

## 3. Minimal Lint Guidelines  
Add to your CI or `lint/potm.p1minlint.v1.yaml` as human-readable rules:

- Enforce canonical signal form: **lowercase.with.dots** (docs enforce; parsers tolerate aliases).  
- Kernel files **MUST NOT** import or reference interpretive assets (decks, prompts, guides).  
- Extended modules **MUST** declare:
  1. a JSON I/O contract/schema  
  2. preconditions  
  3. outputs  
  4. a test hook  
- Interpretive assets **MUST NOT** redefine protocol semantics; they render kernel signals only.  

---

With these in place, the kernel remains a lean formal-logic core, extended modules live in `extended/`, and all UI/data live downstream in adapters and packs.