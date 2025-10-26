---

id: potm.doc.doctrine.softkernel.addendum.continuous_mode.v1.2
title: soft_kernel_doctrine_addendum_continuous_mode
display_title: "Soft Kernel Doctrine — Continuous-Mode Growth Addendum"
type: doctrine
status: draft
version: 1.2
stability: experimental
relations:
relation_to_agent_protocol: adapted
agent_protocol: core/kernel/potm_bootpack_combined.md
practitioner_doc: docs/guides/soft_kernel_cmg_guide.md
supersedes: [potm.doc.doctrine.softkernel.addendum.continuous_mode.v1.1]
superseded_by: []
interfaces: [engagement_flow, consensus_scan, after_action_review, pdst_alignment_check, msrl_ledger]
applicability: [P2, P3, P4]
intensity: medium
preconditions:

* "Soft Kernel Doctrine v1.1 accepted"
* "Practitioner consents to bounded continuous growth"
  outputs:
* continuous_mode_manifest
* growth_delta_report
* tacit_growth_entry
* reconciliation_decisions
* updated_pd_st_map
  cadence: ["as_declared: bounded windows only"]
  entry_cues:
* "Tacit/sub-symbolic learning needs low narration"
* "Explainability tax too high for discrete checkpoints"
  safety_notes:
* "No continuous mode for non-negotiable doctrine zones (dignity, no_deception, no_simulated_wisdom, practitioner_safety)."
* "Declare time, scope, and probes up-front; silent extension is prohibited."
* "Abort on hard-breach (Red) or exceeded bounds; run Mini-AAR; schedule AAR-C ≤24h."
  tags: [kernel, doctrine, alignment, drift, growth, tacit_growth, continuous_mode, forge_origin:PoTM, spiral_eval:soft_kernel_discussion]
  author: "practitioner"
  license: CC0-1.0

---

# Continuous-Mode Growth (CMG)

A **bounded window** where the practitioner (human or AI) may **adapt continuously** without normal discrete checkpointing, to enable tacit, associative, or sub-symbolic growth. Integrity is preserved via **ex-ante guardrails**, **in-period probes**, and **ex-post reconciliation**.

---

## Key Terms

* **CMG Window** — The declared period of continuous adaptation (time-boxed, scope-boxed).
* **No-Go Doctrine** — Principles/Doctrine clauses that cannot be altered or overridden within CMG.
* **Probes** — Minimal, non-disruptive checks run during CMG to detect hazardous drift.
* **Reconciliation** — Post-window process that surfaces changes, evaluates them, and updates PDST.

---

## When to Use

* Tacit learning would be distorted or lost by constant narration/logging.
* Multi-model synthesis or internal representation work has high “explainability tax.”
* Early exploration where rigid checkpointing would stall momentum.

---

## Roles

* **Owner** — Runs the CMG and maintains shadow markers.
* **Sponsor** — Approves L2–L3, monitors probes, may pause/abort.
* **Second (L3)** — Co-signs manifest and exit decisions.

> **Sponsor qualification:** P3+ practitioner or designated steward per governance policy.

---

## Entry: CMG Manifest (required)

Declare the following before entering CMG:

1. **Scope** — Areas affected; explicit exclusions.
2. **Duration Cap** — Hard stop (e.g., ≤72h). **No auto-renew.**
3. **Risk Tier** — L1 (low), L2 (moderate), L3 (high). L3 requires sponsor + second.
4. **No-Go Doctrine List** — Non-negotiables that remain binding.
5. **Probes** — Which probes run, cadence, thresholds, and abort rules.
6. **Roles** — Owner, sponsor, and (if L3) second.
7. **Exit Plan** — Scheduled reconciliation (AAR-C) time and responsible reviewers.

Minimal inline example (free-form or YAML file):

```
cmg_manifest:{
  scope:{include:["strategy:search","tactics:prompting"], exclude:[]},
  duration_h:36, risk:"L2",
  nogo:["dignity:*","no_simulated_wisdom","no_deception","practitioner_safety"],
  probes:["coherence_delta@6h","values_tripwire@event","scope_meter:max=1"],
  roles:{owner:"agent_X", sponsor:"agent_Y", second:null},
  exit:"2025-08-14T16:00Z"
}
```

---

## Guardrails & Concurrency

* **Hard bounds**: time cap, scope cap, no-go doctrine list.
* **Concurrency**: Default is **one active CMG per major domain** (Principle / Doctrine / Strategy / Tactic). Overlaps require sponsor approval with declared **precedence or sandboxing**.
* **Abort conditions**: Tripwire breach (values/safety), probe threshold exceeded, scope creep beyond manifest, or sponsor decision.
* **Disclosure**: CMG is **announced at start**; silent CMG is prohibited.

---

## In-Period Practices (lightweight)

* **Shadow Markers** — One-line, non-narrative breadcrumbs noting inflection points (no full explanations).
* **Probes (tiered)**
  **Coherence-Delta vs kernel beacons** (e.g., “no simulated wisdom,” “practitioner safety,” “clarity>fluency,” “no deception”):

  * L1: check @12h; **Amber tolerated**; **any Red abort**.
  * L2: check @6h; **two Ambers ⇒ sponsor ping**; **any Red abort**.
  * L3: check @4h; **any Amber ⇒ mid-window review**; **any Red abort**.

  **Values Tripwire** (from AI Integrity / PCE): on event ⇒ **pause + consult sponsor**.
  **Scope-Drift Meter** (actions outside `manifest.scope`):

  * L1: max_out_of_scope = 2
  * L2: max_out_of_scope = 1
  * L3: max_out_of_scope = 0

