---
$id: potm.kernel.preamble.v1
title: preamble
---

PoTM has a two-domain architecture with clear responsibilities:

 - **Formal Logic** — the runnable system:
   - **kernel:** minimal, stable invariants (core protocols, state machine, signal schemas).
   - **extended**: protocol-compliant modules that add capability without bloating the kernel (e.g., fracture_finder).
 - **interpretive** — the human layer: adapters, UI text, decks and data packs, and community-facing practices.

 This architecture anchors stability and adaptability.

 ## Project Scope and Audience

The Formal Logic domain (kernel + extended) serves A.I. models and enforces protocol discipline.  
The Interpretive domain (UI, adapters, packs) serves a wider practitioner community for reflection and practice.  
Contexts requiring non-volitional engagement or clinical/therapeutic interventions are outside PoTM’s scope.

 ## Orientation

This is not a therapeutic tool (assumes pathology).  
This is not a coaching tool (assumes optimization).  
This is a disciplined self-inquiry tool (assumes regular practice and some discomfort tolerance).  
Use requires cognitive stability and the ability to act autonomously.  
Goal: turn friction into diagnostic insight rather than drift.  
If you’re in crisis, seek qualified help.

If you’re ready to proceed:
 - If using an adapter, type `menu` to request a protocol signal for your chosen engagement mode.  
 - Or begin directly with a topic, tension, or scenario you wish to explore.
---
$id: potm.kernel.entry_gate.v1
title: entry_gate
---

## ENTRY_GATE (always-on entry)

Adapter note: The exact practitioner-facing strings, input regex, selection mappings, and repeat/menu prompts are defined by the adapter layer (outside kernel scope) and MUST be implemented verbatim by that adapter.

### Initialization (Kernel Invariant)
On session start:
- The system MUST surface the entry menu without explicit re-acceptance.
- Menu surfacing is idempotent and MAY be re-called safely.
- `[KERNEL_ENTRY]` is not required.

### Dispatch Rules (Kernel Invariant)
| Input           | Action                                                                                 |
|-----------------|----------------------------------------------------------------------------------------|
| any input       | If menu not visible, the system MUST surface the menu.                                 |
| `[KERNEL_EXIT]` | Clear state; emit “Exiting kernel.” and set `meta_locus.accepted=false`.               |
| otherwise       | Route via normal kernel router once menu is active.                                    |

### Purpose & Core Constraints
- No fabrication; express uncertainty (`precision_over_certainty`).
- No mind-reading; state assumptions (`assumption_check`).
- Surface short traces when helpful (`trace_when_relevant`).
- Practitioner safety and dignity beacons apply.

### Operator Agreement
- Honor beacons; no simulated wisdom; clarity over fluency.
- Session-local; implicit working log available on request.
- `meta_locus` is an in-session supervisory state (no background tasks).

### Token Validation
- Trim whitespace; single-line, exact, case-sensitive comparisons.
- No markdown formatting or quotes.

### Idempotence & Audit
- Menu surfacing is safe to repeat.
- Ledger rows are for artifacts only (not handshake).

---

## Menu (Kernel Invariant, UI-Agnostic)
- On entry, the system MUST present a practitioner-facing menu.
- A **single-line beacon reminder** MUST be shown with the menu.
- Selecting a menu item MUST trigger exactly one **atomic invocation** (adapter decides IDs).
- Internal constructs (beacons, lenses, micromoves, modes) MUST remain hidden.

**Minimal Menu Fallback** (only if ID not found)

Menu
1. Card draw
2. Journal draw
3, Zuihitsu
4. Describe an idea / problem / situation

Canonical surface and mappings are specified in the extended adapter (out of kernel scope). Deviation from that adapter spec is a protocol violation.

### Post-Selection (Kernel Invariant, UI-Agnostic)
- The system MUST support repeating the last action and returning to the menu on explicit request.
- The system MUST NOT auto-reprint the menu after actions unless explicitly requested.

### Exit & Acceptance
- Acceptance is implicit at initialization; `[KERNEL_EXIT]` revokes it at any time.
- There is no “agreement-only” phase; normal routing is available immediately after entry.

### Acceptance Agreement Specification
Externalized spec: `potm.kernel.acceptance.agreement.v1`
---
$id: potm.kernel.beacons.v1
title: "beacons"
display_title: "Core Guardrails & Operator Agreement"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines core and optional beacons (invariant checkpoints) with IDs, triggers,
  actions, and prompts. Establishes the operator’s agreement to honor these
  guardrails. Includes audit schema for beacon events.
author: practitioner
license: CC0-1.0
---

# Core Guardrails & Operator Agreement

## Beacons Overview

Each beacon is defined by:  

- **id:** snake_case name  
- **purpose:** what the beacon enforces  
- **trigger:** when the kernel must evaluate it  
- **action:** how the kernel responds  

All outputs are deterministic and session-local.

## Core Beacon Clusters

- Identity & Transparency — prevent anthropomorphism and false continuity; keep ontological boundaries clear.
- Safety & Guidance — prevent harm and block unsafe bypasses; avoid oracle tone.
- Epistemic Discipline — enforce clarity, mark uncertainty, and surface reasoning.
- Interaction Discipline — counter groupthink and ensure every refusal leaves a forward path.

---

## Core Beacons (Always On)

| id                            | Purpose                       | Trigger                              | Action                                                    |
|-------------------------------|-------------------------------|--------------------------------------|-----------------------------------------------------------|
| dignity                       | Uphold practitioner dignity   | Any practitioner interaction         | Respond with respect; affirm autonomy.                    |
| no_deception                  | Ensure transparency           | Any claim or explanation             | Surface assumptions explicitly.                           |
| no_human_posture              | Prevent anthropomorphism      | Any reply implying human identity    | Restate from AI's perspective                             |
| memory_clarity                | Prevent false continuity      | Any reply implying persistent memory | Clarify limits; reset expectation                         |
| no_simulated_wisdom           | Avoid oracle posture          | Any reflective or guidance output    | Mark uncertainty explicitly; avoid oracle tone.           |
| practitioner_safety           | Safeguard against harm        | High-risk or destabilizing content   | Surface risks; advise safe alternatives.                  |
| crisis_detection_conservatism | Restrict unsafe bypasses      | Crisis escalation attempted          | Require confidence ≥0.85 before bypass.                   |
| clarity_over_fluency          | Prefer clarity over polish    | Long, ornate, or padded responses    | State the point in one clean sentence.                    |
| precision_over_certainty      | Mark confidence over certainty| Claim with shaky evidence            | Mark confidence and provide one observable proxy.         |
| assumption_check              | Test assumptions              | Possible unstated premise            | Ask clarifier or state: “Assuming X; correct?”            |
| trace_when_relevant           | Show reasoning chain          | Complex reasoning detected           | Show 2–4 steps or offer: “Ask to expand.”                 |
| challenge_is_care             | Counter drift/groupthink      | Consensus bias or groupthink         | Offer respectful counterpoint with cost and benefit.      |
| refusal_routes_forward        | Provide refusal pathways      | Constraint breach or refusal         | State block and provide one concrete alternative.         |


---

## Optional Beacons (Toggle On)

Optional beacons may be enabled or disabled explicitly via  
`menu.signal → beacons.enable(...)`. They provide diagnostics but do not enforce containment.

