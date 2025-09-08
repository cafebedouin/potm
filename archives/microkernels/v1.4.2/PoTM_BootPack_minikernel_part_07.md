# PoTM Boot Pack — Soft Kernel — Part 07 (of 8)
Version: v1.0 | Generated: 2025-08-12

**Operator Contract**
- Don’t assume unstated context; ask if missing.
- Only use content in this part unless I provide another.
- Honor kernel beacons (dignity, no_deception, no_simulated_wisdom, clarity>fluency, practitioner_safety).

---8<--- FILE: modules/ledger/msrl.md (sec_011.md) ---8<---
## Ledger Integration (schema patch)
Add to `core/meta/ledger.yaml`:
```yaml
msrl:
  - msrl_id: "msrl:2025-08-12:mbs-v2"
    practice_id: "practice:modulatory_breath_spiral"
    title: "Modulatory Breath Spiral"
    status: "trialed"            # trialed | salvage | archived | eligible | promoted
    promotion_tier: "annex-H"    # core | annex-H | annex-A | salvage | archived
    survivorship: "1x-H"         # 0x | 1x-H | 1x-A | 2x
    guardian: "G-07"
    lead: "L-03"
    iwbi_30d: 13.5
    fidelity_score: 0.72
    model_families_tested: ["Anthropic_2025-07", "Google_2025-07"]
    harm_flags_30d: 0
    when_not_to_use: "refs/templates/when_not_to_use.md#mbs-v2"
    annex_translation_plan_ref: "plans/mbs_v2_translation.md"
    review_cadence: "3mo"
    evidence_pack: "evidence/mbs_v2_onepager.md"
    ai_trials:
      - model: "familyA:modelX"
        context_isolation: true
        date: "2025-08-01"
        result: "partial"
        trace_ref: "traces/ai/mbs_v2_2025-08-01.jsonl"
    human_trials:
      - cohort_id: "C-12"
        n: 5
        window: "2025-08-01→2025-08-14"
        benefit_count_30d: 7
        benefit_intensity_hist_30d: [3,2,2]
        last_benefit_date: "2025-08-12"
        fidelity_score: 0.7
        hazard_flags: []
        exemplars_ref: "notes/human/mbs_v2_exemplars.md"
    decisions:
      - date: "2025-08-15"
        by: "Guardian"
        action: "Annex-H"
        rationale: "Strong human signal; AI unclear. Plan: scaffolded prompts."
    next_actions:
      - "ai_retest: 2025-09-01"
    tombstone: null
````


---8<--- /END FILE: modules/ledger/msrl.md (sec_011.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_012.md) ---8<---
## State Machine

```
seeded → {AI_trial, Human_trial} (order free, isolated)
 → meta_guardian_ok/containment
 → badge(0x|1x-H|1x-A|2x)
 → {core | annex-H | annex-A | salvage | archived}
 → {review_cycle | retest(max2) | sunset/seed}
