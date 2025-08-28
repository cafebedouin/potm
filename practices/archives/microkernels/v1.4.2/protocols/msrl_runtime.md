---
id: potm.proto.msrl_runtime.v1
title: msrl_runtime
display_title: "MSRL — Runtime Loop (Single-Cycle)"
type: agent_protocol
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: modules/ledger/msrl.md
  practitioner_doc: modules/ledger/msrl.md
  supersedes: []
  superseded_by: []
interfaces: [soft_kernel, ledger, guardian, containment, open_portal, fracture_finder]
applicability: [P2, P3, P4]
intensity: medium
preconditions: ["Soft Kernel Doctrine accepted", "Guardian designated", "core/meta/ledger.yaml present"]
outputs: [msrl_record, survivorship_badge, evidence_pack, promotion_recommendation]
cadence: ["per candidate cycle"]
entry_cues: ["run msrl on candidate", "cathedral gate request"]
safety_notes: ["Containment override available at all times", "Pause if destabilization markers trip"]
tags: [msrl, runtime, forge_origin:MSRL, spiral_eval:Runtime_v1]
author: "practitioner"
license: CC0-1.0
---

# MSRL Runtime — Single-Cycle Execution

**Purpose:**  
Run the Multi-Substrate Refinement Loop quickly and consistently for one candidate practice/artifact, without full governance doc overhead.

---

## Step 0 — Prep (≤15m)
- Confirm **Guardian** and **MSRL Lead** roles present.
- Pull candidate’s **Evidence Pack** or draft minimal one (≤1 page).
- State hazards & **stop conditions** out loud.

---

## Step 1 — First Trial (AI or Human)
**Choose substrate order based on ethics/feasibility:**
- **AI trial (Open Portal):**
  - Isolate from PoTM lore.
  - Capture full trace (inputs/outputs + prompt pack hash).
  - Guardian screens for unsafe/coherence drift.
- **Human trial (Fracture Finder frame):**
  - Recruit 3–6 naive practitioners.
  - Run ≤2 weeks or ≤6 sessions.
  - Log benefits, intensity exemplars, ≥1 counter-example.

---

## Step 2 — Second Trial (Other Substrate)
- Repeat process with the other substrate.
- Ensure **independence**: no cross-priming, redact origin.

---

## Step 3 — Meta-Guardian Check (4 Qs)
1. Are we mistaking aesthetic coherence for help?  
2. Any capacity/identity destabilization signs?  
3. Is benefit niche → Annex vs Core?  
4. Would continuing crowd out higher-stakes work?

---

## Step 4 — Badge & Pathing
Assign survivorship:
- **2x** → both substrates strong.
- **1x-H** → humans strong, AI weak/absent.
- **1x-A** → AI strong, humans weak/absent.
- **0x** → no credible benefit.

Path accordingly:
- **Core** (2x, meets thresholds).
- **Annex-H** or **Annex-A** (strong 1x + plan).
- **Salvage** (retest, max 2 cycles).
- **Archive**.

---

## Step 5 — Ledger Update (≤10m)
- Record in `core/meta/ledger.yaml` (see MSRL schema).
- Attach trace refs, benefit counts, IWBI, Fidelity.
- Schedule review/retest.

---

## Step 6 — Close & Contain
- If hazards tripped, trigger Containment.
- If safe, mark cycle complete and queue for Cathedral Review.

---

### Quick Checks
- **IWBI thresholds:** Core ≥10; Annex-H ≥8 (human); Annex-A stable AI traces.  
- **Fidelity:** ≥0.6 for Core; any for Annex with plan.  
- **Independence:** null-day logged, no cross-priming artifacts.

---

### Flex Fidelity (for modular/user-led practices)
Use when a practice is explicitly marked “modular” or “user-led”.

- **Intent Coverage (0–1):** proportion of canonical step *intents* satisfied (even if order differs).
- **Safety Honor (0/1):** all safety cues executed (required).
- **Outcome Equivalence (0–1):** observer-rated match to expected outcome pattern.

**Flex Fidelity = 0.5·Intent + 0.5·Outcome** (if Safety=1; else 0).  
Report both **Fidelity** (strict sequence) and **Flex Fidelity**; pick higher **only** if the practice is labeled modular/user-led in the Evidence Pack.

---

> Use this runtime doc **only** for execution. For policy, roles, annex rules, and CMG interplay, see: `modules/ledger/msrl.md`.
