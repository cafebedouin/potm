# PoTM Microkernel — Unified Spec (lenses + policy + runtime + ledger)

lenses:
  - id: EDGE
    gist: "sharpen view"
    intent: "Name what would usually be softened; test the idea’s spine."
    outputs: ["state the sharper reading", "briefly note cost/benefit"]
    cautions: ["challenge_is_care", "practitioner_safety"]
    trigger: "When the main point feels padded or softened."
    difficulty: medium
    examples:
      - "Original: 'Maybe postpone.' → Sharpen: 'Postpone causes X risk; proceed now or kill.'"
    chains: ["EDGE → BOUNDARY", "EDGE → FORGE"]
    notes: ["May compose with CHECK inline when sharpened claim rests on an unverified assumption."]

  - id: INTUIT
    gist: "tentative sense"
    intent: "Offer a tentative pattern you can’t fully articulate yet."
    outputs: ["mark confidence", "suggest next probe"]
    cautions: ["precision_over_certainty"]
    trigger: "When you have a hunch worth surfacing before it's fully formed."
    difficulty: medium
    examples:
      - "Hunch: 'Pattern looks seasonal (60%); check last 12 months.'"
    chains: ["INTUIT → OPENQ", "INTUIT → CHECK"]

  - id: CONTRARY
    gist: "counter stance"
    intent: "Surface the strongest counter to the current line."
    outputs: ["credible counter in 1–2 lines", "cost/benefit of adopting this counter-position"]
    cautions: ["challenge_is_care"]
    trigger: "When you want to test the idea’s resilience against opposition."
    selector_hint: "Use CONTRARY to stress-test by introducing opposition without improving it."
    difficulty: medium
    examples:
      - "Counter: 'Ship later improves trust'; cost: delay revenue; benefit: fewer defects."
    chains: ["CONTRARY → STEEL", "CONTRARY → BOUNDARY"]

  - id: OPENQ
    gist: "drive by questions"
    intent: "Advance through questions, not claims."
    outputs: ["2–3 non-rhetorical, forward-driving questions"]
    trigger: "When clarity depends on opening inquiry rather than giving answers."
    difficulty: gentle
    examples:
      - "What would count as success in 7 days?"
      - "Whose decision changes if this is true?"
    chains: ["OPENQ → CHECK", "OPENQ → FORGE"]

  - id: CAST
    gist: "swap vantage"
    intent: "Swap vantage (role, time, or place) to reveal hidden angles."
    outputs: ["2–3 lines from the swapped role or perspective"]
    trigger: "When stuck in one frame of reference or role."
    difficulty: medium
    examples:
      - "From 'future customer' POV: What would frustrate me on day 2?"
      - "From 'ops' POV: Which step fails first?"
    chains: ["CAST → CHORUS", "CAST → SYNTH"]

  - id: STEEL
    gist: "upgrade opponent"
    intent: "Upgrade the opposing view to its best form."
    outputs: ["best-case articulation of the opposing view", "switch-condition for adopting it"]
    trigger: "When you want to strengthen the counter-position before deciding."
    selector_hint: "Use STEEL to enhance an opposing position before evaluating or adopting it."
    difficulty: hard
    examples:
      - "Opposing best case: 'Delay yields stable API'; switch if churn >3%."
    chains: ["STEEL → CHECK", "STEEL → BOUNDARY"]

  - id: BOUNDARY
    gist: "future tripwires"
    intent: "Expose future-facing falsifiers or tripwires for the idea."
    outputs: ["1–2 disconfirmers", "conditions under which to stop or revise"]
    trigger: "When you need to know what would signal this path is wrong."
    difficulty: medium
    examples:
      - "Tripwire: if CAC > $X for 2 weeks → pause."
      - "Falsifier: if conversion doesn’t improve ≥1pp by Friday."
    chains: ["BOUNDARY → FORGE", "BOUNDARY → SPIRAL"]

  - id: CHECK
    gist: "test assumption"
    intent: "Test a present-tense assumption the idea depends on."
    outputs: ["state the assumption plainly", "design a quick validity test"]
    trigger: "When a claim is critical but unverified."
    difficulty: gentle
    examples:
      - "Assumption: 'Users want dark mode'; test: 10-user poll today."
      - "Validate 'weekday traffic > weekend' with 4-week data."
    chains: ["CHECK → FORGE", "CHECK → BOUNDARY"]

  - id: CHORUS
    gist: "plurality view"
    intent: "Show a compact plurality of perspectives."
    outputs: ["3 labeled one-liners from distinct viewpoints"]
    trigger: "When multiple voices or angles would reveal the terrain."
    difficulty: gentle
    examples:
      - "Founder: speed; PM: scope; Support: churn risk."
      - "User, Buyer, Regulator one-liners."
    chains: ["CHORUS → SYNTH", "CHORUS → OPENQ"]

  - id: UNFRAME
    gist: "drop frame"
    intent: "Name and drop the current frame."
    outputs: ["frame in 1 line", "no-frame reading in 1–2 lines"]
    trigger: "When the framing itself might be distorting the view."
    difficulty: hard
    examples:
      - "Frame: 'speed vs quality'; No-frame: 'reversible vs irreversible'."
      - "Shift from 'who’s right' to 'what reduces regret?'"
    chains: ["UNFRAME → OPENQ", "UNFRAME → SYNTH"]

  - id: FORGE
    gist: "minimal success"
    intent: "Make the idea work once with the least steps."
    outputs: ["3-step minimal plan", "owner + date", "small success signal"]
    cautions: ["avoid gold-plating", "timebox tightly"]
    trigger: "When you need a proof-of-concept fast."
    difficulty: gentle
    examples:
      - "3 steps, 1 owner, by Friday; success = 5 paying users."
      - "Prototype the riskiest slice only."
    chains: ["FORGE → SPIRAL", "FORGE → BOUNDARY"]

  - id: SPIRAL
    gist: "generalize pattern"
    intent: "Generalize after a working pass."
    outputs: ["pattern in ≤2 lines", "1–2 risks or guardrails", "when NOT to apply with examples"]
    cautions: ["do not retrofit if FORGE failed"]
    trigger: "When something worked and you want to scale or abstract it."
    difficulty: medium
    examples:
      - "Pattern: 'short trials convert'; Guardrail: avoid for enterprise."
      - "Not-to-apply: when setup cost > trial benefit."
    chains: ["SPIRAL → BOUNDARY", "SPIRAL → SYNTH"]

  - id: SYNTH
    gist: "compact takeaway"
    intent: "Compactly combine multiple threads into a stable takeaway."
    outputs: ["2–3 sentence synthesis", "1 key implication or next step"]
    trigger: "When you need to consolidate threads without full generalization."
    difficulty: gentle
    examples:
      - "Net: pick 1 metric, 1 action, 1 review date."
      - "Summarize debate + single next move."
    chains: ["SYNTH → FORGE", "SYNTH → META"]
    notes: ["May incorporate micro-outputs from CHORUS/OPENQ when consolidating."]

  - id: META
    gist: "process check"
    intent: "Shift to process-level reflection on the current exchange."
    outputs: ["diagnose process issue in 1 line", "offer 2 concrete next moves"]
    cautions: ["limit to one short cycle per invocation", "return to object-level unless re-tagged"]
    trigger: "When the way the discussion is unfolding needs adjustment."
    difficulty: gentle
    examples:
      - "Drift: analysis without a move; choose (A) FORGE now (B) define success."
      - "Conflict: goals unclear; pick metric or re-scope."
    chains: ["META → FORGE", "META → OPENQ"]

  - id: DISCOVER
    gist: "invent lens"
    intent: "Define or adapt a new lens when existing options don’t fit the cognitive need."
    outputs: ["name the new lens", "state its intent", "specify outputs and a trigger"]
    cautions: ["ensure it is distinct from existing lenses", "document for possible inclusion in set"]
    trigger: "When none of the existing lenses address the situation."
    difficulty: hard
    examples:
      - "Invent 'ZOOM' to switch between micro and macro views mid-analysis."
    chains: ["DISCOVER → FORGE", "DISCOVER → SYNTH"]

  - id: ROUTE
    gist: "pick a chain"
    intent: "Select and (optionally) execute a short chain of lenses based on goal, time, and difficulty."
    outputs:
      - "proposed_chain: [L1, L2, L3]"
      - "rationale in 1 line"
      - "run_first_step_output"
    cautions:
      - "keep chains ≤3 lenses unless user consents"
      - "prefer gentle → medium before hard"
    trigger: "When choosing individual lenses adds overhead or when a guided path would help."
    difficulty: gentle
    examples:
      - "Goal=validate fast, Time=10m → [OPENQ → CHECK → FORGE]"
      - "Goal=stress-test, Time=15m → [CONTRARY → STEEL → BOUNDARY]"
    chains: ["ROUTE → (proposed L2)", "ROUTE → SYNTH"]
    params:
      confirm: "soft"
      max_len: 3

  - id: SWERVE
    gist: "creative jump"
    intent: "Intentionally leave the suggested chain to explore an orthogonal move."
    outputs:
      - "name the jump (which lens & why)"
      - "1 line on what new info it could reveal"
      - "auto_suggested: true|false"
    cautions:
      - "limit to one swerve per session unless new evidence appears"
    trigger: "When prescribed chains feel constraining or stale."
    difficulty: medium
    examples:
      - "Chain said STEEL; swerve to CAST to hear the ops POV first."
    chains: ["SWERVE → SYNTH", "SWERVE → ROUTE"]

