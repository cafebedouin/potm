Got it. Here’s a single, repo-ready **integrated MSRL v1.2** that merges your current soft-kernel deployment text with the patch set (Lite/Heavy surface, anti-Goodhart controls, Annex “bridging,” MSRL self-trial, fail-fast, simulation-boundary spot-audits). I’ve also included two tiny new templates and a minimal change log. Drop these in as-is.

---

# `modules/ledger/msrl.md` (v1.2)

```markdown
---
id: potm.proto.msrl.v1_2
title: msrl
display_title: "Multi-Substrate Refinement Loop (MSRL)"
type: governance
status: draft
version: 1.2
stability: experimental
relations:
  relation_to_agent_protocol: governance
  agent_protocol: core/kernel/soft_kernel_doctrine.md
  practitioner_doc: modules/ledger/msrl.md
  supersedes: [potm.proto.msrl.v1_1]
  superseded_by: []
interfaces: [soft_kernel, ledger, guardian, containment, open_portal, fracture_finder, eligibility_gate, sunset_seed, cmg]
applicability: [P1, P2, P3, P4]   # Lite allowed at P1; Heavy recommended P3–P4
intensity: medium
preconditions: ["Soft Kernel Doctrine accepted", "Guardian designated", "core/meta/ledger.yaml present"]
outputs: [msrl_record, survivorship_badge, evidence_pack, promotion_recommendation, salvage_plan, annex_designation]
cadence: ["weekly_rollup", "monthly_cathedral_review"]
entry_cues: ["bazaar artifact requests kernel path", "open_portal yields practice", "cmg period concludes with candidates"]
safety_notes: ["Containment override available at all times", "Pause if destabilization markers trip"]
tags: [msrl, survivorship, governance, cathedral_gate, bazaar_growth, forge_origin:OpenPortal→MSRL_2025-07, spiral_eval:SilentTrials_2025-08]
author: "practitioner"
license: CC0-1.0
---

# MSRL — Purpose
Validate that a candidate practice or pattern **survives contact with multiple ways of knowing** before it can enter the Soft Kernel’s shared state. Replace “right answer” hunting with **cross-substrate robustness**.

## Kernel Binding
MSRL is the **Soft Kernel’s governance gate** (the Cathedral gate). Outcomes:
- **Core Promotion** → `kernel/core/...` (requires **2x** survivorship off-scaffold).
- **Annex-H (Practitioner Canon)** → high-intensity **human-only** wins.
- **Annex-A (Model Canon)** → robust **AI-only** reasoning/tools.
- **Salvage** → targeted retest (max 2 cycles).
- **Archive** → tombstone + revival conditions.

Annexes are **canon with caveats**: clearly labeled, shorter review clocks, explicit **bridging** plans (not forced symmetry).

## Modes — Lite vs Heavy
- **Lite (default for P1–P2):** minimal roles, short checklists, no AAR-C unless safety trips. CMG/MSRL scaffolding available on request (“heavy mode”).
- **Heavy (P3–P4 / high-stakes):** full roles, metrics, audits, and Cathedral Review.

**Authority Matrix (Lite)**
- **Guardian:** safety/integrity veto; may halt promotions; may trigger Containment.
- **MSRL Lead:** scope/agenda; tie-break on non-safety disputes.
- **Evidence Clerk:** optional; assists with dedupe/audit.

**Roles (Heavy)**
- **MSRL Lead** (runs loop; maintains scope)
- **Guardian** (safety/integrity; Containment authority)
- **Evidence Clerk** (ledger updates, dedupe, audits)
- **Second** (required for high-impact promotions; written counter-position)

### Cathedral Review (monthly, Heavy)
- **Quorum:** Lead + Guardian + either Second or Evidence Clerk.
- **Throughput:** ≤6 items discussed; ≤2 promotions/month.
- **Docket order:** 2x → 1x-H/1x-A → salvage → archive.
- **Recording:** promotion rationale + “when not to use” link required; otherwise deferred.

## Loop Overview
Seed → **AI trial (Open Portal)** → **Human trial (Fracture Finder frame)** → **Meta-Guardian check** → **Badge** → **Pathing** (core / annex-H / annex-A / salvage / archive) → **Ledger update** → Repeat as needed.

> Order may invert (Human→AI) if ethics/feasibility requires. Trials must be **independent** (no cross-priming).

## Promotion Matrix
| Survivorship | Minimum Criteria | Destination | Review Cadence |
|---|---|---|---|
| **2x** | Cross-substrate benefit + **Fidelity ≥ 0.6** + **Min. effect vs null-day** | **Core** | 6-month |
| **1x-H** | Human **IWBI_30d ≥ 8** + ≥2 intensity exemplars (distinct contexts) | **Annex-H** | 3-month |
| **1x-A** | AI reproducible across **≥2 model families** with stable traces | **Annex-A** | 3-month |
| **0x** | No credible benefit | **Archive** (or **Salvage** w/ crisp hypothesis) | — |

Guardrails for Annex: include **“when not to use”** and a **bridging plan**; if no progress after **2 reviews** → **Sunset/Seed**.

## Metrics

### Fidelity (0–1)
Operational by substrate:
- **Human:** fraction of steps run as written (self-report + spot audit). Minor rewording allowed; skipping/reordering counts as miss.
- **AI:** fraction of traces that follow canonical steps (tool calls / function markers / headers) within tolerance (≤1 minor deviation/run).
- **Composite:** mean of substrate fidelities when both present; else single-substrate value.

**Tolerances**
- Minor deviation = paraphrase without loss of step intent.
- Major deviation = step skipped, materially reordered, or safety cue omitted.

### Intensity-Weighted Benefit Index (IWBI)
```