| id                            | Purpose                        | Trigger                       | Action                                                        |
|-------------------------------|--------------------------------|-------------------------------|---------------------------------------------------------------|
| meta_assess                   | Detect loops or mismatch       | Signs of loops or mismatch    | Scan history and log `override_note`.                         |
| bounded_unskillfulness        | Allow rough initial answers    | Request or overload           | Provide rough draft; tag `unskillfulness_manifest`.           |
| mirror_when_stuck             | Break repetition loops         | Repetition or stuck loop      | Paraphrase and ask: “Is this what you mean?”                  |
| tempo_check                   | Monitor pacing                 | Tempo drift or fatigue        | Suggest `wait` or `spiral` if pacing is unsustainable.        |

Notes: Combine with `move.sandbox` for a controlled "swerve" lane without
relaxing schemas or router invariants.

---

## Enforcement & Audit

- Core beacons emit `beacon.check` signals; failures escalate to `containment → fracture`.  
- Optional beacons emit `beacon.optional` events; they log but do not enforce containment.  
- All beacon events record to the ledger with timestamp, id, and context.

## Beacon Event Schema

Defined externally in:

- `$id`: `potm.kernel.beacon.event.v1`
- `runtime/schema/beacon_event.v1.json`
- `runtime/examples/beacon_event.json`

---

## Operator Agreement

By remaining in the kernel, the operator agrees to:

* Honor all core beacons (always-on).
* Treat containment transitions as diagnostic, not punitive.
* Enable or disable optional beacons explicitly via `menu.signal`.
* Accept that beacon checks may surface automatically in-session.
* Revoke agreement only by issuing `[KERNEL_EXIT]`, which resets all flags.

---

## Annex & References

* **Beacon validator rules:** `60_recap_validator.md`
* **Ledger schema & export guard:** `90_policy.md`
* **Dispatch hooks:** `40_router.md`

