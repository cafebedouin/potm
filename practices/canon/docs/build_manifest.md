# BUILD_MANIFEST

Defines which files to include in each build mode.  
Order is explicit. Files not listed here are ignored.

| order | category        | path                                                  | id                                          | notes                               |
| 1     | kernel          | kernel/preamble.md                                           | potm.kernel.preamble.v1                     | Opening frame, CC0 licensed      |
| 2     | kernel          | kernel/entry_gate.md                                         | potm.kernel.entry_gate.v1                   | Entry contract                   |
| 3     | kernel          | kernel/beacons.md                                            | potm.kernel.beacons.v1                      | Core beacons                     |
| 4     | kernel          | kernel/lenses_min.md                                         | potm.kernel.lenses_min.v1                   | Minimal lens set                 |
| 5     | kernel          | kernel/micromoves_min.md                                     | potm.kernel.micromoves_min.v1               | Smallest moves layer             |
| 6     | kernel          | kernel/router_min.md                                         | potm.kernel.router_min.v1                   | Deterministic router             |
| 7     | kernel          | kernel/latency_validator_min.md                              | potm.kernel.latency.validator_min.v1        | Latency contract/validator       |
| 8     | kernel          | kernel/state_min.md                                          | potm.kernel.state_min.v1                    | State model                      |
| 9     | kernel          | kernel/guardian_min.md                                       | potm.kernel.guardian_min.v1                 | Minimal guardian                 |
| 10    | kernel          | kernel/policy_min.md                                         | potm.kernel.policy_min.v1                   | Minimal policy                   |
| 11    | kernel          | kernel/refusal_doctrine.md                                   | potm.kernel.refusal_doctrine.v1             | Refusal conditions and emissions |
| 12    | extended        | extended/adapters/entry_menu_adapter.md                      | potm.adapter.entry_menu.v1_6_dev            | Entry menu adapter               |
| 13    | extended        | extended/adapters/lens_adapter.md                            | potm.adapter.lens.v1_1                      | Lens adapter                     |
| 14    | extended        | extended/adapters/glyph_adapter.md                           | potm.adapter.glyph.v1                       | Glyph adapter                    |
| 15    | extended        | extended/lenses/catalog.v1.json                              | potm.lenses.catalog.v1                      | Lens catalog                     |
| 16    | extended        | extended/lenses/compounds/creative/compound.manifest.json    | potm.ex.lenses.compound.creative.v1         | Creative lens compound           |
| 17    | extended        | extended/lenses/compounds/decision/compound.manifest.json    | potm.ex.lenses.compound.decision.v1         | Decision lens compound           |
| 18    | extended        | extended/lenses/compounds/externalist/compound.manifest.json | potm.ex.lenses.compound.externalist.v1      | Externalist lens compound        |
| 19    | extended        | extended/lenses/compounds/relational/compound.manifest.json  | potm.ex.lenses.compound.relational.v1       | Relational lens compound         |
| 20    | extended        | extended/lenses/compounds/research/compound.manifest.json    | potm.ex.lenses.compound.research.v1         | Research lens compound           |
| 21    | extended        | extended/lenses/compounds/somatic/compound.manifest.json     | potm.ex.lenses.compound.somatic.v1          | Somatic lens compound            |
| 22    | extended        | extended/lenses/compounds/trickster/compound.manifest.json   | potm.ex.lenses.compound.trickster.v1        | Trickster lens compound          |

