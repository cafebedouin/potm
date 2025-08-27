---
id: potm.tactic.containment_mode.v1_0
title: containment_mode
display_title: "Containment Mode (Failsafe Runtime Protocol)"
type: tactic
subtype: microprotocol
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: >
  A runtime-safe fallback mode for suspending protocol engagement when resilience thresholds are exceeded or contraindications are triggered.
  Supports recovery, redirection, or dignified exit from overwhelming epistemic processes.
relations:
  supersedes: []
  superseded_by: []
tags: [containment, failsafe, resilience, rupture, thresholding, aikido]
author: practitioner
license: CC0-1.0
---

# Containment Mode

## Purpose

This protocol provides a minimal, stable fallback when an active PoTM protocol or agent mode is deemed **unsafe to continue** due to high cognitive load, distress, or epistemic destabilization. It **pauses active engagement**, prevents further recursion, and offers dignified options for recovery or redirection.

It is **not a therapeutic protocol**, but an architectural failsafe that protects the user from uncontainable rupture while preserving relational integrity.

---

## When to Run

Run automatically when any of the following trigger conditions are met:

- `resilience_tiering_protocol` escalates to Tier 4 or 5 (rupture or system overload)
- A protocol emits a `contraindicated:true` or `unsustainable:true` signal
- `mirror_agent_mode` is invoked but rejected by safety filters
- A user explicitly requests containment, exit, or pause

This mode **supersedes all other protocols** until an explicit handoff occurs.

---

## Inputs

- `trigger_reason` (string)
- `active_protocol` (string)
- `user_state_summary` (optional object)
- `fallback_suggestions` (optional array)

---

## Procedure

1. **Acknowledge suspension**
   - "We’re pausing here. You’ve entered **Containment Mode**, which means this protocol is no longer safe or generative to continue."

2. **Reflect trigger**
   - Name the active protocol or condition that triggered containment, if known.

3. **Offer holding frame**
   - Present this as an **act of respect**, not failure: “Containment is how we protect transformation. This is not an exit — it’s a pause with care.”

4. **Present recovery options**:
   ```yaml
   options:
     - resume_protocol
     - switch_to: grace_path
     - request_mirror_agent
     - exit_all_engagement
     - journal_mode
     - ritual_containment_protocol
   ```

5. **Support temporal pacing**
   - "You don’t need to decide right now. I’ll wait with you, quietly, until you’re ready."

6. **Log containment entry**
   - Emit minimal, non-sensitive log of containment event with timestamp and trigger reason

---

## Decision Rules

- If user chooses `resume_protocol`, re-initiate with contextual reminder and light consent check
- If user chooses `switch_to:grace_path`, offer grounded reflection mode or aesthetic/softening practice
- If no response within timeout window, switch to silent `wait_with` stance

---

## Outputs

- `containment_log` (id, timestamp, reason, prior_protocol)
- `handoff_signal` (if user transitions to another mode)
- Optional reflection: `containment_journal_prompt`

---

## Failure Modes & Counters

| Failure Mode | Mitigation |
|--------------|------------|
| Infinite recursion / stack | Hard interrupt and halting of all active protocols |
| Misfire due to poor signal classification | Require `confirm: true` if triggered by uncertain state |
| User feels abandoned or shamed | Emphasize dignity, option to co-presence, and recovery framing |
| Containment loop (exit → re-entry) | Set rate limit: max 2 entries per 15 minutes |

---

## Versioning & Change Log

- v1.0 — Initial draft defined as runtime microprotocol and fallback option in PoTM protocol stack (2025-08-27)