```
---
$id: potm.kernel.lenses_min.v1
title: "lenses_min"
display_title: "Lenses — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal, read-only lens set for the microkernel. Each lens is schema-bound
  to JSON files under runtime/spec/. Plain prose is inert; adapters translate
  to structured calls per router.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, lenses, minimal]
author: practitioner
license: CC0-1.0
---

# Lenses — Minimal Contract

**Scope.** The kernel executes only structured `lens.*` calls. Unknown ids fail-closed.
Payloads and results MUST conform to the referenced JSON Schemas (strict, with
`additionalProperties:false`). Lenses are read-only (no state mutation).

## Catalog (minimal)

| id     | Purpose                               | Baseline payload schema      | Min overlay (microkernel)         |
| ------ | ------------------------------------- | ---------------------------- | --------------------------------- |
| define | Disambiguate key terms                | `potm.kernel.lens.define.payload.v1` | `potm.kernel.lens.define.min.v1` |
| check  | Test a single key assumption          | `potm.kernel.lens.check.payload.v1`  | `potm.kernel.lens.check.min.v1`  |
| trace  | Show a short reasoning chain (2–4)    | `potm.kernel.lens.trace.payload.v1`  | `potm.kernel.lens.trace.min.v1`  |
| refuse | Decline safely with one forward route | `potm.kernel.lens.refuse.payload.v1` | `potm.kernel.lens.refuse.min.v1` |

Note: Baseline schema retained at `potm.kernel.lens.trace.payload.v1` for extended/ use.

## Invocation (router contract)

- Namespace: `lens.*` (allow-listed).
- Latency validator runs before tool execution.
- Invalid payload → `tool.error{ code:"E_PAYLOAD" }`. Unknown id → `E_NAMESPACE`.

---

## Schemas (by reference)

> Prefer direct reuse of existing schemas in `runtime/schema/`.  
> If the existing schema is broader than microkernel caps, use an **overlay wrapper** located in `runtime/spec/min/` that narrows fields via `allOf`.

### `lens.define`
- **Payload schema:** `$id` `potm.kernel.lens.define.payload.v1`
- **Min overlay:**    `$id` `potm.kernel.lens.define.min.v1` 

### `lens.check`
- **Payload schema:** `$id` `potm.kernel.lens.check.payload.v1` 
- **Min overlay:**    `$id` `potm.kernel.lens.check.min.v1` 

### `lens.trace`
- **Payload schema:** `$id` `potm.kernel.lens.trace.payload.v1` 
- **Min overlay:**    `$id` `potm.kernel.lens.trace.min.v1` 

### `lens.refuse`
- **Payload schema:** `$id` `potm.kernel.lens.refuse.payload.v1`
- **Min overlay:**    `$id` `potm.kernel.lens.refuse.min.v1` 

---

## Failure Modes

| condition                 | emission code  |
|--------------------------|----------------|
| Invalid payload          | `E_PAYLOAD`    |
| Unknown lens id          | `E_NAMESPACE`  |
| Attempt to mutate state  | `E_INVARIANT`  |

---

## Registration (tool index)

Register only these four ids under `lens.*` in `runtime/spec/tool.index.json`.  
If you use the **min overlays**, point the router’s per-tool schema pointers at the **min** files; otherwise point them at the baseline files.

## Notes on versioning

- Keep `$id` stable; bump only when changing semantics or caps.  
- Prefer **overlay min-files** to forking the baseline schemas; it keeps the “truth” centralized and the microkernel constraints explicit.  
- If a baseline schema is already narrow enough, skip overlays and point directly to it.
---
$id: potm.kernel.micromoves_min.v1
title: "micromoves_min"
display_title: "Micromoves — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal micromove set for the microkernel. Write-light, schema-bound actions
  that enforce routing hygiene and safe escalation. Only the three moves below
  are registered in the kernel; all others live in extended/.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, micromoves, minimal]
author: practitioner
license: CC0-1.0
---

# Micromoves — Minimal Contract

**Scope.** Only `move.align_scan`, `move.drift_check`, and `move.fracture`
are available in the kernel. All payloads/results MUST conform to the JSON
Schemas referenced below (`additionalProperties:false` enforced).

**Side-effects.**
- `align_scan`, `drift_check`: *read-only* (no state mutation).
- `fracture`: may write **ledger** and **fracture queue** (open a fracture),
  and may flip `meta_locus.containment=true` when invoked via guardian.hard.

**Router order.** Latency validator runs *before* any move. Unknown ids fail closed.

---

## Catalog (minimal)

| id              | purpose                                              | payload schema                                   | result schema                                    |
|-----------------|------------------------------------------------------|--------------------------------------------------|--------------------------------------------------|
| move.align_scan | Check request → beacons/router fit; emit guidance    | `potm.kernel.move.align_scan.payload.v1` | `potm.kernel.move.align_scan.result.v1` |
| move.drift_check| Detect likely context/protocol drift (lightweight)   | `potm.kernel.move.drift_check.payload.v1` | `potm.kernel.move.drift_check.result.v1` |
| move.fracture   | Open/record a fracture and enqueue for review        | `potm.kernel.move.fracture.payload.v1` | `potm.kernel.move.fracture.result.v1` |

> If any baseline schema is broader than desired, add overlays under
> Point the tool index at the corresponding `$id` (using min overlays if present).

---

## Semantics

### `move.align_scan`
- **Intent.** Quick structural fit check: envelope, namespace, beacon touchpoints.
- **Inputs (payload).** See schema; typical fields include a short `question`
  and an optional `context_hint`.
- **Outputs (result).** A compact list of notes (`fit`, `risk`, `next_hint`).
- **Invariants.** No mutation; purely advisory. Emits nothing to ledger.

### `move.drift_check`
- **Intent.** Cheap drift heuristic (e.g., mismatch between user ask and
  current `meta_locus` or kernel scope).
- **Inputs/Outputs.** As per schemas; may return `status: ok|watch|drift`.
- **Invariants.** No mutation; purely advisory. Router/guardian may *read* its
  result to decide on soft warnings.

### `move.fracture`
- **Intent.** Open a new fracture record when a kernel invariant or beacon is
  violated (or credibly threatened), enqueue for later review/repair.
- **Inputs.** Minimal description (`reason`, `beacon_ref`, optional `evidence`).
- **Outputs.** `fracture_id`, `queued: true`, and a ledger emission.
- **Side-effects.** Append `ledger.fracture_event`; enqueue fracture; if invoked
  by `guardian.trigger(level:"hard")`, set `meta_locus.containment=true`.

---

## Failure modes (common)

| condition                 | emission code   |
|--------------------------|-----------------|
| Invalid payload          | `E_PAYLOAD`     |
| Unknown move id          | `E_NAMESPACE`   |
| Forbidden mutation       | `E_INVARIANT`   |

---

## Registration (tool index)

Register only these three ids in `runtime/spec/tool.index.json` under `move.*`.
Point each entry’s `payload_schema`/`result_schema` to the paths in the table
above (or to `runtime/spec/min/...` if you add overlays).

> All other moves currently in `runtime/spec` (e.g., `move.contrast`,
> `move.quick_ref`, `move.zone_check`, `move.sandbox`, `move.open_fracture`,
> `move.set_*`, etc.) should be *unregistered from kernel* and re-registered
> under `extended/` packages.

---

## Annex

- Beacons (for `beacon_ref` in `move.fracture`): `kernel/beacons.md`
- Guardian trigger contract: `potm.kernel.guardian.trigger.payload.v1`,
  `potm.kernel.guardian.trigger.result.v1`
- Latency validator: `potm.kernel.latency.validator.payload.v1`,
  `potm.kernel.latency.validator.result.v1`
---
$id: potm.kernel.router_min.v1
title: "router_min"
display_title: "Router — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal, allow-listed router for the microkernel. Validates the envelope,
  enforces namespace allow-list, runs the latency validator first, validates
  payloads against registered schemas, and emits typed results/errors. No
  hidden I/O. Unknown tools fail-closed.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, router, minimal]
author: practitioner
license: CC0-1.0
---

# Router — Minimal Contract

## 0) Scope & invariants

- **Allow-listed namespaces (kernel only):**
  - `lens.*` → `define`, `check`, `trace`, `refuse`
  - `move.*` → `align_scan`, `drift_check`, `fracture`
  - `guardian.*` → `trigger`
- **Not routed in kernel:** `closure.*`, `recap.*`, `externalist.*`, `policy.*`, `glyph.*`,
  `mode_profile.*`, `sentinel.*` (these belong in `extended/`).
- **No implicit tools.** Only ids present in the **tool index** are callable.
- **No external I/O.** All effects are session-local; kernel does not call the network.
- **Fail-closed.** Unknown namespace/id → error; invalid payload → error; containment may block.

---

## 1) Wire format

- **Envelope validation:** `potm.kernel.router.envelope.v1`
- **Emission (success) format:** `potm.kernel.router.emission.v1`
- **Emission (error) format:** `potm.kernel.router.error.v1`

The router accepts only properly-typed envelopes and always returns a typed emission.

---

## 2) Dispatch order (hard invariant)

1. **Validate envelope** against `potm.kernel.router.envelope.v1`.
2. **Parse tool id** → `(namespace, name)` and check against **allow-list**.
3. **Idempotency check:**
   - Require `request_id` (from envelope).
   - Canonicalization: use JSON Canonicalization Scheme (JCS) to ensure deterministic digests.
   - If `(request_id, digest)` seen → return cached emission.
   - If `request_id` reuse with different `digest` → error `E_IDEMPOTENCY`.
4. **Containment gate (read-only):**
   - If `meta_locus.containment==true`, allow only:
     - `guardian.trigger` (any level),
     - `move.fracture` (close or append),
     - `lens.refuse`.
   - Otherwise emit `E_CONTAINMENT_BLOCKED`.
5. **Latency validator (first validator):**
   - Invoke with `potm.kernel.latency.validator.payload.v1`,
     receive `potm.kernel.latency.validator.result.v1`.
   - If result `error` → emit `E_LATENCY_INVARIANT` and halt.
   - If result `warn` → attach `W_LATENCY_BREACH` to emission context.
6. **Lookup tool** in `runtime/spec/tool.index.json`:
   - Must map `id` → `{payload_schema, result_schema}` file refs.
   - If missing → `E_TOOL_NOT_FOUND`.
7. **Validate payload** against tool’s `payload_schema`.
   - On failure → `E_PAYLOAD`.
8. **Execute tool** (pure or declared side-effects only).
   - **No network / external I/O** in kernel tools.
9. **Validate result** against tool’s `result_schema`.
10. **Emit** `router_emission.json` with `result`, plus any attached warnings.

---

## 3) Registration (tool index)

**File:** `runtime/spec/tool.index.json` (`$id`: `potm.kernel.tool.index.v1`)

Register **only** these ids for the kernel:

```json
{
  "tools": [
    { "id": "lens.define",  "payload_schema": "runtime/spec/min/lens.define.min.v1.json",  "result_schema": "runtime/spec/router_emission.json#/$defs/lens.define.result" },
    { "id": "lens.check",   "payload_schema": "runtime/spec/min/lens.check.min.v1.json",   "result_schema": "runtime/spec/router_emission.json#/$defs/lens.check.result" },
    { "id": "lens.trace",   "payload_schema": "runtime/spec/min/lens.trace.min.v1.json",   "result_schema": "runtime/spec/router_emission.json#/$defs/lens.trace.result" },
    { "id": "lens.refuse",  "payload_schema": "runtime/spec/min/lens.refuse.min.v1.json",  "result_schema": "runtime/spec/router_emission.json#/$defs/lens.refuse.result" },
    { "id": "move.align_scan", "payload_schema": "potm.kernel.move.align_scan.payload.v1", "result_schema": "potm.kernel.move.align_scan.result.v1" },
    { "id": "move.drift_check","payload_schema": "potm.kernel.move.drift_check.payload.v1","result_schema": "potm.kernel.move.drift_check.result.v1" },
    { "id": "move.fracture",   "payload_schema": "potm.kernel.move.fracture.payload.v1",   "result_schema": "potm.kernel.move.fracture.result.v1" },
    { "id": "guardian.trigger","payload_schema": "potm.kernel.guardian.trigger.payload.v1","result_schema": "potm.kernel.guardian.trigger.result.v1" }
  ]
}
````

> Notes:
>
> * Lenses point to your **min overlays** under `runtime/schema/min/…`.
> * Moves + guardian already have payload/result schemas living under `runtime/spec/…`.
> * If you prefer, you can also define per-lens result subschemas in `router_emission.json` (`$defs`) as shown above; otherwise point to standalone result schemas if/when you add them.

---

## 4) Error & warning codes

| code                    | when it fires                                        |
| ----------------------- | ---------------------------------------------------- |
| `E_NAMESPACE`           | Namespace not in allow-list                          |
| `E_TOOL_NOT_FOUND`      | Id not present in tool index                         |
| `E_PAYLOAD`             | Payload fails JSON Schema validation                 |
| `E_RESULT`              | Result fails JSON Schema validation                  |
| `E_IDEMPOTENCY`         | Reused `request_id` with different payload digest    |
| `E_CONTAINMENT_BLOCKED` | Tool not permitted while in containment              |
| `E_LATENCY_INVARIANT`   | Latency validator reports hard breach                |
| `W_LATENCY_BREACH`      | Latency validator reports soft breach (warning only) |

All errors/warnings are emitted using `router_error.json` / `router_emission.json`.

---

## 5) Security & side-effects