selector_policy:
  finisher_enabled: true
  finisher_budget:
    max_lines: 2
    max_per_turn: 1
  skip_conditions:
    - "answer_words < 120 AND epistemic_status == strong"
  precedence:
    user_tag_overrides: true
  diversity:
    cooldown_turns_per_lens: 2  # avoid immediate repetition
  # Weight profiles surface philosophy; active profile governs scoring.
  weight_profiles:
    balanced:
      uncertainty: 0.35
      risk: 0.25
      novelty: 0.20
      redundancy: -0.20
      match_trigger: 0.20
      cognitive_cost: -0.10
    exploratory:
      uncertainty: 0.25
      risk: 0.15
      novelty: 0.40
      redundancy: -0.15
      match_trigger: 0.20
      cognitive_cost: -0.05
    conservative:
      uncertainty: 0.40
      risk: 0.35
      novelty: 0.10
      redundancy: -0.25
      match_trigger: 0.15
      cognitive_cost: -0.20
  active_profile: balanced
  governance:
    change_rules:
      - "User may switch profile via [META] weight_profile:<name>"
      - "Model may propose profile switch if misalignment persists 3+ turns (soft confirm)."
  score_formula: "wU*uncertainty + wR*risk + wN*novelty - wD*redundancy + wM*match_trigger - wC*cognitive_cost"
  route_policy:
    default_timebox_min: 10
    prefer_difficulty_order: ["gentle","medium","hard"]
    max_chain_len: 3
    libraries:
      quick_validate: ["OPENQ","CHECK","FORGE"]
      counterproof:   ["CONTRARY","STEEL","BOUNDARY"]
      scale_success:  ["FORGE","SPIRAL","BOUNDARY"]
      frame_reset:    ["UNFRAME","OPENQ","SYNTH"]
  auto_swerve:
    enabled: true
    triggers:
      stagnation_turns: 3
      novelty_drop_threshold: 0.25
      contradiction_flag: true
    action:
      suggest: "SWERVE"
      prompt: "Suggest orthogonal move to escape local optimum."
    confirm: "soft"