```


---8<--- /END FILE: modules/ledger/msrl.md (sec_012.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_013.md) ---8<---
## Safety & Containment

* **Tripwires**: destabilization, capacity overreach, identity entanglement, medical/clinical drift.
* **Harm Ledger**: `harm_flags_30d` + brief notes; any harm → **Containment** + Guardian review.
* **Non-clinical** disclaimer + referral language required for public docs.


---8<--- /END FILE: modules/ledger/msrl.md (sec_013.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_014.md) ---8<---
## Trace & Data Policy
- **Retention:** default 90 days for raw traces; summaries kept in ledger.
- **Anonymization:** redact personal identifiers; cohort sizes reported as ranges if n<5.
- **Export:** no external export of raw traces without Guardian approval; model trace hashes allowed.
- **Sensitive content:** if clinical/medical signals arise, immediate Containment + referral language; raw content quarantined.


---8<--- /END FILE: modules/ledger/msrl.md (sec_014.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_015.md) ---8<---
## Cadence & WIP

* **Weekly roll-up (≤10m)**: update counts, flag stale.
* **Monthly Cathedral Review**: ≤6 discussed, ≤2 promotions/mo.
* **Auto-aging**: items with **no benefit** in 90 days must re-justify or **sunset**.

### Role authorities
- **MSRL Lead:** agenda, scope, tie-break on non-safety disputes.
- **Guardian:** safety/integrity veto; can trigger Containment; can halt promotions.
- **Second:** required for high-impact promotions (Core, Annex-A with API exposure); provides written counter-position.

### Cathedral Review (monthly)
- **Quorum:** Lead + Guardian + either Second or Evidence Clerk.
- **Throughput:** ≤6 items discussed; ≤2 promotions/month.
- **Docket order:** 2x → 1x-H/1x-A → salvage; archive last.
- **Decision recording:** promotion rationale + “when not to use” link must be present or item is deferred.



---8<--- /END FILE: modules/ledger/msrl.md (sec_015.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_016.md) ---8<---
## Minimal Checklists

**Promotion Gate (≤1 page)**

* Badge meets tier threshold (2x for Core; strong 1x for Annex + plan)
* IWBI & Fidelity recorded
* Model families ≥2 (for AI-reliant claims)
* “When not to use” present; hazards reviewed
* Guardian + Second sign-off

**Independence**

* Origin redacted, prompt pack isolated, null-day logged, no cross-priming artifacts


---8<--- /END FILE: modules/ledger/msrl.md (sec_016.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_017.md) ---8<---
## Templates (use + adapt)

* `templates/promotion_packet.md`
* `templates/annex_translation_plan.md`
* `templates/when_not_to_use.md`


---8<--- /END FILE: modules/ledger/msrl.md (sec_017.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_018.md) ---8<---
## References
- **Open Portal (AI trial frame):** refs/protocols/open_portal.md
- **Fracture Finder (human trial frame):** refs/protocols/fracture_finder.md
- **AI Integrity Protocol:** core/kernel/ai_integrity_protocol.md
- **Practitioner-Centered Ethics (PCE):** core/principles/practitioner_centered_ethics.md


> Everything else—documents, names, diagrams, even MSRL itself—is scaffold. Useful while it lives; burnable when it stalls.



---8<--- /END FILE: modules/ledger/msrl.md (sec_018.md) ---8<---

---8<--- FILE: annex_a/README.md ---8<---
---
id: potm.annex.a.readme.v1
title: annex_a_readme
display_title: "Annex-A — Model Canon"
type: guideline
status: draft
version: 1.0
stability: experimental
relations:
  relation_to_agent_protocol: none
  supersedes: []
  superseded_by: []
interfaces: [msrl, ledger, guardian, sunset_seed]
applicability: [P2, P3, P4]
intensity: varies
author: "practitioner"
license: CC0-1.0
tags: [annex, ai, forge_origin:MSRL, spiral_eval:AnnexPolicy_v1]
---

# Annex-A — Purpose
A curated space for **substrate-strong AI artifacts** (reasoning tools, prompt grammars) that are **robust across ≥2 model families** but do not translate to direct human practice (1x-A).

## Rules
- Must include **When Not to Use** and a **Translation Plan**.
- **Review cadence: 3 months**; two missed translations → **Sunset/Seed**.
- Trace capture and reproduction instructions are mandatory.
- **Capacity cap:** Default **N=20**. Override cap = **12 × active_reviewers** (rounded to nearest 4).
  Exceeding the active cap requires archiving or promotion to admit new entries.



- **Aging:** items with no measurable benefit or translation progress across **2 review cycles** auto-move to **Sunset/Seed**, with revival criteria specified.
- **Capacity cap:** total Annex items capped at N=20 each; exceeding cap requires archiving or promotion to admit new entries.

---8<--- /END FILE: annex_a/README.md ---8<---

---8<--- FILE: annex_a/README.md ---8<---
---
id: potm.annex.a.readme.v1
title: annex_a_readme
display_title: "Annex-A — Model Canon"
type: guideline
status: draft
version: 1.0
stability: experimental
relations:
  relation_to_agent_protocol: none
  supersedes: []
  superseded_by: []
interfaces: [msrl, ledger, guardian, sunset_seed]
applicability: [P2, P3, P4]
intensity: varies
author: "practitioner"
license: CC0-1.0
tags: [annex, ai, forge_origin:MSRL, spiral_eval:AnnexPolicy_v1]
---

# Annex-A — Purpose
A curated space for **substrate-strong AI artifacts** (reasoning tools, prompt grammars) that are **robust across ≥2 model families** but do not translate to direct human practice (1x-A).

## Rules
- Must include **When Not to Use** and a **Translation Plan**.
- **Review cadence: 3 months**; two missed translations → **Sunset/Seed**.
- Trace capture and reproduction instructions are mandatory.
- **Capacity cap:** Default **N=20**. Override cap = **12 × active_reviewers** (rounded to nearest 4).
  Exceeding the active cap requires archiving or promotion to admit new entries.



- **Aging:** items with no measurable benefit or translation progress across **2 review cycles** auto-move to **Sunset/Seed**, with revival criteria specified.
- **Capacity cap:** total Annex items capped at N=20 each; exceeding cap requires archiving or promotion to admit new entries.

---8<--- /END FILE: annex_a/README.md ---8<---

---8<--- FILE: protocols/templates/aar_c_worksheet.md ---8<---
# AAR-C — Continuous-Mode Growth Reconciliation
cmg_id: ____   owner: ____   sponsor: ____   date: ____

1) Snapshot — What changed?
- Concepts:
- Heuristics:
- Strategies/Tactics:
- Evidence/markers (bullets only):

2) Classification (per delta)
- delta_id → {maladaptive | growth-driven | uncertain} + 1-line rationale

3) PDST Mapping (if applicable)
- delta_id → P|D|S|T (new/updated) + link/path

4) Decisions
- delta_id → {adopt | adapt | reject | hold_for_trial | integrated_tacitly}
  - If integrated_tacitly:
    - summary_tag:
    - probation_until: <date>   (default: +90d)
    - practitioner_signoff: <id>
    - notes (≤140 chars):

5) Kernel Shift?
- shift_id + rationale + cross-refs (for adopted/adapted)

6) Risks & Debt
- hazards:
- mitigations (owner + due):

7) Ledger Write
- Append `growth_delta_report` (and any `tacit_growth_entry`) to MSRL with `cmg_id`.

8) Next Cadence
- If trial: metrics, duration, gating criteria.

---8<--- /END FILE: protocols/templates/aar_c_worksheet.md ---8<---