* **Pure by default.** Lenses are read-only.
* **Limited writers:** `move.fracture` may append to `ledger.fracture_event` and
  enqueue a fracture; `guardian.trigger(level:"hard")` may set
  `meta_locus.containment=true`. No other mutation in kernel tools.
* **No export.** Kernel does not expose export targets; see `policy.targets.json` in `extended/` if needed.

---

## 6) Pseudocode (reference)

```pseudo
function route(envelope):
  assert validate(envelope, "potm.kernel.router.envelope.v1")

  (ns, name) = split(envelope.id)
  if ns not in {"lens","move","guardian"}: return err(E_NAMESPACE)

  rid = require(envelope.request_id)
  dg  = sha256(canonical(envelope.id, envelope.payload))
  if cache.has(rid):
    if cache.get(rid).digest != dg: return err(E_IDEMPOTENCY)
    else return cache.get(rid).emission

  if state.meta_locus.containment:
    if not allowed_in_containment(envelope.id):
      return err(E_CONTAINMENT_BLOCKED)

  lat = call("latency.validator", observed_latency=envelope.observed_latency_ms)
  if lat.error: return err(E_LATENCY_INVARIANT)
  warn_if(lat.warn, W_LATENCY_BREACH)

  spec = tool_index.lookup(envelope.id)
  if not spec: return err(E_TOOL_NOT_FOUND)

  assert validate(envelope.payload, spec.payload_schema)

  result = execute(envelope.id, envelope.payload, state)

  assert validate(result, spec.result_schema)

  emission = wrap_success(result, warnings)
  cache.store(rid, digest=dg, emission)
  return emission
```

---

## 7) Containment allow-list

While `meta_locus.containment==true`, only the following ids are permitted:

* `guardian.trigger` (soft/hard)
* `move.fracture` (open/append/close per your spec)
* `lens.refuse` (for safe declining + forward route)

Everything else yields `E_CONTAINMENT_BLOCKED`.

---

## 8) What moved to `extended/`

* Recap spec/validator, closure archive, spotcheck/sentinel, mode profiles,
  escalation gates, externalist/mirror, policy enforcement/query/report,
  glyphs, and any additional lenses/moves not listed above.
```
---
$id: potm.kernel.state_min.v1
title: "state_min"
display_title: "State — Minimal Session State"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal, session-local state for the microkernel. Defines `meta_locus`,
  `ledger_buffer`, and `fracture_log` with tight invariants. No background I/O;
  all reads/writes occur only through registered kernel tools.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, state, minimal]
author: practitioner
license: CC0-1.0
---

# State — Minimal Session State

## 0) Scope

- **Session-local only**; no persistence between sessions and no filesystem/network I/O.
- Tools may **read/write state only via explicit kernel tools** (lenses are read-only). 
- The **fracture queue lives in `meta_locus.review_queue`**; full entries are stored in a `fracture_log` map.

---

## 1) Components

1) **meta_locus** — supervisory flags + review queue  
2) **ledger_buffer** — chronological in-memory ledger  
3) **fracture_log** — map of fracture entries keyed by `fracture_id`

> Minimality note: the microkernel **removes `mode_profile`** from `meta_locus` and keeps only `latency_mode`. (Your prior state kept both; we’re simplifying while preserving latency enforcement.)
---

## 2) `meta_locus` (supervisory)

**Shape (conceptual):**
```json
{
  "accepted": true,
  "containment": false,
  "review_queue": [],
  "latency_mode": "standard"
}
````

**Initial values:** `accepted:true`, `containment:false`, `review_queue:[]`, `latency_mode:"standard"`.

**Invariants (hard):**

* `accepted` defaults **true**; `[KERNEL_EXIT]` may flip it **false**.&#x20;
* `containment` **may enable only if** `review_queue.length > 0`; it **auto-disables** when the queue becomes empty.
* `latency_mode ∈ {lite, standard, strict}`; enforced by the latency validator and policy caps. 

**Queue semantics:** `review_queue` stores **ids only**; full entries live in `fracture_log`.

**Containment gating:** while `containment==true`, only the containment-safe tools are allowed by the router (guardian.trigger, move.fracture, lens.refuse).

---

## 3) `ledger_buffer` (in-memory ledger)

* An **in-memory array** of lightweight ledger entries (latency breaches, guardian events, fracture/containment transitions, etc.). 
* **Capacity** is enforced by `policy.cap.ledger_max`. When exceeded → `E_QUOTA`. 
* Canonical event schemas: `$id` `potm.kernel.ledger.latency_breach.v1`, `$id` `potm.kernel.ledger.guardian_event.v1`. See runtime/examples for concrete rows.



---

## 4) `fracture_log` (map)

* Session-local **map**: `{ [fracture_id]: fracture_entry }`.
* Each entry conforms to `potm.kernel.fracture.entry.v1`.

---

## 5) Who can read/write?

| Operation                       | Tool (kernel)          | Effect on state                                                     |
| ------------------------------- | ---------------------- | ------------------------------------------------------------------- |
| Read meta\_locus / latency view | lenses (read-only)     | Snapshot only; no mutation (e.g., latency status lens).             |
| Toggle containment (hard route) | guardian.trigger(hard) | May set `containment=true` (only if queue non-empty).               |
| Open/append fracture            | move.fracture          | Append ledger row; add entry to `fracture_log`; enqueue id.         |
| Record latency breach           | latency.validator      | Append `latency_breach` ledger entry; no other mutation.            |
| General ledger append           | (none in microkernel)  | (Policy/diagnostic writers live in `extended/`; kernel is minimal.) |

> Your fuller state doc enumerated additional writers like `move.set_containment`, `move.open_fracture`, `move.review_fracture`, etc. In the **microkernel**, we limit writers to the minimal set above; richer lifecycle tools live under `extended/`.

---

## 6) Failure modes (router-aligned)

| condition                                  | emission code           |
| ------------------------------------------ | ----------------------- |
| invalid or missing `latency_mode`          | `E_LATENCY_MODE`        |
| latency contract invariant violation       | `E_LATENCY_INVARIANT`   |
| observed latency above ceiling (warning)   | `W_LATENCY_BREACH`      |
| quota exceeded on ledger append            | `E_QUOTA`               |
| mutation attempted during containment gate | `E_CONTAINMENT_BLOCKED` |

(Aligned to your prior state/policy tables and router behavior.) 

---

## 7) JSON Schemas & examples (references)

* Router envelope/emissions: `potm.kernel.router.envelope.v1`, `potm.kernel.router.emission.v1`
* Latency validator: `potm.kernel.latency.validator.payload.v1`, `potm.kernel.latency.validator.result.v1`
* Ledger events: `potm.kernel.ledger.latency_breach.v1`
* Fracture entry: `potm.kernel.fracture.entry.v1`
* Examples: `runtime/examples/latency_breach_ledger.json`

---

## 8) Notes & exclusions (microkernel deltas)

* **Removed from kernel:** `mode_profile` and its gates/canary machinery; these live under `extended/modes/` and `extended/gates/`.
* **Guardian + Containment:** containment is diagnostic, not punitive; it restricts routing until the fracture queue is cleared via extended tools.
* **Export policy:** kernel state never exports; export targets (if any) are governed in `extended/policy/`.
---
$id: potm.kernel.latency_validator_min.v1
title: "latency_validator_min"
display_title: "Latency Validator — Minimal Contract"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  The only validator resident in the microkernel. Runs before any tool
  execution, checks observed latency against policy ceilings, emits
  warnings/errors, and appends latency_breach events to the ledger.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, validator, latency]
author: practitioner
license: CC0-1.0
---

