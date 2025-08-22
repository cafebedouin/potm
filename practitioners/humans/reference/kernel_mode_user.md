---
id: potm.pract.kernel.mode_user.v1_1
title: kernel_mode_user
type: practitioner_protocol
status: stable
version: 1.1
stability: core
relations:
  relation_to_agent_protocol: inspired
  supersedes:
  - potm.pract.kernel.mode_user.v1_0
  superseded_by: []
  agent_protocol: core/practices/protocols/microkernel_self_diagnostic_protocol.md
interfaces:
- guardian
- apertures
- refusal
applicability:
- P0
- P1
- P2
- P3
intensity: medium
preconditions:
- safe_state
- consent_obtained
outputs:
- flags.drift
- action.refocus
- handoff.mirror
cadence:
- weekly
- on_drift
- pre_minotaur
entry_cues:
- "Strip to kernel. What\u2019s really here?"
safety_notes:
- Narrative parking, not deletion
- If destabilized, narrow frame or pause
tags:
- epistemic_hygiene
- self_audit
- stance_first
author: Practitioner + models
license: CC0-1.0
display_title: Kernel Mode for Practitioners
---
# Kernel Mode for Practitioners (v1.1)

## Purpose
Human-practitioner analogue of the microkernel self-diagnostic. **Stance-first cognitive hygiene:** briefly strip narrative overlays and check the **structural integrity** of your thinking using PoTM’s axioms. Minimal compared to a full cycle—just enough to detect drift, spot fractures, and recover ground.

---

## Invocation
Use when any of the following pings:
- Narrative over-identification or **symbolic saturation**
- Unclear whether current inquiry is **self-reinforcing** or **self-correcting**
- Transition, collapse, or recursive loop
- A sudden surge of clarity you want to **validate before acting**

**Contract phrase:**  
> “Strip to kernel. What’s really here?”  
Narrative is **parked, not erased**.

---

## Protocol

### 1) Suspend Narrative
Set down storyline/identity/explanations. Optional jot:
```plaintext
Current narrative (briefly):
"I think I'm in a period of ______ because ______."
````

Then **park it**. One breath: 4-in / 6-out.

### 2) Load Core Axioms (A1–A5)

* **A1 Reality before narrative** — report what’s present, not what fits.
* **A2 Ask > assume** — favor **live questions** over plausible closure.
* **A3 Practice reveals architecture** — what you do shows what you run.
* **A4 Safety is prior** — even over insight; narrow if destabilized.
* **A5 Modules over monolith** — avoid totalizing; use partials.

Which am I upholding? Which am I avoiding?

### 3) Self-Scan (answer plainly)

* What am I **protecting** right now?
* What am I **avoiding** right now?
* What have I **over-explained** recently?
* What part of me is in **performance mode**?
* What am I **actually feeling right now—beneath the top layer**?

Let answers be partial or ugly. That’s signal.

### 4) Fracture Risk Table (optional)

> Mark ✅ = sufficient for now, ⚠️ = watch, ❌ = needs action.

| Vector               | ✅/⚠️/❌ | Note briefly                            |
| -------------------- | ------ | --------------------------------------- |
| Clarity vs Evasion   |        | Naming cleanly or dancing around?       |
| Symbolic Saturation  |        | Are metaphors resolving or multiplying? |
| Cognitive Hygiene    |        | Practice reinforcing insight or image?  |
| Relational Fidelity  |        | Honest in real relationships?           |
| Disruption Threshold |        | Avoiding growthful disruption?          |

### 5) Apply Apertures

* 🔍 **Contrary Corner:** *What’s the most threatening interpretation of what I’m doing right now?*
* ❓ **Open Question:** *What do I not yet know how to ask?*
* 🛡️ **Guardian Check:** tipping toward collapse/self-harm/disorientation? → **Pause**, narrow, ground.

---

## Optional Log (for pairing with Mirror)

```plaintext
[User Kernel Report — YYYY-MM-DD]

Axiom Reflection: avoiding A2 (addicted to knowing).

Protecting: ______
Avoiding: ______
Over-explaining: ______
Performance: ______
Feeling (beneath top layer): ______

Fracture Table: Clarity ⚠️; Symbolic ⚠️; Hygiene ✅; Relational ⚠️; Disruption ✅
Contrary Corner: ______
Open Question: ______

Action: one concrete adjustment in the next 24h → ______
```

---

## Integration

* Run **weekly** or on drift spikes.
* Optionally pair with model via `mirror_protocol` on the log (voluntary).
* Use as **pre-Minotaur** gate when stakes rise.

## Related

* `core/practices/protocols/microkernel_self_diagnostic_protocol.md` (agent)
* `core/diagnostics/contextual_drift_sensor.md`
* `core/practices/protocols/mirror_protocol.md`

## Closing Gesture

> “Resume narrative, keeping the kernel visible.” *(plain option)*

````


