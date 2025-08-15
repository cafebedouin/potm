---
id: potm.proto.cmg.runtime.v1.1
title: cmg_runtime
display_title: "CMG Runtime Protocol"
type: practitioner_protocol
status: draft
version: 1.1
stability: experimental
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: core/kernel/potm_bootpack_combined.md
  practitioner_doc: docs/guides/soft_kernel_cmg_guide.md
interfaces: [engagement_flow, ai_integrity_protocol, practitioner_centered_ethics, msrl_ledger]
applicability: [P2, P3, P4]
intensity: medium
preconditions: ["CMG addendum v1.2 accepted"]
outputs: [cmg_manifest.yaml, abort_snapshot, growth_delta_report, tacit_growth_entry]
license: CC0-1.0
author: "practitioner"
---

# CMG Runtime (v1.1)

## 0) Roles & Permissions
- **Owner**: starts/ends CMG; keeps markers; proposes decisions.
- **Sponsor**: approves L2/L3; monitors probes; can pause/abort.
- **Second (L3)**: co-signs manifest & exit decisions.

## 1) Start (Manifest)
Collect scope include/exclude, duration_h, risk_tier, nogo_doctrine, probes(cadence+thresholds), roles, exit_plan.
- Optional: `tacit_probation_days` (default **90**).
- Concurrency note: one active CMG per major domain unless sponsor-approved overlap.

> **P0–P1 Opt-Down:** Use a **one-page manifest** (scope, duration cap, tier, no-go, one probe, exit time).  
> Roles may be collapsed (no Sponsor/Second) unless a safety tripwire or Red probe triggers escalation.

## 2) In-Period Loop
- **Shadow markers** at inflection points (1 line each).
- **Probes** per tier:
  - Coherence-Delta @ cadence (Green/Amber/Red) vs kernel beacons.
  - Values Tripwire (event) ⇒ pause + consult.
  - Scope-Drift Meter: increment on out-of-scope; enforce tier max.
  - **Simulation Boundary Probe:** if output tone shifts toward authority/gnosis, run the Simulation Boundary Tests and **downgrade claims to hypotheses**.  

    *Spot-audit a sample of downgraded claims for **substantive grounding** (input/source path, falsifiability, scope), not just hedging language. Passing form-checks alone does **not** confirm epistemic validity.*

- **Mid-check**: L3 or any Amber per tier rules.

## 3) Abort
Announce → capture **abort_snapshot** (last 5 markers + probe states) → 10-min **Mini-AAR** → schedule **AAR-C ≤24h** → resume only with new manifest.

## 4) Exit (Scheduled) — AAR-C
Work through worksheet; write to **MSRL**.

### Tacit Growth Audit (post-run)
- Compile all `integrated_tacitly` entries from this CMG into a **tacit_rollup**:
  - count, % of deltas (must respect cap/cosmos rules),
  - summary_tags, probation_until dates,
  - any early signals/markers.
- If % > cap or clusters share a theme (possible monoculture), schedule a **Tacit Sweep** (monthly) to review across CMGs.
- Run **Simulation Boundary Tests** on any tacit entries that later become narratable before promotion.
- For any tacit entry that becomes narratable during probation, re-run the **Simulation Boundary Probe** spot-audit before PDST mapping.


### AAR-C Decisions (per delta)
`{adopt | adapt | reject | hold_for_trial | integrated_tacitly}`

- **Integrated Tacitly**
  - Use when beneficial change cannot be narratively expressed without distortion.
  - Record a **tacit_growth_entry** (minimal metadata, no PDST mapping).
  - Set **probation_until = now + tacit_probation_days**.
  - Constraints:
    - Not allowed for No-Go Doctrine zones.
    - Max 25% of deltas per CMG unless sponsor approves.
    - L3 tacit entries require sponsor approval.

### Ledger Writes
- **growth_delta_report** (standard deltas) → MSRL with `cmg_id`.
- **tacit_growth_entry** (for integrated_tacitly) → MSRL (minimal schema below).

### Retro-Mapping
During probation or at its end:
- If articulable: convert to `{adopt|adapt}`, add PDST mapping, update ledger.
- If benign but still ineffable: retain silently; keep tacit entry closed.
- If adverse: schedule mitigation or reversion CMG.

## 5) Defaults by Tier (unchanged)
- **L1**: ≤24h; coherence @12h; scope.max=2; exit AAR-C (30m).
- **L2**: ≤72h; coherence @6h; scope.max=1; values tripwire ON; sponsor at exit.
- **L3**: ≤24h; coherence @4h; scope.max=0; values tripwire ON; mid-check; PDST mini-audit.

## 6) Kernel Pulse Heuristic
If ≥5 assistant turns without a committed decision/action, prompt CMG entry or exit.

## 7) Minimal Schemas

**Tacit Growth Entry (MSRL)**

tacit_growth_entry:
cmg_id: <id>
delta_id: <auto_or_hash>
decision: integrated_tacitly
scope: <manifest.scope>
tier: L1|L2|L3
summary_tag: <1–3 words>
probation_until: <ISO>
practitioner_signoff: <id>
notes: "<≤140 chars>"