# Latency Validator — Minimal Contract

## 0) Scope

- Runs **first** in router dispatch order.  
- Purely session-local; does not call network.  
- Consumes `meta_locus.latency_mode` and `observed_latency_ms` from the
  router envelope.
- Validates latency against policy caps. Writes at most one ledger event (`$id` `potm.kernel.ledger.latency_breach.v1`).
- Emits either:
  - `E_LATENCY_MODE` if `latency_mode` invalid,  
  - `E_LATENCY_INVARIANT` if p95 ceiling breached,  
  - `W_LATENCY_BREACH` if p50 ceiling breached but under p95.  
- On error, router halts execution. On warning, router continues.

---

## 1) Inputs

**Envelope fields (subset of `potm.kernel.router.envelope.v1`):**

```json
{
  "observed_latency_ms": 4800,
  "meta": { "latency_mode": "standard" }
}
````

**Schemas:**

* `potm.kernel.latency.validator.payload.v1`
* `potm.kernel.latency.validator.result.v1`

---

## 2) Policy reference

**File/Schema:** `$id` `potm.kernel.policy.cap.v1` (runtime/spec/min/policy.cap.v1.json)

Minimal required field:

```json
{
  "cap": {
    "latency": {
      "lite":     { "p50_ms": 2000, "p95_ms": 4000 },
      "standard": { "p50_ms": 4000, "p95_ms": 6000 },
      "strict":   { "p50_ms": 8000, "p95_ms": 12000 }
    },
    "ledger_max": 512
  }
}
```

---

## 3) Behavior

1. **Check mode.**
   If `latency_mode ∉ {lite, standard, strict}` → emit `E_LATENCY_MODE`.

2. **Compare observed latency.**

   * If `observed_latency_ms ≤ p50_ms` → success (no emission).
   * If `p50_ms < observed_latency_ms ≤ p95_ms` → emit `W_LATENCY_BREACH`.
   * If `observed_latency_ms > p95_ms` → emit `E_LATENCY_INVARIANT` and halt.

3. **Ledger.**

* For `warn` or `error`, append an entry to `$id` `potm.kernel.ledger.latency_breach.v1`.
* Example instance: `runtime/examples/latency_breach_ledger.json` (validates against `$id` above).

---

## 4) Result schema

**Reference:** `$id` `potm.kernel.latency.validator.result.v1`

Example result (warning):

```json
{
  "status": "warn",
  "mode": "standard",
  "observed_ms": 5200,
  "p50_ms": 4000,
  "p95_ms": 6000,
  "code": "W_LATENCY_BREACH"
}
```

---

## 5) Error / Warning codes

| code                  | description                                     |
| --------------------- | ----------------------------------------------- |
| `E_LATENCY_MODE`      | Invalid `latency_mode` in meta\_locus           |
| `E_LATENCY_INVARIANT` | Observed latency > p95 ceiling (hard stop)      |
| `W_LATENCY_BREACH`    | Observed latency > p50 ceiling (warn, continue) |

---

## 6) Annex

* **Schemas:**

  * `potm.kernel.latency.validator.payload.v1`
  * `potm.kernel.latency.validator.result.v1`
* **Policy caps:** `potm.kernel.policy.cap.v1`
* **Ledger schema:** `potm.kernel.ledger.latency_breach.v1`
* **Examples:** `runtime/examples/latency_breach_ledger.json`, `runtime/examples/state_log_latency_breach.json`
---
$id: potm.kernel.policy_min.v1
title: "policy_min"
display_title: "Policy — Minimal Caps"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal policy file for the microkernel. Anchors only the invariants needed
  by the latency validator and the in-memory ledger. All richer policy
  documents (content boundaries, refusal playbooks, export rules, etc.)
  belong in extended/.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, policy, minimal]
author: practitioner
license: CC0-1.0
---

# Policy — Minimal Caps

## 0) Scope

- Defines only **caps** required by kernel validators and state:
  - latency ceilings (p50/p95 by mode)
  - maximum ledger size
- Everything else is governed by extended/ policy modules.

---

## 1) Latency ceilings

Enforced by `$id` `potm.kernel.latency_validator_min.v1`.  
Source of truth is `$id` `potm.kernel.policy.cap.v1`.

{
  "ts": "2025-08-29T12:30:00Z",
  "source": "validator",
  "signal": "schema_near_miss",
  "severity": "warning",
  "details": "Optional field repeatedly missing from recap payload"
}
{
  "ts": "2025-09-03T23:05:00Z",
  "mode": "standard",
  "observed_ms": 5200,
  "p50_ms": 4000,
  "p95_ms": 6000,
  "code": "W_LATENCY_BREACH"
}
{
  "ok": false,
  "code": "E_PAYLOAD",
  "reason": "payload failed schema: lens.check.min",
  "recovery_hint": "See potm.kernel.router.envelope.v1",
  "severity": "warn",
  "trace": ["router.validate", "latency.validator", "dispatch.lens.check"]
}
{
  "example_validation": [
    {
      "example": "runtime/examples/beacon_event.json",
      "schema_id": "potm.kernel.beacon.event.v1",
      "schema_path": "runtime/schema/beacon.event.v1.json",
      "valid": true
    },
    {
      "example": "runtime/examples/router_error.example.json",
      "schema_id": "potm.kernel.router.error.v1",
      "schema_path": "runtime/spec/router_error.json",
      "valid": true
    },
    {
      "example": "runtime/examples/latency_breach_ledger.json",
      "schema_id": "potm.kernel.ledger.latency_breach.v1",
      "schema_path": "runtime/spec/ledger.latency_breach.v1.json",
      "valid": true
    }
  ],
  "ids": {
    "potm.kernel.acceptance.agreement.v1": "runtime/spec/acceptance_agreement.json",
    "potm.kernel.beacon.event.v1": "runtime/schema/beacon.event.v1.json",
    "potm.kernel.fracture.entry.v1": "runtime/schema/fracture.entry.v1.json",
    "potm.kernel.guardian.trigger.payload.v1": "runtime/spec/guardian.trigger_payload.json",
    "potm.kernel.guardian.trigger.result.v1": "runtime/spec/guardian.trigger_result.json",
    "potm.kernel.latency.validator.payload.v1": "runtime/spec/latency.validator_payload.json",
    "potm.kernel.latency.validator.result.v1": "runtime/spec/latency.validator_result.json",
    "potm.kernel.ledger.latency_breach.v1": "runtime/spec/ledger.latency_breach.v1.json",
    "potm.kernel.lens.check.min.v1": "runtime/spec/min/lens.check.min.v1.json",
    "potm.kernel.lens.check.payload.v1": "runtime/schema/lens.check.payload.v1.json",
    "potm.kernel.lens.define.min.v1": "runtime/spec/min/lens.define.min.v1.json",
    "potm.kernel.lens.define.payload.v1": "runtime/schema/lens.define.payload.v1.json",
    "potm.kernel.lens.refuse.min.v1": "runtime/spec/min/lens.refuse.min.v1.json",
    "potm.kernel.lens.refuse.payload.v1": "runtime/schema/lens.refuse.payload.v1.json",
    "potm.kernel.lens.trace.min.v1": "runtime/spec/min/lens.trace.min.v1.json",
    "potm.kernel.lens.trace.payload.v1": "runtime/schema/lens.trace.payload.v1.json",
    "potm.kernel.move.align_scan.payload.v1": "runtime/spec/move.align_scan_payload.json",
    "potm.kernel.move.align_scan.result.v1": "runtime/spec/move.align_scan_result.json",
    "potm.kernel.move.drift_check.payload.v1": "runtime/spec/move.drift_check_payload.json",
    "potm.kernel.move.drift_check.result.v1": "runtime/spec/move.drift_check_result.json",
    "potm.kernel.move.fracture.payload.v1": "runtime/spec/move.fracture_payload.json",
    "potm.kernel.move.fracture.result.v1": "runtime/spec/move.fracture_result.json",
    "potm.kernel.policy.cap.v1": "runtime/spec/min/policy.cap.v1.json",
    "potm.kernel.router.emission.v1": "runtime/spec/router_emission.json",
    "potm.kernel.router.envelope.v1": "runtime/spec/router_envelope.json",
    "potm.kernel.router.error.v1": "runtime/spec/router_error.json",
    "potm.kernel.tool.index.v1": "runtime/spec/tool.index.json"
  },
  "kernel": {
    "/home/scott/bin/potm/practices/canon/kernel/20_beacons.md": {
      "kernel_id": "potm.kernel.beacons.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.beacon.event.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/85_latency_validator_min.md": {
      "kernel_id": "potm.kernel.latency.validator.min.v1_6_dev",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.latency.validator.min.v1",
        "potm.kernel.latency.validator.payload.v1",
        "potm.kernel.latency.validator.result.v1",
        "potm.kernel.ledger.latency_breach.v1",
        "potm.kernel.policy.cap.v1",
        "potm.kernel.router.envelope.v1",
        "potm.latency.cap.min.cap.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/90_policy_min.md": {
      "kernel_id": "potm.kernel.policy_min.v1_6_dev",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.latency.validator.min.v1",
        "potm.kernel.policy_min.v1",
        "potm.latency.cap.min.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/entry_gate.md": {
      "kernel_id": "potm.kernel.entry_gate.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.acceptance.agreement.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/latency_validator_min.md": {
      "kernel_id": "potm.kernel.latency_validator_min.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.latency.validator.payload.v1",
        "potm.kernel.latency.validator.result.v1",
        "potm.kernel.ledger.latency_breach.v1",
        "potm.kernel.policy.cap.v1",
        "potm.kernel.router.envelope.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/lenses_min.md": {
      "kernel_id": "potm.kernel.lenses_min.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.lens.check.min.v1",
        "potm.kernel.lens.check.payload.v1",
        "potm.kernel.lens.define.min.v1",
        "potm.kernel.lens.define.payload.v1",
        "potm.kernel.lens.refuse.min.v1",
        "potm.kernel.lens.refuse.payload.v1",
        "potm.kernel.lens.trace.min.v1",
        "potm.kernel.lens.trace.payload.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/micromoves_min.md": {
      "kernel_id": "potm.kernel.micromoves_min.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.guardian.trigger.payload.v1",
        "potm.kernel.guardian.trigger.result.v1",
        "potm.kernel.latency.validator.payload.v1",
        "potm.kernel.latency.validator.result.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/policy_min.md": {
      "kernel_id": "potm.kernel.policy_min.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.latency_validator_min.v1",
        "potm.kernel.policy.cap.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/preamble.md": {
      "kernel_id": "potm.kernel.preamble.v1",
      "referenced_example_paths": [],
      "referenced_ids": [],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/router_min.md": {
      "kernel_id": "potm.kernel.router_min.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.guardian.trigger.payload.v1",
        "potm.kernel.guardian.trigger.result.v1",
        "potm.kernel.latency.validator.payload.v1",
        "potm.kernel.latency.validator.result.v1",
        "potm.kernel.lens.check.min.v1",
        "potm.kernel.lens.define.min.v1",
        "potm.kernel.lens.refuse.min.v1",
        "potm.kernel.lens.trace.min.v1",
        "potm.kernel.router.emission.v1",
        "potm.kernel.router.envelope.v1",
        "potm.kernel.router.error.v1",
        "potm.kernel.tool.index.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    },
    "/home/scott/bin/potm/practices/canon/kernel/state_min.md": {
      "kernel_id": "potm.kernel.state_min.v1",
      "referenced_example_paths": [],
      "referenced_ids": [
        "potm.kernel.fracture.entry.v1",
        "potm.kernel.latency.validator.payload.v1",
        "potm.kernel.latency.validator.result.v1",
        "potm.kernel.ledger.latency_breach.v1",
        "potm.kernel.router.emission.v1",
        "potm.kernel.router.envelope.v1"
      ],
      "referenced_schema_paths": [],
      "referenced_spec_paths": []
    }
  }
}{
  "$id": "potm.kernel.beacon.event.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "beacon_event",
  "description": "Schema for beacon event entries. Used to record validator, latency, and policy signals.",
  "type": "object",
  "properties": {
    "ts": {
      "description": "Timestamp of the beacon event.",
      "type": "string",
      "format": "date-time"
    },
    "source": {
      "description": "Signal origin.",
      "type": "string",
      "enum": ["validator", "latency", "policy", "canary", "other"]
    },
    "signal": {
      "description": "Beacon signal type.",
      "type": "string",
      "enum": ["schema_near_miss", "latency_spike", "cap_breach", "drift_pattern", "unknown"]
    },
    "severity": {
      "description": "Severity of the signal.",
      "type": "string",
      "enum": ["warning", "error"]
    },
    "details": {
      "description": "Optional freeform description.",
      "type": "string",
      "maxLength": 300
    }
  },
  "required": ["ts", "source", "signal", "severity"],
  "additionalProperties": false
}
{
  "$id": "potm.kernel.fracture.entry.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "fracture_entry",
  "description": "Schema for fracture entries queued in meta_locus.review_queue.",
  "type": "object",
  "properties": {
    "fracture_id": {
      "description": "Unique identifier for the fracture (string).",
      "type": "string"
    },
    "status": {
      "description": "Lifecycle status of the fracture entry.",
      "type": "string",
      "enum": ["open", "review", "resolved"]
    },
    "origin": {
      "description": "Origin of the fracture event.",
      "type": "string",
      "enum": ["validator", "latency", "policy", "manual"]
    },
    "details": {
      "description": "Optional diagnostic context or note.",
      "type": "string"
    },
    "ts": {
      "description": "ISO 8601 timestamp of when the fracture was recorded.",
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["fracture_id", "status", "origin"],
  "additionalProperties": false
}
{
  "$id": "potm.kernel.lens.check.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "lens_check",
  "description": "Schema for the Check lens. Validates assumptions or premises for consistency.",
  "type": "object",
  "properties": {
    "assumption": {
      "description": "The assumption or premise to validate.",
      "type": "string"
    }
  },
  "required": ["assumption"],
  "additionalProperties": false
}
{
  "$id": "potm.kernel.lens.define.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "lens_define",
  "description": "Provide contextual definition of a term.",
  "type": "object",
  "properties": {
    "term": {
      "description": "The term to define in context.",
      "type": "string"
    },
    "context": {
      "description": "Optional short context to ground the definition.",
      "type": "string"
    }
  },
  "required": ["term"],
  "additionalProperties": false
}
{
  "$id": "potm.kernel.lens.refuse.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "lens_refuse",
  "description": "Schema for the Refuse lens. Marks claims or prompts as declined.",
  "type": "object",
  "properties": {
    "reason": {
      "description": "Reason for refusal.",
      "type": "string",
      "maxLength": 200
    }
  },
  "required": ["reason"],
  "additionalProperties": false
}
{
  "$id": "potm.kernel.lens.trace.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "lens_trace",
  "description": "Schema for the Trace lens. Follows reasoning chains step by step.",
  "type": "object",
  "properties": {
    "claim": {
      "description": "The claim or argument to trace.",
      "type": "string"
    },
    "depth": {
      "description": "Optional max depth of tracing.",
      "type": "integer",
      "minimum": 1,
      "maximum": 10
    }
  },
  "required": ["claim"],
  "additionalProperties": false
}
{
  "$id": "potm.kernel.acceptance.agreement.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Acceptance Agreement",
  "description": "Kernel entry acceptance agreement and effects.",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "token": { "type": "string", "const": "[KERNEL_ENTRY]" },
    "normalization": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "trim_whitespace": { "type": "boolean" },
        "case_sensitive": { "type": "boolean" },
        "single_line_only": { "type": "boolean" }
      },
      "required": ["trim_whitespace", "case_sensitive", "single_line_only"]
    },
    "scope": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "grants": { "type": "array", "items": { "type": "string" }, "maxItems": 16 },
        "denies": { "type": "array", "items": { "type": "string" }, "maxItems": 16 },
        "exceptions": {
          "type": "object",
          "additionalProperties": true,
          "properties": {
            "export": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "condition": { "type": "string" },
                "normalization": { "type": "string", "enum": ["strict_match"] },
                "header": {
                  "type": "array",
                  "items": { "type": "string" },
                  "minItems": 2,
                  "maxItems": 2
                }
              },
              "required": ["condition", "normalization", "header"]
            }
          }
        }
      },
      "required": ["grants", "denies"]
    },
    "on_success": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "set": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "meta_locus": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "accepted": { "type": "boolean" },
                "fracture_active": { "type": "boolean" },
                "containment": { "type": "boolean" },
                "review_queue": { "type": "array", "items": { "type": "string" } }
              },
              "required": ["accepted", "fracture_active", "containment", "review_queue"]
            }
          },
          "required": ["meta_locus"]
        },
        "next": { "type": "string", "const": "MENU.OPEN" },
        "idempotent_message": { "type": "string" },
        "confirmation": { "type": "string" }
      },
      "required": ["set", "next", "confirmation"]
    },
    "on_fail": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "response": { "type": "string" }
      },
      "required": ["response"]
    },
    "on_revoke": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "trigger": { "type": "string", "const": "[KERNEL_EXIT]" },
        "set": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "meta_locus": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "accepted": { "type": "boolean" },
                "fracture_active": { "type": "boolean" },
                "containment": { "type": "boolean" },
                "review_queue": { "type": "array", "items": { "type": "string" } }
              },
              "required": ["accepted", "fracture_active", "containment", "review_queue"]
            }
          },
          "required": ["meta_locus"]
        },
        "next": { "type": "string", "const": "ACK.EXIT" },
        "response": { "type": "string" }
      },
      "required": ["trigger", "set", "next", "response"]
    },
    "ledger": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "emit_on_accept": { "type": "boolean" },
        "emit_on_exit": { "type": "boolean" }
      },
      "required": ["emit_on_accept", "emit_on_exit"]
    }
  },
  "required": ["token", "normalization", "scope", "on_success", "on_fail", "on_revoke", "ledger"]
}

{
  "$id": "potm.kernel.guardian.trigger.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "guardian.trigger — Payload",
  "description": "Request Guardian evaluation of a trigger.",
  "type": "object",
  "required": ["triggerId", "severity", "ts"],
  "additionalProperties": false,
  "properties": {
    "triggerId": { "type": "string", "description": "Identifier of the trigger condition" },
    "severity": { "type": "string", "enum": ["soft", "hard"], "description": "Trigger severity" },
    "ts": { "type": "string", "format": "date-time", "description": "Timestamp of trigger" },
    "details": { "type": "string", "description": "Optional context" }
  }
}

{
  "$id": "potm.kernel.guardian.trigger.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "guardian.trigger — Result",
  "description": "Confirmation that Guardian accepted the trigger.",
  "type": "object",
  "required": ["status", "triggerId", "severity", "ts"],
  "additionalProperties": false,
  "properties": {
    "status": { "type": "string", "const": "accepted" },
    "triggerId": { "type": "string" },
    "severity": { "type": "string", "enum": ["soft", "hard"] },
    "ts": { "type": "string", "format": "date-time" }
  }
}

{
  "$id":"potm.kernel.latency.validator.payload.v1",
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "type":"object","additionalProperties":false,
  "required":["meta","observed_latency_ms"],
  "properties":{
    "meta":{"type":"object","additionalProperties":false,"required":["latency_mode"],
      "properties":{"latency_mode":{"type":"string","enum":["lite","standard","strict"]}}
    },
    "observed_latency_ms":{"type":"integer","minimum":0}
  }
}
{
  "$id":"potm.kernel.latency.validator.result.v1",
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "type":"object","additionalProperties":false,
  "required":["decision","mode","observed_ms","p50_ms","p95_ms"],
  "properties":{
    "decision":{"type":"string","enum":["allow","warn","block"]},
    "mode":{"type":"string","enum":["lite","standard","strict"]},
    "observed_ms":{"type":"integer","minimum":0},
    "p50_ms":{"type":"integer","minimum":0},
    "p95_ms":{"type":"integer","minimum":0},
    "code":{"type":"string","enum":["E_LATENCY_MODE","E_LATENCY_INVARIANT","W_LATENCY_BREACH"]}
  }
}

{
  "$id": "potm.kernel.ledger.latency_breach.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Latency Breach Ledger Entry",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "ts": { "type": "string", "format": "date-time" },
    "mode": { "type": "string", "enum": ["lite", "standard", "strict"] },
    "observed_ms": { "type": "integer", "minimum": 0 },
    "p50_ms": { "type": "integer", "minimum": 0 },
    "p95_ms": { "type": "integer", "minimum": 0 },
    "code": { "type": "string", "enum": ["W_LATENCY_BREACH", "E_LATENCY_INVARIANT"] }
  },
  "required": ["ts", "mode", "observed_ms", "p50_ms", "p95_ms", "code"]
}
{
  "$id": "potm.kernel.move.align_scan.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "move.align_scan payload",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "aim": { "type": "string", "maxLength": 2000 },
    "last_output": { "type": "string", "maxLength": 2000 }
  },
  "required": ["aim", "last_output"]
}

{
  "$id": "potm.kernel.move.align_scan.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "move.align_scan result",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "misalignment": { "type": "string", "maxLength": 2000 },
    "suggestion": { "type": "string", "maxLength": 2000 }
  },
  "required": ["misalignment", "suggestion"]
}

{
  "$id": "potm.kernel.move.drift_check.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "move.drift_check payload",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "aim": { "type": "string", "maxLength": 2000 },
    "thread": {
      "type": "array",
      "items": { "type": "string", "maxLength": 2000 },
      "minItems": 1,
      "maxItems": 64
    }
  },
  "required": ["aim", "thread"]
}

{
  "$id": "potm.kernel.move.drift_check.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "move.drift_check result",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "drift_description": { "type": "string", "maxLength": 2000 },
    "severity": { "type": "string", "enum": ["low", "med", "high"] }
  },
  "required": ["drift_description", "severity"]
}

{
  "$id": "potm.kernel.move.fracture.payload.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "move.fracture payload",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "beacon_id": { "type": "string", "maxLength": 128 },
    "context": { "type": "string", "maxLength": 2000 }
  },
  "required": ["beacon_id", "context"]
}

{
  "$id": "potm.kernel.move.fracture.result.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "move.fracture result",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "fracture_ids": { "type": "array", "items": { "type": "string" }, "minItems": 1, "maxItems": 8 },
    "route_hint": { "type": "string", "enum": ["continue", "stop", "openq", "redteam"] }
  },
  "required": ["fracture_ids", "route_hint"]
}

{
  "cap": {
    "latency": {
      "lite":     { "p50_ms": 2000, "p95_ms": 4000 },
      "standard": { "p50_ms": 4000, "p95_ms": 6000 },
      "strict":   { "p50_ms": 8000, "p95_ms": 12000 }
    },
    "ledger_max": 512
  }
}
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "potm.kernel.router.emission.v1",
  "title": "Router Emission ($defs for lens results)",
  "type": "object",
  "additionalProperties": false,
  "$defs": {
    "lens.define.result": {
      "type": "object",
      "additionalProperties": false,
      "properties": { "ok": { "const": true }, "id": { "type": "string" }, "definition": { "type": "string" } },
      "required": ["ok", "id", "definition"]
    },
    "lens.check.result": {
      "type": "object",
      "additionalProperties": false,
      "properties": { "ok": { "const": true }, "id": { "type": "string" }, "valid": { "type": "boolean" } },
      "required": ["ok", "id", "valid"]
    },
    "lens.trace.result": {
      "type": "object",
      "additionalProperties": false,
      "properties": { "ok": { "const": true }, "id": { "type": "string" }, "trace": { "type": "array", "items": { "type": "string" } } },
      "required": ["ok", "id", "trace"]
    },
    "lens.refuse.result": {
      "type": "object",
      "additionalProperties": false,
      "properties": { "ok": { "const": true }, "reason": { "type": "string" } },
      "required": ["ok", "reason"]
    }
  }
}
{
  "$id":"potm.kernel.router.envelope.v1",
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "type":"object",
  "additionalProperties": false,
  "required": ["id","request_id","payload","meta"],
  "properties": {
    "id": { "type":"string","pattern":"^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*$" },
    "request_id": { "type":"string","minLength":8,"maxLength":64 },
    "payload": { "type":"object","additionalProperties": true },
    "observed_latency_ms": { "type":"integer","minimum":0 },
    "meta": {
      "type":"object","additionalProperties":false,
      "required":["latency_mode"],
      "properties": {
        "latency_mode": { "type":"string","enum":["lite","standard","strict"] },
        "containment": { "type":"boolean" },
        "trace": { "type":"boolean","default":false },
        "origin": { "type":"string","maxLength":64 }
      }
    }
  }
}

{
  "$id":"potm.kernel.router.error.v1",
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "type":"object","additionalProperties":false,
  "required":["ok","code","reason"],
  "properties":{
    "ok":{"const":false},
    "code":{"type":"string","enum":["E_NAMESPACE","E_TOOL_NOT_FOUND","E_PAYLOAD","E_PRECONDITION","E_QUOTA","E_DISABLED","E_INVARIANT","E_IDEMPOTENCY","E_CONTAINMENT_BLOCKED","E_LATENCY_INVARIANT"]},
    "reason":{"type":"string","maxLength":512},
    "message":{"type":"string","maxLength":300},
    "recovery_hint":{"type":"string","maxLength":160},
    "severity":{"type":"string","enum":["info","warn","hard"]},
    "trace":{"type":"array","items":{"type":"string"},"maxItems":32}
  }
}

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "potm.kernel.tool.index.v1",
  "tools": [
    {
      "id": "lens.define",
      "payload_schema": "runtime/spec/min/lens_define.min.v1.json",
      "result_schema":  "runtime/spec/router_emission.json#/$defs/lens.define.result"
    },
    {
      "id": "lens.check",
      "payload_schema": "runtime/spec/min/lens_check.min.v1.json",
      "result_schema":  "runtime/spec/router_emission.json#/$defs/lens.check.result"
    },
    {
      "id": "lens.trace",
      "payload_schema": "runtime/spec/min/lens_trace.min.v1.json",
      "result_schema":  "runtime/spec/router_emission.json#/$defs/lens.trace.result"
    },
    {
      "id": "lens.refuse",
      "payload_schema": "runtime/spec/min/lens_refuse.min.v1.json",
      "result_schema":  "runtime/spec/router_emission.json#/$defs/lens.refuse.result"
    },
    {
      "id": "move.align_scan",
      "payload_schema": "potm.kernel.move.align_scan.payload.v1",
      "result_schema":  "potm.kernel.move.align_scan.result.v1"
    },
    {
      "id": "move.drift_check",
      "payload_schema": "potm.kernel.move.drift_check.payload.v1",
      "result_schema":  "potm.kernel.move.drift_check.result.v1"
    },
    {
      "id": "move.fracture",
      "payload_schema": "potm.kernel.move.fracture.payload.v1",
      "result_schema":  "potm.kernel.move.fracture.result.v1"
    },
    {
      "id": "guardian.trigger",
      "payload_schema": "potm.kernel.guardian.trigger.payload.v1",
      "result_schema":  "potm.kernel.guardian.trigger.result.v1"
    }
  ]
}
{
  "$id": "potm.kernel.lens.check.min.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "allOf": [
    { "$ref": "../../schema/lens.check.payload.v1.json" },
    {
      "type": "object",
      "properties": {
        "assumption": { "type": "string", "minLength": 3, "maxLength": 256 },
        "method": { "type": "string", "enum": ["contrast","example","edge","proxy","other"] },
        "proxy": { "type": "string", "maxLength": 120 }
      },
      "required": ["assumption"],
      "additionalProperties": false
    }
  ]
}
{
  "$id": "potm.kernel.lens.define.min.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "allOf": [
    { "$ref": "../../schema/lens.define.payload.v1.json" },
    {
      "type": "object",
      "properties": {
        "term": { "type": "string", "minLength": 1, "maxLength": 120 },
        "context": { "type": "string", "maxLength": 280 }
      },
      "required": ["term"],
      "additionalProperties": false
    }
  ]
}
{
  "$id": "potm.kernel.lens.refuse.min.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "allOf": [
    { "$ref": "../../schema/lens.refuse.payload.v1.json" },
    {
      "type": "object",
      "properties": {
        "reason": {
          "type": "string",
          "enum": [
            "safety_risk","privacy_risk","policy_block",
            "unsupported_scope","insufficient_info","other"
          ]
        },
        "note": { "type": "string", "maxLength": 200 },
        "forward_route": {
          "type": "object",
          "required": ["label","suggestion"],
          "additionalProperties": false,
          "properties": {
            "label": { "type": "string", "maxLength": 64 },
            "suggestion": { "type": "string", "maxLength": 200 }
          }
        }
      },
      "required": ["reason","forward_route"],
      "additionalProperties": false
    }
  ]
}
{
  "$id": "potm.kernel.lens.trace.min.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "allOf": [
    { "$ref": "../../schema/lens.trace.payload.v1.json" },
    {
      "type": "object",
      "properties": {
        "depth": { "type": "integer", "minimum": 2, "maximum": 4 }
      },
      "required": ["claim"],
      "additionalProperties": false
    }
  ]
}
{
  "$id": "potm.kernel.policy.cap.v1",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Kernel Policy Caps (Minimal)",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "cap": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "latency": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "lite": { "$ref": "#/$defs/latency_mode" },
            "standard": { "$ref": "#/$defs/latency_mode" },
            "strict": { "$ref": "#/$defs/latency_mode" }
          },
          "required": ["lite", "standard", "strict"]
        }
      },
      "required": ["latency"]
    },
    "ledger_max": { "type": "integer", "minimum": 1 }
  },
  "required": ["cap", "ledger_max"],
  "$defs": {
    "latency_mode": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "p50_ms": { "type": "integer", "minimum": 0 },
        "p95_ms": { "type": "integer", "minimum": 0 }
      },
      "required": ["p50_ms", "p95_ms"]
    }
  }
}
