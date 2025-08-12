# PoTM Boot Pack — Soft Kernel — Part 06 (of 8)
Version: v1.0 | Generated: 2025-08-12

**Operator Contract**
- Don’t assume unstated context; ask if missing.
- Only use content in this part unless I provide another.
- Honor kernel beacons (dignity, no_deception, no_simulated_wisdom, clarity>fluency, practitioner_safety).

---8<--- FILE: modules/ledger/msrl.md (sec_001.md) ---8<---
---
id: potm.proto.msrl.v1_1
title: msrl
display_title: "Multi-Substrate Refinement Loop (MSRL)"
type: diagnostic
status: draft
version: 1.1
stability: experimental
relations:
  relation_to_agent_protocol: governance
  agent_protocol: core/kernel/soft_kernel_doctrine.md
  practitioner_doc: modules/ledger/msrl.md
  supersedes: [potm.proto.msrl.v1]
  superseded_by: []



interfaces: [soft_kernel, ledger, guardian, containment, open_portal, fracture_finder, eligibility_gate, sunset_seed, cmg]
applicability: [P2, P3, P4]
intensity: medium
preconditions: ["Soft Kernel Doctrine accepted", "Guardian designated", "core/meta/ledger.yaml present"]
outputs: [msrl_record, survivorship_badge, evidence_pack, promotion_recommendation, salvage_plan, annex_designation]
cadence: ["weekly_rollup", "monthly_cathedral_review"]
entry_cues: ["bazaar artifact requests kernel path", "open_portal yields practice", "cmg period concludes with candidates"]
safety_notes: ["Containment override available at all times", "Pause if destabilization markers trip"]
tags: [msrl, survivorship, diagnostic, cathedral_gate, bazaar_growth, forge_origin:OpenPortal→MSRL_2025-07, spiral_eval:SilentTrials_2025-08]
author: "practitioner"
license: CC0-1.0
---

# MSRL — Purpose
Validate that a candidate practice or pattern **survives contact with multiple ways of knowing** before it can enter the Soft Kernel’s shared state. Replace “right answer” hunting with **cross-substrate robustness**.


---8<--- /END FILE: modules/ledger/msrl.md (sec_001.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_002.md) ---8<---
## Kernel Binding
MSRL is the **Soft Kernel’s governance gate** (the Cathedral gate). Outcomes:
- **Core Promotion** → `kernel/core/...` (requires **2x** survivorship off-scaffold).
- **Annex-H (Practitioner Canon)** → high-intensity **human-only** wins.
- **Annex-A (Model Canon)** → robust **AI-only** reasoning/tools.
- **Salvage** → targeted retest (max 2 cycles).
- **Archive** → tombstone + revival conditions.

Annexes are **canon with caveats**: clearly labeled, shorter review clocks, explicit translation plans.


---8<--- /END FILE: modules/ledger/msrl.md (sec_002.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_003.md) ---8<---
## Definitions
- **Substrate**: cognitive architecture class. Here: **Human** (naive practitioners) and **AI** (models isolated from PoTM lore).
- **Survivorship badge**: **0x** (fails both) / **1x-H** / **1x-A** / **2x** (works in both).
- **Evidence Pack (≤1 page)**: Tuesday-problem, intended user, 5-step minimal procedure, outcomes, stop conditions, measurement, pointers.
- **Benefit signal**: deduped instance of practical help.


---8<--- /END FILE: modules/ledger/msrl.md (sec_003.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_004.md) ---8<---
## Roles
- **MSRL Lead**: runs loop; maintains scope.
- **Guardian**: safety/integrity; can trigger **Containment** anytime.
- **Evidence Clerk**: updates `ledger.yaml`, enforces dedupe & independence.
- **Second** (optional): structured counter-voice for bias checks.

### Role authorities
- **MSRL Lead:** agenda, scope, tie-break on non-safety disputes.
- **Guardian:** safety/integrity veto; can trigger Containment; can halt promotions.
- **Second:** required for high-impact promotions (Core, Annex-A with API exposure); provides written counter-position.

### Cathedral Review (monthly)
- **Quorum:** Lead + Guardian + either Second or Evidence Clerk.
- **Throughput:** ≤6 items discussed; ≤2 promotions/month.
- **Docket order:** 2x → 1x-H/1x-A → salvage; archive last.
- **Decision recording:** promotion rationale + “when not to use” link must be present or item is deferred.


---8<--- /END FILE: modules/ledger/msrl.md (sec_004.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_005.md) ---8<---
## Loop Overview
Seed → **AI trial (Open Portal)** → **Human trial (Fracture Finder frame)** → **Meta-Guardian check** → **Badge** → **Pathing** (core / annex-H / annex-A / salvage / archive) → **Ledger update** → Repeat as needed.

> Order may invert (Human→AI) if ethics/feasibility requires. Trials must be **independent** (no cross-priming).


