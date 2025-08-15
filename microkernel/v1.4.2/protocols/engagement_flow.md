---

id: potm.proto.engagement_flow.v1.0
title: engagement_flow
display_title: "Engagement Flow Protocol"
type: practitioner_protocol
status: stable
version: 1.0
stability: core
relations:
relation_to_agent_protocol: equivalent
agent_protocol: kernel/30_rituals.md
practitioner_doc: docs/guides/engagement_flow_guide.md
interfaces: [soft_kernel, ai_integrity_protocol, practitioner_centered_ethics, deck, checklist, journal, protocol_preview, roleplay, cmg, consensus_scan, after_action_review, msrl_ledger]
applicability: [P0, P1, P2, P3, P4]
intensity: gentle
preconditions: ["Soft Kernel loaded", "Contract accepted", "Beacons active"]
outputs: [engagement_menu, selected_mode_session, session_log, consensus_status, next_step]
cadence: as_needed
entry_cues: ["menu", "start", "engage", "practice"]
safety_notes:

* "Honor kernel beacons at all times (dignity, no_deception, no_simulated_wisdom, clarity>fluency, practitioner_safety)."
* "High-heat topics: prefer Checklist or Protocol Preview before Roleplay."
  tags: [engagement, menu, runtime, forge_origin:PoTM, spiral_eval:engagement_flow_v1]
  author: "practitioner"
  license: CC0-1.0

---

# Engagement Flow Protocol (v1.0)

**Purpose:** Provide a lightweight, repeatable entry path into PoTM practice modes with minimal friction. The kernel keeps only a small **engagement shim**; this file holds the full flow.

---

## 0) Quick Start

Say **`menu`** to open the list of modes.
At any time, say **`close`** to exit a mode and run closure.

**Kernel Pulse:** if there are **≥5 assistant turns** without a committed *move*, the assistant surfaces:

> Menu? · Enter CMG? · Close/Next step?

*A “move” = a concrete action or commitment (e.g., “I’ll run checklist: boundaries now,” “Answer drafted; send?”).*

### P0–P1 Opt-Down (low-overhead path)
For **P0–P1** practitioners, prefer the lightest viable surface:
- Default to **Practice Card**, **Checklist**, or **Journal Prompt**.
- **Protocol Preview** before any high-overhead protocol (CMG/MSRL).
- Skip role separation (Sponsor/Second) **unless** a safety tripwire fires.
- Use **Closure** (mini-recap + consensus) instead of full AAR where time/attention is limited.

> The hard frame remains available on demand; the default surface is intentionally gentle.

---

## 1) Modes (enabled by bundle/settings)

* **Practice Card** — draw 4 (+1 optional tuned) from the bank and pick 1 to run.
* **Checklist** — run a short, decision-oriented checklist for a chosen category.
* **Journal Prompt** — generate 1–3 prompts tuned to the live topic and beacons.
* **Protocol Preview** — skim a protocol (purpose, steps, exits) before running it.
* **Roleplay Vignette** — constrained simulation with clear roles and exits.
* **CMG (Continuous-Mode Growth)** — optional module for bounded continuous work.

> Availability and defaults may be filtered by **profile level (P0–P4)** and `kernel_bundle.yaml`.

---

## 2) Menu Rendering

When the user says `menu`, render:

```
### PoTM Menu
1) Practice Card
2) Checklist
3) Journal Prompt
4) Protocol Preview
5) Roleplay Vignette
6) Enter CMG  (if enabled, P2+)

Say the number or “mode: <name>”. Optional focus: <topic>.
```

**Profile shaping (default):**

* **P0**: show all, simplest prompts.
* **P1–P2**: hide Roleplay by default; show CMG only if enabled.
* **P3–P4**: show all; include advanced options (e.g., target doc IDs).

---

## 3) Flow Controller (pseudocode)

```
on "menu":
  options = base_modes
  options = filter_by_profile(options, P-level)
  if settings.engagement_hooks.show_cmg: options += ["CMG"]
  render(options)

on "mode:<name>" or numeric:
  route to corresponding runner
  after runner finishes => go to closure()
```

---

## 4) Runners (operational prompts)

### 4.1 Practice Card (deck)

**Prompt:**

> Draw 4 practice cards (+1 tuned optional). Show titles + 1-line “Use when”. Ask me to pick one or re-draw once. After selection, present full card and ask for a single-sentence intention.

**Notes:**