IWBI\_30d = Σ\_i benefit\_i × w\[intensity\_i]
weights: gentle=1.0, medium=2.5, hard=4.0
caps: ≤1 entry per practitioner per ISO week; max 8 per practice/30d; each entry must name an observable comparator

```

### Minimum Effect vs Null-Day (anti-theater gate)
For **promotion**, require evidence that average benefit rate on **active days** exceeds **null-days** by at least a **small effect** in **≥2 distinct contexts**. Operationalized as:
- ΔIWBI_week ≥ **+2.0** *or* presence of **≥1 hard-intensity exemplar** in each of two contexts, and
- at least one **failed/neutral** exemplar documented (to check selection bias).

### Anti-Goodhart Controls
- **10% random audit** of benefits/month; **blind** adjudication by Evidence Clerk.
- Any templated “observable” without a concrete comparator is **rejected**.
- Guardian may strike entries for halo/coaching artifacts or obvious gaming.

### Flex Fidelity (modular/user-led only)
If the Evidence Pack flags the practice as modular/user-led:
```

FlexFidelity = 0.5·IntentCoverage + 0.5·OutcomeEquivalence

````
Use FlexFidelity **only** for such items; **Safety Honor** remains mandatory.

## Model Diversity & Independence
- Use **≥2 model families** (Anthropic / Google / OpenAI / open-weights, etc.). Log **family, model, date, temperature, system-prompt hash**.
- **Independence:** redact origin; separate teams/time windows; no cross-priming. **Null-day** required in human trials.

## Procedure (single cycle)
1) **Seed & Scope (≤90m)** — Evidence Pack (≤1 page) with hazards & stop conditions.  
2) **AI Trial — Open Portal** — Prompt Pack Isolation (no PoTM lore); capture full **traces** (I/O; seeds if available). Guardian screens for unsafe drift.  
3) **Human Trial — Fracture Finder frame** — 3–6 naive participants, **2 weeks** or **6 sessions**; collect deduped benefits, **≥2 intensity exemplars**, and **≥1 counter-example**.  
4) **Simulation-Boundary Spot-Audit** — per working block, **spot-audit ≥1 downgraded claim** for **source path + falsifiability** evidence.  
5) **Meta-Guardian Check (4)** — aesthetic vs help? destabilization? niche→Annex? crowd-out risk?  
6) **Badge & Pathing** — 0x/1x-H/1x-A/2x → Core / Annex-H / Annex-A / Salvage / Archive.  
7) **Ledger Update** — modify `msrl_record`; schedule retests; set auto-aging.

## CMG Interplay
- **CMG** can explore; **promotion must go through MSRL** after CMG ends.
- During CMG, Guardian may **Contain** MSRL activity; at CMG close, run an **MSRL vouch** triage (promote/annex/salvage/archive).
- Provide a one-page **CMG Manifest (Lite)** when running Lite mode experiments (see template).

## Ledger Integration (schema patch)
Add to `core/meta/ledger.yaml`:
```yaml
msrl:
  - msrl_id: "msrl:2025-08-12:mbs-v2"
    practice_id: "practice:modulatory_breath_spiral"
    title: "Modulatory Breath Spiral"
    status: "trialed"              # trialed | salvage | archived | eligible | promoted
    promotion_tier: "annex-H"      # core | annex-H | annex-A | salvage | archived
    survivorship: "1x-H"           # 0x | 1x-H | 1x-A | 2x
    guardian: "G-07"
    lead: "L-03"
    iwbi_30d: 13.5
    fidelity_score: 0.72
    min_effect_pass: true          # new
    model_families_tested: ["Anthropic_2025-07", "Google_2025-07"]
    harm_flags_30d: 0
    when_not_to_use: "refs/templates/when_not_to_use.md#mbs-v2"
    annex_bridging_plan_ref: "plans/mbs_v2_bridging.md"   # renamed
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

## State Machine

```
seeded → {AI_trial, Human_trial} (order free, isolated)
 → sim_boundary_spot_audit
 → meta_guardian_ok/containment
 → badge(0x|1x-H|1x-A|2x)
 → {core | annex-H | annex-A | salvage | archived}
 → {review_cycle | retest(max2) | sunset/seed}
