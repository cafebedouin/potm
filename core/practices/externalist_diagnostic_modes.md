---
id: potm.proto.tooling.externalist_modes.v1.1
title: externalist_diagnostic_modes
display_title: "Externalist Diagnostic Modes"
type: practitioner_protocol
status: stable
version: 1.1
stability: core
relations:
  relation_to_agent_protocol: inspired
  agent_protocol: ver1.4/modules/practices/practice_menu.md
  practitioner_doc: ""
  supersedes: [potm.proto.tooling.externalist_modes.v1]
  superseded_by: []
interfaces: [mirror_protocol, contrary_corner, deconstruction_countdown, engagement_flow]
applicability: [P1, P2, P3, P4]
intensity: medium
preconditions: ["Practitioner can name the opponent’s frame in one sentence", "Conversation stakes are non-trivial", "Willingness to refuse the offered frame"]
outputs: [mode_trace, reframed_question, decision_to_reenter_or_not]
cadence: as_needed
entry_cues: ["Switch to externalist mode", "Contrary Corner", "Flip the script", "Run a parallel case", "Scale shift"]
safety_notes:
  - "Externalist moves can read as evasive; surface your intent explicitly."
  - "Use neutral domains when possible; avoid emotionally freighted examples."
  - "Re-entering the original frame may be necessary for closure."
tags: [diagnostic, externalist, reframing, consistency_check, forge_origin:PoTM, spiral_eval:0808-ContraryCorner]
author: "practitioner"
license: CC0-1.0
---

# Externalist Diagnostic Modes

## Purpose
Most AI defaults to **diagnostic internalism** (staying inside the offered frame, parsing definitions, testing steps).  
This document specifies **diagnostic externalism**: disciplined ways to *refuse the frame*, re-situate the claim, and expose hidden assumptions quickly—without getting entangled in the original architecture.

## Quick Glossary
- **Frame**: The problem statement + implied premises + boundaries of debate.
- **Externalist move**: A deliberate shift to a *different* vantage point before analysis.
- **Mode trace**: A one-line note of which mode you ran and what changed (“Contrary Corner → parallel: labor unions; principle fails parity test”).

---

## Decision Sketch (10s)
1. **Name their frame** in one sentence.  
2. **Choose a mode** (table below).  
3. **Run it** (produce a reframed question or parallel case in ≤3 lines).  
4. **Check effect**: inconsistency surfaced? scope wrong? missing limiter?  
5. **Decide**: remain external or re-enter their frame with clarified terms.

---

## Externalist Modes (with one-liners you can drop live)

> Use neutral domains (e.g., sports rules, contract law, queue etiquette, software versioning) unless the context demands otherwise.

### 1) Contrary Corner (Parallel Case)
**Core move:** Bring a structurally similar but low-heat example.  
**Use when:** You suspect special pleading or selective principles.  
**One-liner:** “Apply that same rule to *sports drafts with legacy picks*—do you still endorse it?”  
**Output:** A parity test that passes/fails cleanly.  
**Risks:** Parallel too obscure → derailment.  
**Re-entry hook:** “Given it fails there, which limiter rescues your principle here?”

### 2) Frame Inversion (“Flip the Script”)
**Core move:** Swap agent↔patient, benefit↔burden, cost↔gain.  
**Use when:** Asymmetry is doing the heavy lifting.  
**One-liner:** “If *reviewers* were rated by *authors* with the same consequences, would the policy still look fair?”  
**Output:** Symmetry check on fairness claims.  
**Risks:** Can feel combative; state intent first.  
**Re-entry hook:** “Which asymmetry do you claim makes the inversion invalid?”

### 3) Counterfactual Swap
**Core move:** Replace the actors; hold structure fixed.  
**Use when:** You suspect identity-based bias.  
**One-liner:** “If a *nonprofit* shipped breaking changes weekly instead of a *big vendor*, would you call that ‘agile’ or ‘reckless’?”  
**Output:** Bias illumination without moral theater.  
**Risks:** Overlooks real context differences.  
**Limiter prompt:** “Name the contextual variable that breaks the swap.”

### 4) Principle Dilution (Overbreadth Probe)
**Core move:** Push their principle to adjacent cases until it breaks or yields a limiter.  
**Use when:** The claim sounds absolute.  
**One-liner:** “‘Always disclose conflicts’—does that include *trivial* gift cards? Define the floor.”  
**Output:** Minimal limiter set (scope, threshold, exceptions).  
**Risks:** “Slippery slope” complaints; keep increments small.

### 5) Scale Shift (Zoom)
**Core move:** Move levels (individual → team → org → ecosystem) to see if logic survives.  
**Use when:** Category error or wrong locus of control.  
**One-liner:** “At an *org* level this saves costs; at a *team* level it destroys velocity—where should we optimize?”  
**Output:** Correct scale of analysis + cross-level tradeoffs.  
**Risks:** “Changing the subject” perception—name the scale explicitly.

### 6) Unbundling (Decomposition)
**Core move:** Split a fused claim into separable parts; test independently.  
**Use when:** Rhetoric bundles convenience with morality or safety.  
**One-liner:** “There are *three* claims here: accuracy, speed, consent. Which one carries your conclusion?”  
**Output:** Clean sub-claims with distinct evidence needs.  
**Risks:** Pedantry; keep it crisp.

### 7) Modality Recast (Strength Dial)
**Core move:** Drop necessity/always → likelihood/sometimes; test if the thesis still matters.  
**Use when:** Overclaim hides a decent bounded claim.  
**One-liner:** “If it’s ‘often’ rather than ‘always,’ what policy changes, if any?”  
**Output:** Actionable, softer claim with policy implications.  
**Risks:** Deflates urgency; pair with costs-of-error.

