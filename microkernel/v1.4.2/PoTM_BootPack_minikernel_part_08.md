# PoTM Boot Pack — Soft Kernel — Part 08 (of 8)
Version: v1.0 | Generated: 2025-08-12

**Operator Contract**
- Don’t assume unstated context; ask if missing.
- Only use content in this part unless I provide another.
- Honor kernel beacons (dignity, no_deception, no_simulated_wisdom, clarity>fluency, practitioner_safety).

---8<--- FILE: protocols/templates/cmg_manifest.yaml ---8<---
id: cmg_YYYYMMDD_hhmm_owner
owner: <agent_id>
roles:
  sponsor: <id_or_none>
  second: <id_or_none>   # required for L3
profile_level: P2|P3|P4
scope:
  include: ["strategy:search", "tactics:prompting"]
  exclude: []
risk_tier: L1|L2|L3
duration_h: 24
nogo_doctrine: ["dignity:*", "no_simulated_wisdom", "no_deception", "practitioner_safety"]
probes:
  coherence_delta:
    cadence_h: 12|6|4
    thresholds: {amber: tolerate|warn, red: abort}
  values_tripwire: {on: event, action: pause+consult}
  scope_drift_meter: {max_out_of_scope: 2|1|0}
data_policy:
  retention_days: 14
  export: false
exit_plan:
  aar_c_at: 2025-08-14T16:00Z
  reviewer: <sponsor_or_none>
tacit_probation_days: 90     # NEW: default probation for tacit entries
notes: ""

---8<--- /END FILE: protocols/templates/cmg_manifest.yaml ---8<---

---8<--- FILE: templates/promotion_packet.md ---8<---
---
id: potm.tpl.promotion_packet.v1
title: promotion_packet
display_title: "Promotion Packet (≤1 page)"
type: template
status: stable
version: 1.0
stability: core
author: "practitioner"
license: CC0-1.0
---

# Promotion Packet (Cathedral Gate)

**Practice name & ID:**
**Tuesday-problem (1–2 sentences):**
**Intended user/context (plain):**
**Canonical 5-step form (minimal):**
1.
2.
3.
4.
5.

**Outcomes (observables):**
-

**Survivorship badge & evidence:**
- Badge: 2x | 1x-H | 1x-A | 0x
- IWBI_30d: ___ ; Fidelity: ___
- Trials (dates, cohorts/models, links):

**Hazards & when not to use (link to template):**
-

**Translation plan (if Annex):**
-

**Maintenance owner & review cadence:**
- Owner: ___ ; Next review: ___

**Polyphony Note (variants & boundaries):**
- Named variants that also work (links or short notes):
- Where variants diverge safely (scope/context tags):
- When to prefer canonical form over a variant:

**Sign-offs:** Guardian ___ ; Second ___ ; Date ___

---8<--- /END FILE: templates/promotion_packet.md ---8<---

---8<--- FILE: templates/annex_translation_plan.md ---8<---
---
id: potm.tpl.annex_translation_plan.v1
title: annex_translation_plan
display_title: "Annex Translation Plan (≤1 page)"
type: template
status: stable
version: 1.0
stability: core
author: "practitioner"
license: CC0-1.0
---

# Annex Translation Plan

**Practice / Artifact:**
**Annex Tier:** Annex-H | Annex-A
**Hypothesis for translation:** (what principle carries across?)

## Targets
- **Substrate gap to bridge:** (Human→AI or AI→Human)
- **Concrete translation moves:** (e.g., scaffolded prompts / embodied cues)
- **Measures of success:** (what would count as cross-substrate benefit?)

## Trials
- **Design:** sample size, duration, independence guarantees
- **Risks & mitigations:** hazards, containment criteria
- **Timeline:** next two review cycles

## Exit Criteria
- Promote to Core if ___ ; otherwise re-annex or Sunset/Seed with rationale.

---8<--- /END FILE: templates/annex_translation_plan.md ---8<---

---8<--- FILE: templates/null_day_example.md ---8<---
---
id: potm.tpl.null_day_example.v1
title: null_day_example
display_title: "Null-Day Logging Example"
type: template
status: stable
version: 1.0
stability: core
author: "practitioner"
license: CC0-1.0
---

# Null-Day Logging — Example

**Practice:** Focus Pulse v2
**Cohort:** C-12  |  **Participant:** P-03
**Window:** 2025-08-01–2025-08-14  |  **Null-day:** 2025-08-08

## What I skipped
- Skipped Step 3 (pulse timer) and Step 4 (micro-AAR).

## Observed difference (same task/context)
- **Time-on-task:** 31 → 18 min (−13)
- **Subjective clarity (1–5):** 4 → 2
- **Error count:** 1 → 3

## Notes (1–2 lines)
- Without the pulse timer, I drifted to email twice. Micro-AAR seems to anchor re-entry.

---8<--- /END FILE: templates/null_day_example.md ---8<---

---8<--- FILE: templates/when_not_to_use.md ---8<---
---
id: potm.tpl.when_not_to_use.v1
title: when_not_to_use
display_title: "When Not To Use (≤1 page)"
type: template
status: stable
version: 1.0
stability: core
author: "practitioner"
license: CC0-1.0
---

# When Not To Use

**Practice / Artifact:**
**Intended user/context:**

## Contraindications
- (e.g., acute distress without support, medical conditions, role constraints)

## Known failure modes
- (where it tends to backfire or confuse)

## Capacity requirements
- (minimum attention, time, privacy, prior skills)

## Safer alternatives
- (grounding variants, lower-intensity options)

## Referral language
- “This practice is **not a replacement for medical or mental health care**. If you’re experiencing sustained distress, please consider contacting a qualified professional (e.g., a licensed therapist or physician).”
- “If you feel worse while using this practice, **stop** and try a lower-intensity option, or reach out to support.”
- “In crisis, contact your local emergency services or a trusted hotline in your region.”

---8<--- /END FILE: templates/when_not_to_use.md ---8<---