---8<--- /END FILE: modules/ledger/msrl.md (sec_005.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_006.md) ---8<---
## Promotion Matrix
| Survivorship | Minimum Criteria | Destination | Review Cadence |
|---|---|---|---|
| **2x** | Cross-substrate benefit + **Fidelity ≥ 0.6** | **Core** | 6-month |
| **1x-H** | Human **IWBI_30d ≥ 8** + ≥2 intensity exemplars (distinct contexts) | **Annex-H** | 3-month |
| **1x-A** | AI reproducible across **≥2 model families** with stable traces | **Annex-A** | 3-month |
| **0x** | No credible benefit | **Archive** (or **Salvage** w/ crisp hypothesis) | — |

Guardrails for Annex: include **“when not to use”** and a **translation plan**; if no progress after **2 reviews** → **Sunset/Seed**.


---8<--- /END FILE: modules/ledger/msrl.md (sec_006.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_007.md) ---8<---
## Metrics

### Fidelity (0–1)
Operational definition by substrate:

- **Human sessions:** fraction of steps run as written in the canonical 5-step form (self-report + spot audit). Minor rewording of prompts/cues allowed; skipping or reordering counts as a miss.
- **AI runs:** fraction of traces that follow the canonical steps (tool calls / function markers / section headers) within tolerance (≤1 minor deviation per run).
- **Composite:** mean of substrate fidelities when both are present; else single-substrate value.

**Tolerances**
- Minor deviation: paraphrase without loss of step intent.
- Major deviation: step skipped, reordered materially, or safety cue omitted.

**Intensity-Weighted Benefit Index (IWBI)**

IWBI_30d = Σ_i benefit_i × w[intensity_i], with caps
weights: gentle=1.0, medium=2.5, hard=4.0
caps:

- ≤1 entry per practitioner per ISO week
- max contribution per practice: 8 in 30 days
- require "observable" note per entry (no vibes-only)

**Benefit adjudication:** Evidence Clerk dedupes and rejects vague or duplicated claims; Guardian may strike entries that show coach/halo effects or obvious Goodharting.

**Fidelity Score (0–1)**: fraction of sessions run as written.

Thresholds:
- **Core**: IWBI_30d ≥ 10 **and** Fidelity ≥ 0.6
- **Annex-H**: IWBI_30d ≥ 8 (human), regardless of AI
- **Annex-A**: stable AI traces ≥3 runs/model across **2 families**

**Flex Fidelity (variant, modular/user-led only)**
Flex Fidelity = 0.5·Intent Coverage + 0.5·Outcome Equivalence, with Safety Honor required.
Report both metrics; use Flex Fidelity for promotion decisions *only* if the practice is labeled modular/user-led in the Evidence Pack.


---8<--- /END FILE: modules/ledger/msrl.md (sec_007.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_008.md) ---8<---
## Model Diversity & Independence
- Use **≥2 distinct model families** (e.g., Anthropic / Google / OpenAI / open-weights). Log **family, model, date, temperature, system-prompt hash**.
- **Independence**: redact origin; separate teams/time windows; Evidence Clerk checks for leakage.
- **Null-day** in human trials: participants skip the practice once and log differences.


---8<--- /END FILE: modules/ledger/msrl.md (sec_008.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_009.md) ---8<---
## Procedure (single cycle)
1. **Seed & Scope (≤90m)**
   Draft Evidence Pack (≤1 page) with hazards & stop conditions.
2. **AI Trial — Open Portal**
   - **Prompt Pack Isolation** (no PoTM lore).
   - Capture full **traces** (inputs/outputs; seeds if available).
   - Guardian screens for unsafe content/coherence drift.
3. **Human Trial — Fracture Finder frame**
   - 3–6 naive participants, **2 weeks** or **6 sessions**.
   - Collect deduped benefits, **≥2 intensity exemplars**, ≥1 counter-example.
4. **Meta-Guardian Check (4 questions)**
   1) Are we mistaking aesthetic coherence for help?
   2) Any capacity/identity destabilization signs?
   3) Is benefit niche → Annex vs Core?
   4) Would continuing crowd out higher-stakes work?
5. **Badge & Pathing**
   Assign 0x/1x-H/1x-A/2x → choose **Core / Annex-H / Annex-A / Salvage / Archive**.
6. **Ledger Update**
   Add/modify `msrl_record` (schema below). Schedule retests; set auto-aging.


---8<--- /END FILE: modules/ledger/msrl.md (sec_009.md) ---8<---

---8<--- FILE: modules/ledger/msrl.md (sec_010.md) ---8<---
## CMG Interplay
- **CMG** may generate candidates. **Exploration** may occur inside CMG, but **promotion must go through MSRL** after CMG ends.
- During CMG, Guardian may **Contain** MSRL activity; at CMG close, run **MSRL vouch** triage (promote/annex/salvage/archive).


---8<--- /END FILE: modules/ledger/msrl.md (sec_010.md) ---8<---

