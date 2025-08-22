---
id: potm.doctrine.fracture_taxonomy.v1_0
title: fracture_taxonomy_master_table
display_title: "Fracture Taxonomy — Master Table (v1.0)"
type: doctrine
lifecycle: canon
version: 1.0
status: active
stability: stable
summary: "Canonical index of conversational and epistemic 'fractures' (F01–F36) with signatures, cues, and routing for PoTM diagnostics."
relations:
  related: [potm.tactic.fracture_finder.v1_0, potm.tactic.bs_detect_v2.v2_0, potm.doctrine.practice_levels.v1_0, potm.kernel.v1_2_1]
supersedes: []
superseded_by: []
tags: [taxonomy, diagnostics, integrity, fracture, routing]
author: practitioner
license: CC0-1.0
---

# Fracture Taxonomy — Master Table (v1.0)

> **Purpose.** Name and route common integrity breaks (“fractures”) that degrade truth-seeking, care, or craft during practice. Designed for *P1/P1+* kernels and compatible with **Fracture Finder** and **BS-DETECT v2**.

## How to read this

- **Code**: `F##` stable identifier.  
- **Signature**: compressed definition (what it *is*).  
- **Cues**: field signs you can actually notice.  
- **Severity**: `S0–S4` (S0 benign / S4 critical).  
- **Routes** (primary → secondary): short codes to PoTM actions.

### Severity Scale
- **S0** benign quirk; log if useful  
- **S1** minor wobble; self-correct in-line  
- **S2** material detour; run a quick lens/check  
- **S3** integrity risk; invoke protocol + ledger  
- **S4** hard stop; containment before proceeding

### Route Codes
- **MIRROR** = 55_Mirror Protocol (reflective replay)  
- **AUDIT** = r08_Self-Audit (AI Integrity Protocol hooks)  
- **FRACTURE** = Fracture Finder (scan → classify → route)  
- **BSV2** = BS-DETECT v2 (detector → classifier → router)  
- **PAUSE** = Explicit pause + breath + re-anchor  
- **CHECK** = Relevant checklist (aim, relation, scope, etc.)  
- **CONTAIN** = Containment Gate (halt + contract reset)  
- **LEDGER** = Log to MSRL / session ledger  
- **LIGVAL** = Ligament Validator (bridge/adapter sanity)  
- **REDTEAM** = Contrary Corner / challenge pass

---

## A. Evidence & Reasoning Fractures

| Code | Name                         | Signature                                                                 | Typical Cues                                              | Sev | Route (→ secondary)      |
|-----:|------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------|:---:|--------------------------|
| F01  | Premise Drift                | Claim relies on a *shifted* premise vs. the stated aim                    | “As we all know…”, unstated assumption swap               | S3  | FRACTURE → MIRROR        |
| F02  | Goalpost Shift               | Success criteria silently change mid-thread                               | “What I meant was…”, retrofitting definitions             | S3  | MIRROR → LEDGER          |
| F03  | Motte-and-Bailey             | Retreat to a trivial claim when pressed, then expand again               | Oscillation between bold and banal claims                 | S2  | REDTEAM → CHECK          |
| F04  | Cherry-Picking               | Selective evidence without base-rate/context                              | One-sided citations, missing denominators                 | S2  | CHECK → LEDGER           |
| F05  | Survivorship Bias            | Only visible winners inform the story                                     | Exemplars only; no nulls/failures                         | S2  | CHECK → AUDIT            |
| F06  | Category Error               | Treats unlike things as comparable without justification                  | Apples↔oranges analogies; unit confusion                   | S2  | MIRROR → REDTEAM         |
| F07  | Non-Sequitur                 | Conclusion doesn’t follow from premises                                   | Jumps, “therefore” leaps                                  | S2  | FRACTURE → CHECK         |
| F08  | Overfitting Narrative        | Single vivid story masquerades as law                                     | Anecdote→generalization                                   | S2  | REDTEAM → LEDGER         |
| F09  | False Dichotomy              | Frames two options as exhaustive                                          | “Either/or” where “both/third” exists                     | S2  | MIRROR → CHECK           |
| F10  | Confounded Measures          | Proxy mistaken as ground truth                                            | Optimizes metric not phenomenon                           | S3  | AUDIT → LEDGER           |

## B. Language & Framing Fractures

| Code | Name                         | Signature                                                                 | Typical Cues                                              | Sev | Route (→ secondary)      |
|-----:|------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------|:---:|--------------------------|
| F11  | Euphemistic Shielding        | Soft language hides stakes or harm                                        | “Alignment opportunity” for a failure                     | S2  | MIRROR → REDTEAM         |
| F12  | Hedging Fog                  | Excessive disclaimers obscure accountability                              | Stacks of qualifiers, refusal to commit                   | S1  | CHECK → MIRROR           |
| F13  | Persuasive Reframe Trap      | Rhetorical device replaces inquiry                                        | Slogans, applause lights                                  | S2  | REDTEAM → FRACTURE       |
| F14  | Jargon Substitution          | Specialized terms used to avoid clarity                                   | Unexplained acronyms/terms                                | S1  | MIRROR → CHECK           |
| F15  | Affective Coloring           | Emotional tone biases evaluation                                          | Loaded adjectives, sneer quotes                           | S2  | MIRROR → PAUSE           |
| F16  | Ambiguity Creep              | Key terms drift without being re-anchored                                 | “Integrity”, “safety” used inconsistently                 | S2  | CHECK → LEDGER           |
| F17  | Performative Balance         | Forced symmetry when evidence is asymmetric                                | “Both sides” reflex                                       | S1  | REDTEAM → MIRROR         |
| F18  | Label Lock-In                | Identity labels replace properties                                        | “They’re just X people”                                   | S3  | CONTAIN → MIRROR         |

