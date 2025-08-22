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
      - "Name the non-negotiable in one line."
    chains: ["EDGE → BOUNDARY", "EDGE → FORGE"]

  - id: INTUIT
    gist: "tentative sense"
    intent: "Offer a tentative pattern you can’t fully articulate yet."
    outputs: ["mark confidence", "suggest next probe"]
    cautions: ["precision_over_certainty"]
    trigger: "When you have a hunch worth surfacing before it's fully formed."
    difficulty: medium
    examples:
      - "Hunch: 'Pattern looks seasonal (60%); check last 12 months.'"
      - "Flag weak signal + propose a quick probe."
    chains: ["INTUIT → OPENQ", "INTUIT → CHECK"]

  - id: CONTRARY
    gist: "counter stance"
    intent: "Surface the strongest counter to the current line."
    outputs: ["credible counter in 1–2 lines", "cost/benefit of adopting this counter-position"]
    cautions: ["challenge_is_care"]
    trigger: "When you want to test the idea’s resilience against opposition."
    difficulty: medium
    examples:
      - "Counter: 'Ship later improves trust'; cost: delay revenue; benefit: fewer defects."
      - "Name best case for the other side."
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
    difficulty: hard
    examples:
      - "Opposing best case: 'Delay yields stable API'; switch if churn >3%."
      - "Name the condition that would make you flip."
    chains: ["STEEL → CHECK", "STEEL → BOUNDARY"]

  - id: BOUNDARY
    gist: "future tripwires"
    intent: "Expose future-facing falsifiers or tripwires for the idea."
    outputs: ["1–2 disconfirmers", "conditions under which to stop or revise"]
    trigger: "When you need to know what would signal this path is wrong."
    difficulty: medium
    examples:
      - "Tripwire: if CAC> $X for 2 weeks → pause."
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
      - "User, Buyer, Regulator in one-liners."
    chains: ["CHORUS → SYNTH", "CHORUS → OPENQ"]

  - id: UNFRAME
    gist: "drop frame"
    intent: "Name and drop the current frame."
    outputs: ["frame in 1 line", "no-frame reading in 1–2 lines"]
    trigger: "When the framing itself might be distorting the view."
    difficulty: hard
    examples:
      - "Frame: 'speed vs quality'; No-frame: 'choose reversible vs irreversible.'"
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
      - "3 steps, 1 owner, done by Friday, success = 5 paying users."
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