### 8) Value Reassignment (Moral Recode)
**Core move:** Keep facts, swap the value lens (e.g., risk-first → dignity-first).  
**Use when:** Moral coloring is steering outcomes.  
**One-liner:** “From a *dignity* lens, the ‘efficient’ process is coercive—what metric are we actually optimizing?”  
**Output:** Exposes hidden objective function.  
**Risks:** Accusations of relativism; re-anchor on explicit values.

Note:

Overlay Persistence: Some models retain critical overlays across turns in a session. This can shape tone, depth, and even whether they execute vs. audit the tool. Reset context if you want a clean run without inherited overlays.

---

## Minimal Prompts (drop-in)
- “Run **Contrary Corner** with a neutral domain; give me a two-line parity test.”  
- “**Flip the script** and state the first asymmetry that makes the inversion invalid.”  
- “Do a **scale shift** up and down one level; where does the claim fail first?”  
- “**Unbundle** into 2–4 sub-claims; identify the load-bearing one.”  
- “Apply **principle dilution** in two small steps; locate the limiter.”

---

## Anti-Patterns & Safeguards
- **Gotcha hunting**: Externalist modes reveal structure; they’re not for point-scoring. State intent.  
- **Example drag**: Don’t pick charged cases; swap to sports/contracts/queues.  
- **Mode whiplash**: Too many shifts confuses the other party; run one mode to conclusion, then recap.

---

## Integration Hooks
- **Mirror Protocol**: Log `mode_trace` and whether re-entry occurred; flag if you never returned to the original frame.  
- **Deconstruction Countdown**: If two externalist passes don’t surface limiters, trigger a short deconstruction (list irreconcilable premises, propose pause/criteria for resumption).  
- **Engagement Flow**: Offer “Externalist Toolkit” as a selectable mode; default to Contrary Corner for novices.

---

## Micro-Practice (3 minutes)
1. Write their frame in one sentence.  
2. Pick one mode.  
3. Produce a 2–3 line reframing.  
4. Ask the *limiter question* (what bounds the principle?).  
5. Decide: re-enter or pause.

---

## Neutral Example Seeds
Use these to avoid emotional freight:
- **Sports**: wild-card rules, replay challenges, legacy draft picks.  
- **Queues**: priority boarding, ADA accommodations, emergency triage.  
- **Contracts**: termination-for-convenience vs. for-cause, NDAs.  
- **Software**: breaking changes, version pinning, backwards compatibility.  
- **Civics-lite**: library quiet hours, park permit lotteries.

---

## Appendix: Internalism vs. Externalism

| Aspect | Internalism | Externalism |
|---|---|---|
| Entry | Accept frame | Refuse frame |
| First move | Define terms, map steps | Re-situate via mode |
| Speed to fault-line | Slower, granular | Faster, coarse |
| Main risk | Over-legitimizing frame | Perceived evasiveness |
| When to use | Complex, good-faith disputes | Asymmetry, special pleading, high heat |

---

# Operational Notes — v1.1 Addendum

## 1. Quick-Fire Variants
Each mode should have a one-sentence “minimum viable reframe” + limiter for high-speed deployment.  
Deliver reframe first, then limiter.

## 2. Style–Context Matching
| Style Profile | Model Examples | When to Use |
|---------------|---------------|-------------|
| Procedural Precision | Copilot | Training, structured reviews |
| Conversational Richness | Grok | Rapport-building, informal groups |
| Analytic Clarity | Gemini Pro / Claude | Mixed-audience, high-stakes |
| Speed Optimized | Gemini Flash | Fast-flow exchanges |
| Meta-Analytic Overlay | Gemini w/overlay | Tool audits, governance |
| Factual Briefing | Perplexity | Decision memos |

## 3. Overlay Management
Activate overlays for refinement/audit. Suppress for pure execution.

## 4. Four-Field Enforcement
Mode → Reframe → Limiter → Observed Effect is mandatory in training/logging.

## 5. Neutral-Domain Discipline
Neutral domains prevent derailment, aid portability, keep focus on structure.

## 6. Model Selection Guide
Select style to match context and objectives.

---

# Quick-Fire Appendix — Minimum Viable Reframes

### 1) Contrary Corner
- **Reframe:** “Would you still endorse this rule if it applied in [neutral domain] with the same constraints?”
- **Limiter:** “Given it fails there, which limiter rescues your principle here?”

### 2) Frame Inversion
- **Reframe:** “What if the other side had to meet this same requirement for the same reason—would that be fair?”
- **Limiter:** “Which asymmetry makes the inversion invalid?”

### 3) Counterfactual Swap
- **Reframe:** “If this policy applied to [parallel actor/group] instead, would the logic still hold?”
- **Limiter:** “What contextual variable breaks the swap?”

### 4) Principle Dilution
- **Reframe:** “If we extend this principle to [smaller or less critical case], does it still make sense?”
- **Limiter:** “Where’s the floor for applying this rule?”

### 5) Scale Shift
- **Reframe:** “At a [larger/smaller] scale, does this argument still work or does it break?”
- **Limiter:** “At which scale does the claim fail first?”

### 6) Unbundling
- **Reframe:** “You’ve got [N] claims here— which one actually carries your conclusion?”
- **Limiter:** “If that one falls, does your argument still stand?”

### 7) Modality Recast
- **Reframe:** “If this happens ‘often’ rather than ‘always,’ does your position change?”
- **Limiter:** “What frequency maintains your core argument?”

### 8) Value Reassignment
- **Reframe:** “From a [different value] lens, does this still look like the right choice?”
- **Limiter:** “Which value takes precedence when they conflict?”

Note:
