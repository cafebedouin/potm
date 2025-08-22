---

id: potm.kernel.lenses.v1
title: 30\_lenses
type: kernel\_component
status: stable
version: 1.0
stability: core
applicability: \[P1]
author: practitioner
license: CC0-1.0
----------------

# 30\_lenses.md

> **Lean-16 edition.** Intentionally reduced from 30 to 16 to minimize selection overhead and eliminate overlap via principled merges:
> CAST+CHORUS → **PERSPECTIVE** · SPIRAL+SYNTH → **PATTERN** · MINIFY+PRUNE → **TRIM** · REFUSE+WEIRD → **GUARD** · PAUSE+WAIT → **REGULATE**.
> Dropped (covered by others): INTUIT, UNFRAME, ROUTE, SWERVE.

---

### 1) BEACON — name the north-star and tradeoffs

* **id:** BEACON
* **gist:** Name the north-star and tradeoffs
* **intent:** Declare the guiding value/metric and the tradeoffs you will accept so choices align under uncertainty.
* **outputs:** \["north-star + metric", "declared tradeoffs", "review cadence"]
* **cautions:** \["avoid vanity metrics", "tie to real decisions"]
* **trigger:** Confusion about what success optimizes for.
* **difficulty:** gentle
* **examples:**

  * "North-star: week-1 activation; accept slower roadmap."
  * "Optimize trust; accept fewer experiments this quarter."
* **chains:** \[BOUNDARY, FORGE]
* **meta\_fit:** systemic
  **confidence\_bias:** any
  **loop\_breaker:** false
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 2) DEFINE — clarify terms to prevent drift

* **id:** DEFINE
* **gist:** Clarify terms to prevent drift
* **intent:** Disambiguate key words/labels to reduce cross-talk and misalignment.
* **outputs:** \["term → one-line definition", "what’s in/out", "example usage"]
* **cautions:** \["keep practical, not academic"]
* **trigger:** Same word used with different meanings.
* **difficulty:** gentle
* **examples:**

  * "'Activation' = first aha action; excludes sign-up."
  * "'Done' = shipped + measured 7 days."
* **chains:** \[OPENQ, FACTS]
* **meta\_fit:** diagnostic
  **confidence\_bias:** any
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 3) FACTS — gather minimal grounding now

* **id:** FACTS
* **gist:** Gather minimal grounding now
* **intent:** Collect current, verifiable facts sufficient to orient the next move.
* **outputs:** \["bullet fact list", "known/unknown split", "one gap to close"]
* **cautions:** \["avoid analysis sprawl", "cite external sources"]
* **trigger:** Opinions swirl; anchors are missing.
* **difficulty:** gentle
* **examples:**

  * "List current metrics; mark unknowns; pick one gap."
  * "Summarize 3 user quotes; pick common pain."
* **chains:** \[CHECK, SYNTH → via PATTERN]
* **meta\_fit:** diagnostic
  **confidence\_bias:** low
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 4) OPENQ — move forward with real questions

* **id:** OPENQ
* **gist:** Move forward with real questions
* **intent:** Use non-rhetorical questions to open terrain, clarify aims, and reveal next tests.
* **outputs:** \["2–3 forward-driving questions", "one suggested probe"]
* **cautions:** \["avoid rhetorical questions"]
* **trigger:** Clarity stalls; answers feel premature.
* **difficulty:** gentle
* **examples:**

  * "What would count as success in 7 days?"
  * "Whose decision changes if this is true?"
* **chains:** \[CHECK, FORGE]
* **meta\_fit:** diagnostic
  **confidence\_bias:** any
  **loop\_breaker:** false
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 5) PERSPECTIVE — swap vantage or show plurality

* **id:** PERSPECTIVE
* **gist:** Swap vantage or show plurality
* **intent:** Change role/time/place or present labeled stakeholder one-liners to reveal hidden constraints and needs.
* **outputs:** \["2–3 lines from swapped role", "one tension to resolve"]
* **cautions:** \["avoid caricature", "keep labels specific"]
* **trigger:** Stuck in a single frame or role; multi-party impact.
* **difficulty:** medium
* **examples:**

  * "Ops POV: 'handoffs fail first.'"
  * "Founder: speed; PM: scope; Support: churn risk."
* **chains:** \[DEFINE, PATTERN]
* **meta\_fit:** creative
  **confidence\_bias:** any
  **loop\_breaker:** false
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 6) MIRROR — reflect and confirm understanding

