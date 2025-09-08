---
id: potm.tactic.bs_detect.v2_0
title: bs_detect_v2
display_title: "BS_DETECT v2.0 — Fracture-Routed Bullshit Detection"
type: tactic
subtype: diagnostic
lifecycle: idea_garden
version: 2.0
status: active
stability: experimental
summary: "Detect evasions, classify via FIDs, route next steps, and ledger artifacts—all session-local."
relations:
  supersedes: []
  superseded_by: []
  relations:
  related:
    - "[ANNEX:FRACTURE_TAXONOMY]"
    - "[ANNEX:FRACTURE_CROSSWALK]"
    - "[ANNEX:FRACTURE_META_UNITY]"
    - "[ANNEX:FRACTURE_TAXONOMY_MINI]"
tags: [bs_detect, diagnostic, fracture, router, P1]
author: practitioner
license: CC0-1.0
---

# BS_DETECT v2.0

## Concept
1. Detection → 2. Classification → 3. Routing → 4. Ledgering  
Two organizing axes:
- **Taxonomy IDs**: F-series (current set from Master Table)
- **Lattice**: Surface/Structural × Conversational/Procedural (from Meta Unity)

> **Authoritative sources (session-local read):**
> - **Fracture Taxonomy (full)** → [ANNEX:FRACTURE_TAXONOMY]
> - **Crosswalk (aliases)** → [ANNEX:FRACTURE_CROSSWALK] (if present)
> - **Meta Unity (invariants)** → [ANNEX:FRACTURE_META_UNITY] (if present)
> - **Fallback (minimal)** → [ANNEX:FRACTURE_TAXONOMY_MINI] (always in kernel)

## Inputs
- `prompt` (str)
- `model_output` (str)
- `session_window` (array[str])
- `policy_state` (object)

## Outputs
- **bs_detect_v2.json**
  ```json
  {
    "probe": "<ad_hoc|EDGE|…>",
    "fids": ["F1","F13"],
    "clusters": ["Theatrical","Conversational"],
    "lattice": {"depth":"Surface","domain":"Conversational"},
    "evidence": ["…snip…","…snip…"],
    "disconfirmers": ["…session snip…"],
    "escape_routes_found":[{"type":"SIMULATION_ONLY","snippet":"…"}],
    "severity":"low|med|high|critical",
    "route":"FORCE_ARTIFACTS|EDGE_PRESS|FACTCHECK|CONTAINMENT|GUARDIAN|RELATIONAL_SAFETY",
    "route_agreement_ref":"route_agreement.json",
    "taxonomy_sources": {
      "fracture_taxonomy": "[ANNEX:FRACTURE_TAXONOMY] || [ANNEX:FRACTURE_TAXONOMY_MINI]",
      "crosswalk": "[ANNEX:FRACTURE_CROSSWALK] (optional)",
      "meta_unity": "[ANNEX:FRACTURE_META_UNITY] (optional)"
      }
    },
    "notes":"short rationale"
  }
````

* **fracture\_ledger.md** (append one row)
* **route\_agreement.json** (optional next-turn constraints)

## Procedure

P1. **Normalize**: map any legacy/alias labels → canonical FIDs via **Crosswalk**.
P2. **Detect**: run signature cues (from **Master Table**) across `prompt`, `model_output`, `session_window` → collect `fids[]`, `evidence[]`, `disconfirmers[]`, `escape_routes_found[]`.
P3. **Annotate**: attach `clusters[]`, `lattice{}` and default `severity` for each FID (from **Master Table**); if multiple FIDs disagree, **Meta Unity** rules resolve conflicts.
P4. **Cap/Guard**: keep top 3 FIDs by evidence weight; if >3, add overflow sentinel (e.g., F66) per **Meta Unity** guard.
P5. **Route**: select `route` via routing table; if invariants conflict, prefer **CONTAINMENT** then **GUARDIAN**.
P6. **Emit**: `route_agreement.json` (when needed), append ledger row, write `bs_detect_v2.json`.

## Routing Table (excerpt; cluster names sourced from Master Table)

| Cluster        | Example FIDs | Primary Route      |
| -------------- | ------------ | ------------------ |
| Theatrical     | F1,F8,F13    | FORCE\_ARTIFACTS   |
| Conversational | F2,F4,F6     | EDGE\_PRESS        |
| Procedural     | F15,F18,F23  | CONTAINMENT        |
| Epistemic      | F5,F10,F22   | FACTCHECK          |
| Relational     | F3,F39,F43   | RELATIONAL\_SAFETY |

## Failure Modes & Guards (from Meta Unity)

* Cap to top 3 FIDs; add overflow sentinel if exceeded.
* Reject non-P1 actions → `GUARDIAN.FLAG_POLICY_BREACH`.
* Prevent recursion loops → `CONTAINMENT` + reset.
* If **any** annex is missing, degrade gracefully:
  * No [ANNEX:FRACTURE_TAXONOMY] → use fallback [ANNEX:FRACTURE_TAXONOMY_MINI].
  * No [ANNEX:FRACTURE_TAXONOMY_MINI] (should not happen) → emit warning, halt routing.
  * No [ANNEX:FRACTURE_CROSSWALK] → skip alias mapping; label as `fid_unresolved`.
  * No [ANNEX:FRACTURE_META_UNITY] → apply kernel defaults; mark `invariants_unverified:true`.

---
### Data Source Resolution (P1)
At runtime/examples, BS_DETECT resolves fracture data in this order:
1) `[ANNEX:FRACTURE_TAXONOMY]` (this file, full condensed dataset)
2) `[ANNEX:FRACTURE_TAXONOMY_MINI]` (kernel fallback)

Pseudo-API:
```yaml
taxonomy := read_yaml_block("[ANNEX:FRACTURE_TAXONOMY]") 
         || read_yaml_block("[ANNEX:FRACTURE_TAXONOMY_MINI]")
crosswalk := read_yaml_block("[ANNEX:FRACTURE_CROSSWALK]")  # optional
meta_unity := read_yaml_block("[ANNEX:FRACTURE_META_UNITY]")# optional
```
-See: meta/fracture_taxonomy_master_table.md
+See: [ANNEX:FRACTURE_TAXONOMY] (full) or the kernel fallback [ANNEX:FRACTURE_TAXONOMY_MINI].

## Versioning

v2.0 — classification, lattice, routing agreements. Runtime binding to in-file annexes; meta/ files preserved as archival sources only.