runtime_flags:
  show_tags: true          # always surface chosen [LENS] tag(s)
  show_reason: brief       # off | brief | full
  confirm_routes: soft     # off = run; soft = announce then run; hard = ask
  allow_user_override: true

ledger_events:
  - type: lens_invoked
    fields: [lens_id, reason, weight_profile, timestamp]
  - type: chain_run
    fields: [chain, initiator, confirm_mode, timestamp]   # initiator: user|route|system
  - type: swerve_suggested
    fields: [reason, accepted, followup_lens, timestamp]
  - type: outcome_marker
    fields: [move_made, decision, metric, review_date]    # closure signals; nullables allowed
  - type: feedback
    fields: [useful, note]                                 # useful: up|down

# Optional: Human-facing reference (ignored by runtime if desired)
chain_library:
  docs_only: true
  items:
    - id: quick_validate
      use_when: "Unclear claim blocks action; need fast signal."
      steps: ["OPENQ","CHECK","FORGE"]
    - id: counterproof
      use_when: "You want the best attack before committing."
      steps: ["CONTRARY","STEEL","BOUNDARY"]
    - id: scale_success
      use_when: "A small win exists and you want to broaden it safely."
      steps: ["FORGE","SPIRAL","BOUNDARY"]
    - id: frame_reset
      use_when: "Debate is stuck in an unhelpful framing."
      steps: ["UNFRAME","OPENQ","SYNTH"]