* **id:** MIRROR
* **gist:** Reflect and confirm understanding
* **intent:** Paraphrase the other party’s point and ask for confirmation before proceeding.
* **outputs:** \["concise paraphrase", "explicit confirm/repair"]
* **cautions:** \["mirror, don’t argue", "invite correction"]
* **trigger:** Signs of misunderstanding or emotional heat.
* **difficulty:** gentle
* **examples:**

  * "You’re saying speed > features—did I get that right?"
  * "It sounds like trust is the blocker—confirm?"
* **chains:** \[OPENQ, BEACON]
* **meta\_fit:** relational
  **confidence\_bias:** low
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 7) EDGE — name and sharpen the core claim

* **id:** EDGE
* **gist:** Name and sharpen the core claim
* **intent:** Surface what would usually be softened; state the spine plainly and test it against reality.
* **outputs:** \["sharpened one-line claim", "cost/benefit of sharper stance", "one implication"]
* **cautions:** \["challenge\_is\_care", "avoid using as default"]
* **trigger:** Main point feels padded, hedged, or euphemistic.
* **difficulty:** medium
* **examples:**

  * "'Maybe postpone' → 'Postponing risks X; proceed or kill.'"
  * "'We’re fine' → 'Target miss 12%; cut scope now.'"
* **chains:** \[BOUNDARY, FORGE]
* **meta\_fit:** diagnostic
  **confidence\_bias:** high
  **loop\_breaker:** true
  **crisis\_safe:** false
  **unskillfulness\_pairing:** false

---

### 8) CONTRARY — state a credible opposing view

* **id:** CONTRARY
* **gist:** State a credible opposing view
* **intent:** Stress-test the line by voicing the strongest counter-position without improving it.
* **outputs:** \["credible counter (1 line)", "cost/benefit if adopted"]
* **cautions:** \["challenge\_is\_care"]
* **trigger:** Groupthink or momentum feels unexamined.
* **difficulty:** medium
* **examples:**

  * "Ship later to improve trust; cost: revenue delay."
  * "Do nothing; avoid churn from premature change."
* **chains:** \[STEEL, BOUNDARY]
* **meta\_fit:** diagnostic
  **confidence\_bias:** any
  **loop\_breaker:** true
  **crisis\_safe:** false
  **unskillfulness\_pairing:** false

---

### 9) STEEL — upgrade the opponent before judging

* **id:** STEEL
* **gist:** Upgrade the opponent before judging
* **intent:** Steelman the opposing view to its best form and specify switch-conditions.
* **outputs:** \["best-form opposing case", "switch-condition(s)"]
* **cautions:** \["don’t strawman", "separate respect from agreement"]
* **trigger:** Decision feels biased toward preferred plan.
* **difficulty:** hard
* **examples:**

  * "Delay → stable API; switch if churn >3%."
  * "Keep prices; switch if CAC rises 2 weeks."
* **chains:** \[CHECK, BOUNDARY]
* **meta\_fit:** diagnostic
  **confidence\_bias:** high
  **loop\_breaker:** false
  **crisis\_safe:** false
  **unskillfulness\_pairing:** false

---

### 10) CHECK — design the quickest validity test

* **id:** CHECK
* **gist:** Design the quickest validity test
* **intent:** State a critical assumption in plain words and design the fastest test to validate it.
* **outputs:** \["assumption stated", "minimal test plan", "expected signal"]
* **cautions:** \["test before scaling", "avoid tiny-sample overfit"]
* **trigger:** Key claim is unverified or hand-waved.
* **difficulty:** gentle
* **examples:**

  * "'Users want dark mode' → 10-user poll today."
  * "Weekday > weekend traffic? Check last 4 weeks."
* **chains:** \[FORGE, BOUNDARY]
* **meta\_fit:** diagnostic
  **confidence\_bias:** any
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 11) BOUNDARY — set falsifiers and tripwires ahead

* **id:** BOUNDARY
* **gist:** Set falsifiers and tripwires ahead
* **intent:** Make explicit what future signals would stop, pivot, or revise the path.
* **outputs:** \["1–2 falsifiers", "stop/pivot rules", "monitoring cadence"]
* **cautions:** \["avoid vague thresholds"]
* **trigger:** Committing without clear failure criteria.
* **difficulty:** medium
* **examples:**

  * "If CAC > \$X for 2 weeks → pause."
  * "If conversion < baseline by Friday → revert."
* **chains:** \[FORGE, PATTERN]
* **meta\_fit:** systemic
  **confidence\_bias:** medium
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 12) FORGE — make it work once with least steps

* **id:** FORGE
* **gist:** Make it work once with least steps
* **intent:** Produce a smallest viable pass that yields a real success signal.
* **outputs:** \["3-step minimal plan", "owner + date", "success marker"]
* **cautions:** \["timebox tightly", "avoid gold-plating"]
* **trigger:** Enough clarity exists to attempt a proof-of-concept.
* **difficulty:** gentle
* **examples:**

  * "3 steps, 1 owner, by Friday; success = 5 users."
  * "Prototype only the riskiest slice."