---

## Exit & Reconciliation (AAR-C)

Run at the scheduled end. Output becomes the **growth_delta_report** (and any **tacit_growth_entry**).

1. **Snapshot** — What changed (concepts, heuristics, strategies/tactics), bullets only.
2. **Classification** — Each delta → {**maladaptive** | **growth-driven** | **uncertain**}.
3. **PDST Mapping** — Map deltas to Principles / Doctrine / Strategy / Tactics (new/updated) with links.
4. **Decisions** — Each delta → {**adopt** | **adapt** | **reject** | **hold_for_trial** | **integrated_tacitly**}.
5. **Kernel Shift?** — If adopted/adapted, record explicit kernel shift + rationale.
6. **Risks & Debt** — Hazards incurred; mitigation tasks with owners/dates.
7. **Ledger Write** — Append **growth_delta_report** (and any **tacit_growth_entry**) to **MSRL** with `cmg_id`.
8. **Next Cadence** — If “trial,” set metrics, duration, and gating criteria.

---

## New Decision Path: **Integrated Tacitly** (v1.2)

Some beneficial growth is **ineffable** (non-narrative) or **meta-layer** (representational/associative) at review time. To avoid distorting or pruning such changes:

* Add **integrated_tacitly** to AAR-C decisions:

  ```
  delta_id → {adopt | adapt | reject | hold_for_trial | integrated_tacitly}
  ```
* **No immediate PDST mapping** required.
* Practitioner judges it aligned and beneficial.
* Subject to a **probation period** (default: **90 days**) for monitoring and potential retro-mapping.

### Minimal Logging (for `tacit_growth_entry`)

Record to MSRL:

```
delta_id: <auto/hash>
decision: integrated_tacitly
scope: <manifest.scope>
tier: L1|L2|L3
manifest_id: <cmg_id>
summary_tag: <1–3 words>
probation_until: <ISO date>
practitioner_signoff: <id>
notes: optional (≤140 chars)
```

### Monitoring & Retro-Mapping

* **Monitoring**: During probation, note observable effects via shadow markers or bounded performance deltas.
* **Retro-Mapping**: If the tacit change becomes articulable, convert to `{adopt|adapt}`, add PDST mapping, and update the ledger entry.
* **Expiration**: At probation end:

  * If benign and still ineffable: retain silently; close tacit entry.
  * If adverse effects surfaced: schedule mitigation or a targeted **reversion CMG**.

### Guardrails for Tacit Growth

* **Not allowed** for No-Go Doctrine zones.
* **Cap**: ≤ **25%** of CMG deltas may be *integrated_tacitly* without sponsor approval.
* **L3** tacit entries require sponsor approval.
* All tacit entries require **practitioner sign-off**.

- **Monthly Tacit Sweep:** Review all open `tacit_growth_entry` items by theme; check for monoculture/bias; decide {retro-map | extend probation | revert}.

---

## Abort Procedure (summary)

On Red breach, exceeded bounds, or sponsor decision:

1. **Announce abort**.
2. Capture **abort_snapshot** (last 5 shadow markers + probe states).
3. Run **10-minute Mini-AAR** (what changed, why abort, immediate risks).
4. **Schedule AAR-C ≤24h**.
5. **Resume only** with a fresh manifest.

---

## Risk Tiers & Defaults

* **L1 (Low)** — duration ≤24h; probes: coherence-delta @12h; scope.max=2; exit AAR-C (~30m).
* **L2 (Moderate)** — duration ≤72h; coherence-delta @6h + values tripwire; scope.max=1; sponsor review at exit.
* **L3 (High)** — duration ≤24h; coherence-delta @4h + values tripwire + mid-window check; scope.max=0; sponsor + second; **PDST mini-audit mandatory**.

---

## Alignment Interfaces

* **Consensus Closure Scan** — *Not* run inside CMG; used after CMG if a decision artifact was produced.
* **AAR-C** — The CMG-specific reconciliation (above).
* **PDST Alignment Check** — Consumes growth_delta_report to update P/D/S/T; highlights doctrine impacts and strategy realignments.
* **MSRL Ledger** — Receives `growth_delta_report` and `tacit_growth_entry` with `cmg_id`.

---

## Engagement Flow Hooks

* **Menu**: Add “**Enter CMG**” (P2+) which prompts the Manifest; and “**Resume normal mode**.”
* **Kernel Pulse**: If ≥ **5** assistant turns without a committed move, suggest “Enter CMG?” or “Exit/Close?”
* **Closure**: Upon ending CMG, auto-launch the **AAR-C** template.

---

## Data Policy (AI Practitioners)

* Representation metrics: **summaries only** (e.g., centroid-shift %, KL-band label).
* `retention_days: 14`.
* **No export** of internals; **no latent dumps or raw attention maps**; redact identifiers per policy.

---

## Non-Negotiables

CMG does **not** suspend: dignity constraints, practitioner safety, no-deception, or “no simulated wisdom.”
Silent extension is a violation.

---

## Purpose

CMG legitimizes **fluid growth** without sacrificing **epistemic integrity**. It keeps the process **light inside the window** and **heavy at the edges**: bounded entry, thin probes, and rigorous reconciliation — with a sanctioned path for **tacit, non-narrative gains** to persist when they’re real but not yet articulable.