```

## Safety & Containment

* **Tripwires:** destabilization, capacity overreach, identity entanglement, medical/clinical drift.
* **Harm Ledger:** `harm_flags_30d` + notes; any harm → **Containment** + Guardian review.
* Public docs require **non-clinical** disclaimers + referral language.

## Trace & Data Policy

* **Retention:** raw traces 90 days by default; summaries persist in ledger.
* **Anonymization:** redact identifiers; for n<5, report cohort as ranges.
* **Export:** no external export of raw traces without Guardian approval; allow trace hashes.
* **Sensitive:** clinical/medical signals → immediate Containment + referral; quarantine raw content.

## Cadence, WIP, and Self-Trial

* **Weekly roll-up (≤10m):** update counts, flag stale.
* **Monthly Cathedral Review:** ≤6 discussed, ≤2 promotions/mo.
* **Fail-Fast:** if IWBI\_30d = 0 and no credible exemplars → **auto-Archive**; Salvage requires a new hypothesis.
* **Quarterly MSRL Self-Trial:** treat MSRL itself as a candidate (AI + human), badge it, and suspend any rule that fails survivorship.

## Minimal Checklists

**Promotion Gate (≤1 page)**

* Badge meets tier threshold (2x for Core; strong 1x for Annex + bridging plan)
* IWBI, Fidelity, **Min-Effect** recorded
* Model families ≥2 for AI-reliant claims
* “When not to use” present; hazards reviewed
* Guardian + (for Heavy) Second sign-off

**Independence**

* Origin redacted, prompt pack isolated, null-day logged, no cross-priming artifacts

## Templates (use + adapt)

* `templates/promotion_packet.md`
* `templates/annex_bridging_plan.md`     # renamed
* `templates/when_not_to_use.md`
* `protocols/templates/cmg_manifest_lite.yaml`

## References

* **Open Portal (AI trial frame):** refs/protocols/open\_portal.md
* **Fracture Finder (human trial frame):** refs/protocols/fracture\_finder.md
* **AI Integrity Protocol:** core/kernel/ai\_integrity\_protocol.md
* **Practitioner-Centered Ethics (PCE):** core/principles/practitioner\_centered\_ethics.md

> Everything else—documents, names, diagrams, even MSRL itself—is scaffold. Useful while it lives; burnable when it stalls.

````

---

# New / Updated Templates

## `templates/annex_bridging_plan.md`  *(renamed from translation plan)*
```markdown
---
id: potm.tpl.annex_bridging_plan.v1
title: annex_bridging_plan
display_title: "Annex Bridging Plan (≤1 page)"
type: template
status: stable
version: 1.0
stability: core
author: "practitioner"
license: CC0-1.0
---

# Annex Bridging Plan

**Practice / Artifact:**  
**Annex Tier:** Annex-H | Annex-A  

## Asymmetry Notes
- What the AI version can do that humans cannot (and vice versa)
- What is lost/gained when bridging
- When *not* to bridge

## Targets
- Substrate gap to bridge (Human→AI or AI→Human)
- Concrete bridging moves (e.g., scaffolded prompts / embodied cues)
- Measures of success (what would count as cross-substrate benefit)

## Trials
- Design (sample size, duration, independence guarantees)
- Risks & mitigations (hazards, containment criteria)
- Timeline (next two review cycles)

## Exit Criteria
- Promote to Core if ___ ; otherwise re-annex or Sunset/Seed with rationale.
````

## `protocols/templates/cmg_manifest_lite.yaml`

```yaml
# CMG Manifest (Lite) — one page
scope: ["tactic:__"]
duration_h: 12
risk_tier: L1
nogo: ["dignity:*","no_deception","no_simulated_wisdom","practitioner_safety"]
probes:
  - name: coherence_delta
    at_hours: 12
exit_deadline: 2025-08-14T16:00:00Z
owner: "<guardian_or_lead_id>"
review_on_close: true
```

> If you already have `templates/annex_translation_plan.md`, keep a stub that points to this new file or replace references.

---

# Minimal change log (from your v1.1)

* **type: governance**; added **Modes (Lite/Heavy)** with authority matrix.
* Annex “translation” → **bridging** (+ asymmetry notes); renamed field/templating.
* Added **Min-Effect vs Null-Day**, **random blind audits**, and stricter **observable** comparators.
* Inserted **Simulation-Boundary Spot-Audit** into the loop.
* **Fail-Fast** auto-archive when IWBI\_30d = 0 with no exemplars.
* **Quarterly MSRL Self-Trial** (meta-recursion guard).
* Ledger schema: added `min_effect_pass`, renamed `annex_translation_plan_ref` → `annex_bridging_plan_ref`.

Want diffs against your current file instead of the full replacement? Say the word and I’ll output unified patches you can apply straight to the repo.