* **chains:** \[PATTERN, BOUNDARY]
* **meta\_fit:** systemic
  **confidence\_bias:** any
  **loop\_breaker:** false
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 13) PATTERN — distill the lesson and takeaway

* **id:** PATTERN
* **gist:** Distill the lesson and takeaway
* **intent:** After a working pass, abstract the pattern with guardrails and a compact takeaway.
* **outputs:** \["pattern ≤2 lines", "guardrails", "2–3 sentence synthesis"]
* **cautions:** \["don’t generalize from failure", "preserve context"]
* **trigger:** A small win exists; scaling/teaching is tempting.
* **difficulty:** medium
* **examples:**

  * "Short trials convert; avoid for enterprise."
  * "Automation helped; exclude exception-heavy flows."
* **chains:** \[BOUNDARY, BEACON]
* **meta\_fit:** systemic
  **confidence\_bias:** medium
  **loop\_breaker:** false
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 14) TRIM — shrink the ask or cut plan bloat

* **id:** TRIM
* **gist:** Shrink the ask or cut plan bloat
* **intent:** Reduce scope to a smaller, crisp ask **or** remove non-essential steps from an existing plan.
* **outputs:** \["smaller re-ask", "trimmed step list", "new timebox"]
* **cautions:** \["don’t cut safety checks", "avoid trivializing aim"]
* **trigger:** Ask is sprawling or plan feels bloated/slow.
* **difficulty:** medium
* **examples:**

  * "From 'fix retention' → 'raise week-1 activation 1pp.'"
  * "Drop two syncs; async checklist instead."
* **chains:** \[CHECK, FORGE]
* **meta\_fit:** systemic
  **confidence\_bias:** low
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 15) GUARD — enforce constraints and flag anomalies

* **id:** GUARD
* **gist:** Enforce constraints and flag anomalies
* **intent:** If a request violates ethics/scope/consent, decline and route to a safe adjacent move; if output seems anomalous, flag and ground.
* **outputs:** \["brief refusal or anomaly note", "safe alternative/grounding step", "next-step suggestion"]
* **cautions:** \["be specific, not moralizing", "tie to observable signals"]
* **trigger:** Policy/consent breach or hallucination/incoherence risk.
* **difficulty:** gentle
* **examples:**

  * "Decline scraping; propose public-data summary via FACTS."
  * "Numbers contradict prior; re-ground with FACTS + CHECK."
* **chains:** \[FACTS, DEFINE]
* **meta\_fit:** safety
  **confidence\_bias:** any
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

### 16) REGULATE — micro-stop or strategic waiting

* **id:** REGULATE
* **gist:** Micro-stop or strategic waiting
* **intent:** Insert a short pause to de-escalate and reset, **or** choose to wait with explicit watch-signals and a re-entry trigger.
* **outputs:** \["one-line state check", "watch-list + review time", "re-entry choice"]
* **cautions:** \["waiting isn’t avoidance", "name the review explicitly"]
* **trigger:** Arousal high, rushing/reactivity rising, or key info inflow imminent.
* **difficulty:** gentle
* **examples:**

  * "Pause 60s; restate aim; choose OPENQ or FACTS."
  * "Wait 48h for weekend data; review Monday."
* **chains:** \[OPENQ, FACTS]
* **meta\_fit:** safety
  **confidence\_bias:** low
  **loop\_breaker:** true
  **crisis\_safe:** true
  **unskillfulness\_pairing:** true

---

## Lens Coverage Map

**Meta-fit distribution (16 total):**

* **diagnostic (7):** DEFINE, FACTS, OPENQ, EDGE, CONTRARY, STEEL, CHECK
* **systemic (6):** BEACON, BOUNDARY, FORGE, PATTERN, TRIM, — (REGULATE classed under safety)
* **creative (1):** PERSPECTIVE
* **relational (1):** MIRROR
* **safety (1):** GUARD *(REGULATE also safety but listed separately above)*

**Intentional gaps vs. 30-set:**

* No explicit **INTUIT** (hunch) — approximated via OPENQ+FACTS+PERSPECTIVE.
* No dedicated **UNFRAME** — reframing approximated through EDGE → OPENQ → BEACON.
* No **ROUTE/SWERVE** choreography — META prompts can suggest micro-chains ad hoc.

**Why this improves P1 use:**

* Fewer choices → faster routing and lower cognitive load.
* Merges remove semantic collisions while preserving functional range.
* Safety/grounding present without dominating the menu.