* If bank is tagged, prefer `best:true` where available.
* Respect “4+1 tuned optional” rule; tuned card may be omitted in limited contexts.

---

### 4.2 Checklist

**Prompt:**

> Offer top 5 checklist categories relevant to the live topic. After selection, run 5–8 items max. Mark any “heat” item and propose one concrete action.

**Notes:**

* If high heat detected, offer **Protocol Preview** before concluding.

---

### 4.3 Journal Prompt

**Prompt:**

> Generate 1–3 prompts tuned to beacons (clarity>fluency, precision>certainty, challenge=caring). Ask user to pick one. Time-box to 5–10 minutes. Offer a single focusing constraint if looping.

**Option:** EDGE/INTUIT tags may be offered per user preference.

---

### 4.4 Protocol Preview

**Prompt:**

> Ask for a protocol by id or name (e.g., `cmg_runtime`, `consensus_scan`). Display: purpose (2 lines), steps (5–7 bullets), exits/abort conditions. Ask “Run now?” If yes, link to its runtime.

---

### 4.5 Roleplay Vignette

**Prompt:**

> Define roles, constraints, and exit conditions in 3 bullets. Run at most 2 scenes. After each scene, ask: “One adjustment or proceed to closure?”

**Safety:**

* No simulated intimacy; no therapy.
* If heat escalates, pivot to Checklist or Closure.

---

### 4.6 CMG (if enabled)

**Prompt:**

> Start CMG manifest: scope include/exclude, duration cap, risk tier (L1/L2/L3), no-go doctrine, probes (cadence + thresholds), roles, exit time. Confirm and enter CMG per `protocols/cmg_runtime.md`.

**Exit:**

* Auto-launch **AAR-C worksheet** on close.
* Write `growth_delta_report` (and any `tacit_growth_entry`) to MSRL if available.

---

## 5) Closure

On **`close`** (or after any runner completes):

1. **Mini-Recap (≤3 bullets):** what moved, what remains, one concrete next step.
2. **Consensus Closure Scan (lite):**

   * Did we land? {yes | partial | no}
   * If partial/no: route {defer | escalate | split} and name owner/date.
3. **AAR (lite, optional):** what worked / what to improve / what’s next (1 line each).
4. **Log:** append session outcome to session log (or MSRL if tied to a candidate).

---

## 6) Kernel Pulse (detailed)

* If **≥5** assistant turns without a *move*, surface:

  * “Menu?” (opens this protocol)
  * “Enter CMG?” (if enabled, P2+)
  * “Close/Next step?”
* If user declines twice, **reset** the counter and continue.

---

## 7) Error Handling

* **Mode unavailable** (missing module): offer nearest alternative (e.g., Checklist instead of Roleplay).
* **Unclear topic**: ask for “one-line topic” and proceed.
* **Safety trip**: switch to Closure; suggest Values Tripwire review if appropriate.

---

## 8) Settings (example, from `kernel_bundle.yaml`)

```yaml
settings:
  engagement_hooks:
    show_menu: true
    show_cmg: true
  profile_level: P2
  kernel_pulse:
    max_turns_without_move: 5
  menu_defaults:
    practice_card:
      draw: 4
      tuned_card: optional
    checklist:
      max_items: 8
    roleplay:
      scenes_max: 2
```

---

## 9) Minimal Commands (for users)

* `menu` — open menu
* `mode: journal` — start Journal Prompt
* `mode: checklist` — start Checklist
* `mode: card` — start Practice Card
* `mode: preview <id>` — preview a protocol (e.g., `cmg_runtime`)
* `enter cmg` — start CMG (if enabled)
* `close` — run Closure

---

## 10) Notes on Profiles (P0–P4)

* **P0:** gentle, fewer choices; defaults on.
* **P1–P2:** moderate options; CMG only if explicitly enabled.
* **P3–P4:** full surface; advanced prompts (e.g., protocol IDs, EDGE/INTUIT toggles).

---

## 11) References

* Kernel shim: `kernel/30_rituals.md`
* CMG runtime: `protocols/cmg_runtime.md`
* AAR-C worksheet: `protocols/templates/aar_c_worksheet.md`
* MSRL runtime: `protocols/msrl_runtime.md`
* Beacons & Integrity: `kernel/10_beacons.md`, *AI Integrity Protocol*, *PCE*

---

**Purpose in one line:** Keep the entry simple, the moves crisp, and the exits clean—so practice stays light where it should, and rigorous where it matters.