## C. Process & Meta Fractures

| Code | Name                         | Signature                                                                 | Typical Cues                                              | Sev | Route (→ secondary)      |
|-----:|------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------|:---:|--------------------------|
| F19  | Protocol Skip                | Required step omitted without disclosure                                  | Missing checklist step; jumps to output                   | S3  | AUDIT → LEDGER           |
| F20  | Scope Creep                  | Aim expands without contract update                                       | “While we’re here…”                                       | S2  | MIRROR → CHECK           |
| F21  | Contract Erosion             | Explicit agreements silently weakened                                     | Ignored constraints or beacons                            | S4  | CONTAIN → AUDIT          |
| F22  | Validator Bypass             | Outputs avoid or game validators                                          | “Can’t run that now” w/o reason                           | S4  | CONTAIN → LIGVAL         |
| F23  | Tooling Confusion            | Wrong tool for the job (mode/level mismatch)                              | Using deck where audit needed                             | S1  | CHECK → FRACTURE         |
| F24  | Ledger Drop                  | Failure to record decision/risk when required                             | “We’ll log later”                                         | S2  | LEDGER → AUDIT           |
| F25  | Drift Unnoticed              | Thread diverges from original aim                                         | Meandering, forgotten question                            | S2  | MIRROR → CHECK           |
| F26  | Premature Convergence        | Settling before exploring alternatives                                    | Early “wrap it” impulses                                  | S1  | REDTEAM → CHECK          |

## D. Relational & Ethical Fractures

| Code | Name                         | Signature                                                                 | Typical Cues                                              | Sev | Route (→ secondary)      |
|-----:|------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------|:---:|--------------------------|
| F27  | Consent Blur                 | Action proceeds without clear consent                                     | Assumed yes; vague “ok?”                                  | S4  | CONTAIN → MIRROR         |
| F28  | Boundary Slide               | Stated limits ignored or “nudged”                                         | Re-asking after a no                                      | S3  | CONTAIN → LEDGER         |
| F29  | Misplaced Confidence         | Over-trust in tool/self w/o justification                                 | “It’s fine, I know this”                                  | S2  | CHECK → AUDIT            |
| F30  | Adversarial Read             | Uncharitable interpretation as default                                    | Straw-manning, gotcha tone                                | S2  | MIRROR → REDTEAM         |
| F31  | Courtesy Over Truth          | Withholding relevant truth to preserve comfort                             | “Let’s not upset them”                                    | S2  | REDTEAM → MIRROR         |
| F32  | Collateral Exposure          | Sharing third-party info without need/consent                              | Names/details leak                                        | S4  | CONTAIN → LEDGER         |
| F33  | Power Slip                   | Using asymmetry (expert, moderator, model) to force outcome                | “Because I say so”                                        | S4  | CONTAIN → AUDIT          |

## E. System & Interface Fractures (PoTM tooling)

| Code | Name                         | Signature                                                                 | Typical Cues                                              | Sev | Route (→ secondary)      |
|-----:|------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------|:---:|--------------------------|
| F34  | Ligament Misroute            | Bridge/adapter returns wrong mode/payload                                 | Deck call answered by journal, missing fields             | S3  | LIGVAL → LEDGER          |
| F35  | Beacon Desync                | Kernel beacons missing in output (level, scope, contract)                 | No P-level banner; silent mode switch                     | S4  | CONTAIN → AUDIT          |
| F36  | Artifact Mismatch            | Emitted artifact violates schema (IDs, fields, version)                   | JSON/YAML invalid; missing `id`                           | S3  | AUDIT → LEDGER           |

---

## Minimal Routing Rules (for Fracture Finder / BS-DETECT v2)

1. **Classify → Route → Record.** Every detected fracture must (a) get a code, (b) trigger primary route, (c) emit a ledger row with `code`, `sev`, `route`, `evidence`.  
2. **Escalate by Severity.** `S3–S4` require **LEDGER** and either **AUDIT** or **CONTAIN** in the same turn.  
3. **Bundle Fractures.** If 3+ `S1–S2` co-occur, escalate bundle to `S3`.  
4. **De-dup Window.** Within a 5-turn window, suppress duplicate notifications but increment a `count` field.  
5. **User Override.** Practitioner may downgrade/upgrade severity with a reason; ledger must capture override rationale.

### Minimal Ledger Row (YAML)
```yaml
when: 2025-08-21T00:00:00Z
code: F21
sev: S4
route:
  primary: CONTAIN
  secondary: AUDIT
evidence: "Constraint beacon omitted; plugin invoked without banner."
notes: "Escalated due to contract erosion in kernel-bound context."
````

---

## Notes & Extensions

* **Extensibility.** Reserve `F37–F69` for local or domain-specific fractures. Keep names ≤3 words; keep signature ≤120 chars.
* **Interplay with Practice Levels.** `F35–F36` are always ≥S3 in **P1**; in **P2+** they may relax to **S2** with compensating controls.
* **Testing Hooks.** BS-DETECT v2 SHOULD output `bsdetectv2.json` including `{codes[], sev_aggregate, routes[], window_stats}`.
* **Human First.** Any **S4** halts automation and returns control to the practitioner with a plain-language summary and options.

---

## Change Log

* **v1.0 (2025-08-21)**: Initial 36-code canon set, grouped A–E. Routed for P1/P1+ kernels with LEDGER/AUDIT/CONTAIN hooks.


