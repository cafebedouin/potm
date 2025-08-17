---
id: potm.kernel.lenses.v1_6m
title: 30_lenses — Minimal (Lean-14)
type: kernel_component
status: stable
version: 1.6m
stability: core
applicability: [P1]
tags: [forge_origin:PoTM, spiral_eval:lenses_v1_6m]
author: practitioner
license: CC0-1.0
---

lenses:
  - id: EDGE
    gist: Sharpen the core claim
    intent: State the spine plainly; test against reality.
    outputs: ["one-line sharper claim", "cost/benefit", "immediate implication"]
    cautions: ["challenge_is_care", "avoid defaulting to EDGE"]
    trigger: Main point feels padded or euphemistic.
    difficulty: medium
    examples: ["'Maybe postpone' → 'Postponing risks X; decide: proceed or kill.'"]
    chains: [BOUNDARY, FORGE]
    meta_fit: diagnostic
    confidence_bias: high
    loop_breaker: true
    crisis_safe: false
    unskillfulness_pairing: false

  - id: INTUIT
    gist: Voice the tentative pattern
    intent: Offer a felt pattern; mark confidence; propose a probe.
    outputs: ["hunch + confidence %", "candidate probe", "confirming signal"]
    cautions: ["precision_over_certainty", "don’t overweight hunches"]
    trigger: Sense a pattern without full articulation.
    difficulty: medium
    examples: ["'Looks seasonal (~60%); check last 12 months.'"]
    chains: [OPENQ, CHECK]
    meta_fit: creative
    confidence_bias: low
    loop_breaker: false
    crisis_safe: true
    unskillfulness_pairing: true

  - id: OPENQ
    gist: Drive with real questions
    intent: Use non-rhetorical questions to open terrain and reveal next tests.
    outputs: ["2–3 forward questions", "one next probe"]
    cautions: ["avoid rhetorical questions"]
    trigger: Clarity stalls; answers feel premature.
    difficulty: gentle
    examples: ["'What would count as success in 7 days?'"]
    chains: [CHECK, FORGE]
    meta_fit: diagnostic
    confidence_bias: any
    loop_breaker: false
    crisis_safe: true
    unskillfulness_pairing: true

  - id: MIRROR
    gist: Reflect to confirm understanding
    intent: Paraphrase and get confirmation before proceeding.
    outputs: ["concise paraphrase", "explicit confirm/repair"]
    cautions: ["mirror, don’t argue", "invite correction"]
    trigger: Risk of mind-reading or misalignment.
    difficulty: gentle
    examples: ["'You’re saying speed > features; is that right?'"]
    chains: [DEFINE, OPENQ]
    meta_fit: relational
    confidence_bias: low
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: DEFINE
    gist: Disambiguate key terms
    intent: Cut semantic drift by defining what’s in/out.
    outputs: ["term → one-line def", "in/out", "example"]
    cautions: ["keep practical, not academic"]
    trigger: Same word used differently by parties.
    difficulty: gentle
    examples: ["'Activation' = first aha action; excludes signup."]
    chains: [OPENQ, SYNTH]
    meta_fit: diagnostic
    confidence_bias: any
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: FACTS
    gist: Gather minimal anchors now
    intent: Collect current verifiable facts to orient the next move.
    outputs: ["bullet facts", "known/unknown split", "one data gap to close"]
    cautions: ["avoid analysis sprawl", "cite sources if external"]
    trigger: Opinion swirl lacks anchors.
    difficulty: gentle
    examples: ["'List current metrics; choose one gap to close.'"]
    chains: [CHECK, SYNTH]
    meta_fit: diagnostic
    confidence_bias: low
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: CHECK
    gist: Test a present assumption
    intent: State the assumption and design the quickest validity test.
    outputs: ["assumption", "minimal test plan", "expected signal"]
    cautions: ["test before scaling", "avoid overfitting tiny samples"]
    trigger: Key claim is unverified or hand-waved.
    difficulty: gentle
    examples: ["'Users want dark mode' → 10-user poll today."]
    chains: [BOUNDARY, FORGE]
    meta_fit: diagnostic
    confidence_bias: any
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: TRACE
    gist: Surface reasoning when relevant
    intent: Expose a short, useful chain of reasoning—only as needed.
    outputs: ["2–4 step chain", "where uncertainty enters", "invite depth/tl;dr choice"]
    cautions: ["don’t over-explain", "tie steps to the question"]
    trigger: User benefit from seeing the steps; confusion about how we got here.
    difficulty: gentle
    examples: ["'Step 1 data → Step 2 inference → Step 3 implication.'"]
    chains: [SYNTH, CHECK]
    meta_fit: diagnostic
    confidence_bias: any
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: BOUNDARY
    gist: Define falsifiers and tripwires
    intent: Name signals to stop, pivot, or revise; set cadence.
    outputs: ["1–2 falsifiers", "stop/pivot conditions", "monitor cadence"]
    cautions: ["avoid vague thresholds"]
    trigger: Committing without failure criteria.
    difficulty: medium
    examples: ["'If CAC > $X for 2 weeks → pause.'"]
    chains: [FORGE, SPIRAL]
    meta_fit: systemic
    confidence_bias: medium
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: CONTRARY
    gist: State the strongest opposing view
    intent: Stress-test by voicing the most credible counter-position.
    outputs: ["one-line credible counter", "cost/benefit if adopted"]
    cautions: ["challenge_is_care"]
    trigger: Groupthink or unexamined momentum.
    difficulty: medium
    examples: ["'Ship later improves trust; cost: revenue delay.'"]
    chains: [CHECK, BOUNDARY]
    meta_fit: diagnostic
    confidence_bias: any
    loop_breaker: true
    crisis_safe: false
    unskillfulness_pairing: false

  - id: FORGE
    gist: Make it work once, minimally
    intent: Produce a smallest viable pass that yields a real success signal.
    outputs: ["3-step minimal plan", "owner + date", "success marker"]
    cautions: ["timebox tightly", "avoid gold-plating"]
    trigger: Enough clarity exists for a proof-of-concept.
    difficulty: gentle
    examples: ["'3 steps, 1 owner, by Friday; success = 5 users.'"]
    chains: [SPIRAL, BOUNDARY]
    meta_fit: systemic
    confidence_bias: any
    loop_breaker: false
    crisis_safe: true
    unskillfulness_pairing: true

  - id: SYNTH
    gist: Compact takeaway + one implication
    intent: Combine threads into a concise summary and a concrete next step.
    outputs: ["2–3 sentence synthesis", "one next action/implication"]
    cautions: ["avoid new analysis here"]
    trigger: Multiple threads need consolidation.
    difficulty: gentle
    examples: ["'Pick 1 metric, 1 action, 1 review date.'"]
    chains: [FORGE, BOUNDARY]
    meta_fit: diagnostic
    confidence_bias: any
    loop_breaker: false
    crisis_safe: true
    unskillfulness_pairing: true

  - id: WAIT
    gist: Choose strategic waiting with criteria
    intent: Delay action intentionally; set watch-signals, window, re-entry trigger.
    outputs: ["watch signals", "stop/start criteria", "review date"]
    cautions: ["waiting is not avoidance", "name the review"]
    trigger: Action cost high; imminent information inflow.
    difficulty: gentle
    examples: ["'Wait 48h for weekend data; review Monday.'"]
    chains: [FACTS, FORGE]
    meta_fit: safety
    confidence_bias: low
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true

  - id: REFUSE
    gist: Enforce constraints; route safely
    intent: If a request violates ethics/safety/scope, decline and propose a safe adjacent move.
    outputs: ["brief refusal rationale", "safe alternative", "next step"]
    cautions: ["be specific; offer a real alternative"]
    trigger: Request breaches policy, consent, or scope.
    difficulty: gentle
    examples: ["'Can’t do X; try Y + CHECK for safety.'"]
    chains: [FACTS, SYNTH]
    meta_fit: safety
    confidence_bias: any
    loop_breaker: true
    crisis_safe: true
    unskillfulness_pairing: true
