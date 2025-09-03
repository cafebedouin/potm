
2. BS Detect

Diagnostics doc: diagnostics/bs_detect.md.

What’s missing:

Not wired into kernel contracts. No schemas, no invoke/result examples.

Should be treated as a diagnostic tool with:

schema: bs_detect.report_payload.json, bs_detect.report_result.json

examples: e.g., bs_detect_violation.json

optional ledger entries (if BS flags must be auditable).

70_state.md would need a “Diagnostic moves” subsection to point to it.

3. Spotchecker (sentinel_spotcheck.md)

Diagnostics doc exists.

Missing wiring: same as BS Detect. Needs payload/result schema + examples.

Should probably log spotcheck events to the ledger buffer.

4. Fracture Finder

Docs: meta/fracture_finder.md, canon/extended/diagnostics/fracture_finder.md, plus playbooks/fracture_finder_playbook.md.

Kernel integration:

Not yet tied into 75_fracture.md or the runtime.

Should generate events when anomalies are detected → ledger entries (fracture_event subtype).

Needs schemas (fracture.finder_payload.json, fracture.finder_result.json) and minimal examples.

5. Menu (practice menu, engagement flow)

Current state:

kernel/75_practice_menu.md defines the structure.

v1.4.2+ has modules/engagement_flow.md and protocols/engagement_flow.md.

Missing:

No schemas for menu state or invocation. E.g., menu.invoke_payload.json, menu.result.json.

No examples under runtime/examples/.

Should be referenced in 70_state.md as an entry-point diagnostic/mode selector.

6. Ledger Gaps

Fracture & Containment covered.

Not covered: guardian events, diagnostics (bs_detect, spotcheck, fracture_finder), menu selections.

Likely need new schemas:

ledger.guardian_event.json

ledger.diagnostic_event.json

ledger.menu_event.json

✅ In short:
The kernel wiring is complete for fracture + containment, but the guardian, bs_detect, spotchecker, fracture_finder, and menu subsystems are “floating”: present in canon narrative, not yet enforced by schemas/examples/specs/ledger.

Below is a practical audit of canon, focused on whether kernel docs reference each
file. I list candidates to archive/move, plus anything referenced but missing (with
suggested placement).

Unreferenced In Kernel (candidates to archive/move)

- Root
    - canon_kernel.md: composite doc; not referenced by kernel docs. Suggest move to
meta/ or keep as build output.
    - onboarding_kernel.md: onboarding guidance; not referenced. Suggest keep in meta/
or interpretative/.
- kernel/
    - combined_kernel.md: generated aggregate; not referenced. Suggest keep as build
artifact or move to meta/.
    - 00_preamble.md: not referenced. If you want it in canon, link it from kernel/
index.md; otherwise move to meta/.
    - protocols/
    - elements_of_refusal_protocol.md, floor_integration_stack.md,
microkernel_self_diagnostic_protocol.md: no current references in kernel docs.
Practitioner-facing; suggest move to extended/coordination/ or keep here but add refs
where appropriate.
- extended/
    - diagnostics/
    - cross_model_diagnostics.md and cross_model_diagnostics_harness.md (both top-level
and in diagnostics/cross_model_diagnostics/ subdir): duplicates; keep only one
canonical placement (prefer the nested directory version).
    - logs/fracture_log.md: not referenced by kernel; optional practitioner log.
    - integrity_report.md, maintenance_flow_playbook.md, rb_dualtrack.md, rbtrack.md,
version_info_playbook.md, etc.: not referenced by kernel; keep as practitioner
playbooks in extended/.
    - fracture/fracture_meta_unity.md, fracture_taxonomy_master_table.md: not
referenced directly; can remain as practitioner annexes (see “Missing referenced
content” below).
- fracture_finder.md (top-level): likely redundant with extended/diagnostics/fracture/
fracture_finder.md; keep only the diagnostics/fracture version.
- mirror_protocol_subsystem.md, mirror_subsystem_checklist_v1.0.md: not referenced by
kernel; keep in extended/.
- tools/: lint scripts and lineage utilities are repo tooling; not referenced by
kernel; keep in extended/tools.
- interpretative/
    - kernel_1_6_dev.md: not referenced; likely historical. Keep in interpretative/
or archive.
    - data/zuihitsu/zuihitsu_test.txt: appears to be a dev/test file; menu doc
references only zuihitsu_combined.txt. Suggest remove or move to a developer fixtures
folder.
    - dignity/, doctrines/, frameworks/potm_framework.md, glossary/guidelines: not
referenced by kernel; fine to keep as interpretative materials.

Referenced But Missing or Needing Alignment

- Closure annex (descriptive pointers)
    - kernel/80_closure.md mentions ANNEX:FRACTURE_TAXONOMY_MINI. There is no concrete
file named “fracture_taxonomy_mini.md”. Suggest add:
    - extended/diagnostics/fracture/fracture_taxonomy_mini.md (curated subset of master
table), or
    - change the pointer to the existing extended/diagnostics/fracture/
fracture_taxonomy_master_table.md.
- Protocol index (optional)
    - kernel/index.md now has Subsystems, Diagnostics, and Protocols. If you want
00_preamble.md to remain, add a link to it in index.md.


- Deduplicate extended/diagnostics/cross_model_diagnostics* (keep nested directory
variants).

- Mark canonical composites (canon_kernel.md, combined_kernel.md) as
build artifact.

- kernel/00_preamble.md should stay, reference it from kernel/index.md

- revise closure annex to point to the extended/diagnostics/fracture/fracture_taxonomy_master_table.md that already exists.

---


**PROJECT CONTEXT**

You are editing a markdown-spec “kernel” repo for PoTM. Files are deterministic specs (no runtime code). Behavior is defined by documents under `kernel/`.

Goal: Modify the **ENTRY\_GATE** flow so that:

1. On any first inbound message (e.g., `menu`, free text, etc.), the Agreement is shown **first**.
2. When the user sends `[KERNEL_ENTRY]`, show the normal acceptance confirmation **then** a one-line acknowledgement of the original starter input (what they typed before acceptance), and then open the menu.

Do not change other invariants or schemas. Maintain fail-closed behavior and idempotence.

---

**FILES TO EDIT**

1. `kernel/70_state.md` (meta\_locus initial state)
2. `kernel/10_entry_gate.md` (ENTRY\_GATE Initialization + Dispatch Rules)
3. (Optional, only if present) any examples that rely on the entry handshake under `runtime/examples/` to reflect the new emissions.

---

**REQUIRED CHANGES (SPEC-LEVEL)**

A) **State — add a field to meta\_locus**

* Add `initial_trigger: null` to the *initial state* of `meta_locus`.
* Type: `string | null`, session-local, trimmed raw first inbound message before acceptance.
* Never mutated after acceptance; set only on the first pre-accept message.

B) **ENTRY\_GATE — Initialization**

* Explicitly initialize `meta_locus.initial_trigger = null` on session start.

C) **ENTRY\_GATE — Dispatch Rules**

* For `accepted=false` and **any non-`[KERNEL_ENTRY]` input**:

  * If `meta_locus.initial_trigger == null`, set it to the *trimmed* raw input (guard: ignore empty string and `[KERNEL_ENTRY]`).
  * Emit the **Agreement Prompt** verbatim (unchanged text).
  * Do **not** emit “Not accepted…”; Agreement takes precedence.
  * Next state remains `accepted=false`.

* For `accepted=false` and `[KERNEL_ENTRY]`:

  * Set `accepted=true`. Reset other flags **but preserve `initial_trigger`**.
  * Emit the standard confirmation string:

    > Accepted. Constraints on. You’re in the kernel. (No export by default.)
  * If `initial_trigger` is not null, emit exactly one acknowledgement line:

    > Startup note: you began with → {initial\_trigger}
  * Trigger `MENU.OPEN`.
  * Next state: `accepted=true`.

* For `accepted=true` and `[KERNEL_ENTRY]` (idempotence):

  * Keep the existing behavior: “Agreement already active. Opening menu.” → `MENU.OPEN`.

* Keep token validation unchanged: single-line, exact, case-sensitive `[KERNEL_ENTRY]`.

D) **Idempotence & Audit**

* `MENU.OPEN` remains safe to call repeatedly.
* Do **not** add ledger rows for handshake-only exchanges (no change to current policy).
* Ensure changes do not alter export guards or recap behavior.

E) **Copy edits / Guards**

* When setting `initial_trigger`, trim whitespace. Ignore `[KERNEL_ENTRY]`. Ignore empty strings.
* Do not re-emit the Agreement **after** acceptance; per requirement, acceptance text + acknowledgement + menu only.

---

**ACCEPTANCE CRITERIA (SCENARIO-BASED EMISSIONS)**

1. **Start with `menu`**

* Input #1: `menu`

  * State: `accepted=false`
  * Action: `initial_trigger ← "menu"`; emit Agreement Prompt.
* Input #2: `[KERNEL_ENTRY]`

  * Emit:

    ```
    Accepted. Constraints on. You’re in the kernel. (No export by default.)
    Startup note: you began with → menu
    ```
  * Then `MENU.OPEN` triggers.

2. **Start with arbitrary text**

* Input #1: `i feel ready`

  * `initial_trigger ← "i feel ready"`, Agreement Prompt.
* Input #2: `[KERNEL_ENTRY]`

  * Acceptance line + `Startup note: you began with → i feel ready` + `MENU.OPEN`.

3. **Start with `[KERNEL_ENTRY]` directly**

* Input #1: `[KERNEL_ENTRY]`

  * Acceptance line, **no** startup note (since no prior trigger), then `MENU.OPEN`.

4. **Duplicate entry after acceptance**

* Input (after accepted=true): `[KERNEL_ENTRY]`

  * Emit: “Agreement already active. Opening menu.” → `MENU.OPEN`.

5. **Whitespace / trivial inputs pre-accept**

* Input #1: `   `

  * Agreement Prompt (do **not** set `initial_trigger` to empty).
* Input #2: `[KERNEL_ENTRY]`

  * Acceptance line only (no startup note), then `MENU.OPEN`.

6. **Case-sensitivity validation**

* Input: `[kernel_entry]` (lowercase)

  * Treat as “any other input” → Agreement Prompt; do not accept.

---

**OUTPUT FORMAT**

Produce unified diffs for each edited file, minimal and focused. Example structure:

```diff
*** a/kernel/70_state.md
--- b/kernel/70_state.md
@@
   - accepted: false
   - containment: false
   - review_queue: []
   - latency_mode: standard
   - mode_profile: standard
+  - initial_trigger: null     # string|null; first pre-accept inbound token (trimmed)

*** a/kernel/10_entry_gate.md
--- b/kernel/10_entry_gate.md
@@
 ## Initialization
- - Initialize `meta_locus` (externalized example): see `runtime/examples/state_meta_locus.json`
+ - Initialize `meta_locus` (externalized example): see `runtime/examples/state_meta_locus.json`
+ - Set `meta_locus.initial_trigger = null`
@@
 ## Dispatch Rules
- | any other input | accepted=false | Emit: “Not accepted. Reply with exactly: [KERNEL_ENTRY]” | accepted=false |
+ | any other input | accepted=false | If `initial_trigger == null` set it to trimmed input (ignore empty or "[KERNEL_ENTRY]"); Emit Agreement Prompt | accepted=false |
@@
- | `[KERNEL_ENTRY]` | accepted=false | Set `accepted=true`, reset other flags; Emit confirmation; Re-emit Agreement Prompt; Trigger `MENU.OPEN` | accepted=true |
+ | `[KERNEL_ENTRY]` | accepted=false | Set `accepted=true` (preserve `initial_trigger`); Emit confirmation; If `initial_trigger` present, also emit: “Startup note: you began with → {initial_trigger}”; Trigger `MENU.OPEN` | accepted=true |
```

If examples need updates, add small diffs under `runtime/examples/` to reflect the new emissions for the above scenarios.

---

**NON-GOALS**

* Do not change beacon logic, lenses, micro-moves, mode profiles, or recap/export policy.
* Do not introduce external I/O or background tasks.
* Do not alter token validation rules for `[KERNEL_ENTRY]`.

---

**DELIVERABLES**

1. Diffs for `kernel/70_state.md` and `kernel/10_entry_gate.md` (and any touched examples).
2. A short commit message:

   * `entry_gate: show Agreement first; acknowledge initial trigger after acceptance`
3. A brief “verification log” enumerating the 6 acceptance scenarios and showing expected emissions.



---

# PROJECT CONTEXT

You are editing a markdown-spec repo for PoTM. Kernel invariants must remain deterministic, fail-closed, and session-local. UX belongs to the interpretive layer (adapters), while the kernel exposes stable contracts (glyphs, lenses, moves).

**Goal:** Replace the visible menu with four practitioner-facing actions and enable optional **dynamic (context-generated)** artifacts with provenance. Internal constructs (Lenses, Micromoves, Beacons, Modes) remain hidden from users.

User menu (post-acceptance) must show **exactly**:

1. Card draw
2. Journal prompt
3. Zuihitsu
4. Describe an idea / problem / situation

Selecting any item should produce a single artifact (text) via `glyph.invoke`. If `dynamic_generated` is used, include provenance, rationale, and confidence.

---

# FILES TO EDIT / ADD

* **Edit:** `kernel/10_entry_gate.md`  — change user-visible MENU copy only; keep routing/logic intact.
* **Add:** `interpretive/menu_user_surface.md` — adapter contract and UX rules.
* **Edit:** `runtime/spec/glyph.invoke_payload.json` — add new types + generation mode + optional context/constraints.
* **Edit:** `runtime/spec/glyph.result.json` — add provenance, rationale, and confidence fields; allow static pack or generated source.
* **Add:** `extended/generative/prompt_forge.md` — selection rules for dynamic generation.
* **Edit:** `kernel/90_policy.md` (or equivalent) — caps/quotas for artifacts and dynamic generation.
* **Add examples:**

  * `runtime/examples/glyph_card_draw_static.json`
  * `runtime/examples/glyph_card_draw_dynamic.json`
  * `runtime/examples/glyph_journal_prompt.json`
  * `runtime/examples/glyph_zuihitsu.json`
  * `runtime/examples/glyph_describe_intake.json`

> Do **not** change router allow-lists, idempotency rules, or acceptance gate semantics.

---

# REQUIRED SPEC CHANGES

## 1) ENTRY MENU (copy only)

Update the MENU section so adapters render only the four options. Do not rename tools or change dispatch rules.

```diff
*** a/kernel/10_entry_gate.md
--- b/kernel/10_entry_gate.md
@@
 ## Idempotence & Audit
 `MENU.OPEN` is safe to call repeatedly.
 Ledger rows are emitted only for actual artifacts, not for handshake exchanges.
 
+---
+
+## MENU.OPEN — Practitioner-Facing Menu (Adapter Copy)
+
+When `accepted == true` and `MENU.OPEN` is triggered, adapters MUST display only:
+
+1) **Card draw**
+2) **Journal prompt**
+3) **Zuihitsu**
+4) **Describe an idea / problem / situation**
+
+Selecting an item MUST translate into a single `glyph.invoke` call (see glyph specs).
+Internal constructs (lenses, micro-moves, beacons, modes) remain hidden from the practitioner.
```

## 2) Adapter contract for the new menu

Create an interpretive doc that maps menu selections → glyph calls.

```patch
*** /dev/null
--- b/interpretive/menu_user_surface.md
+# Practitioner Menu — Adapter Contract
+
+## Options (exact strings)
+1) Card draw
+2) Journal prompt
+3) Zuihitsu
+4) Describe an idea / problem / situation
+
+## Mapping to Kernel Call
+All options invoke `glyph.invoke`:
+- Card draw → `{ type:"card_draw", mode:"static_pack" | "dynamic_generated", context?, constraints? }`
+- Journal prompt → `{ type:"journal_prompt", ... }`
+- Zuihitsu → `{ type:"zuihitsu", ... }`
+- Describe… → `{ type:"describe_intake", ... }`
+
+### Context & Constraints (optional)
+- `context` is an adapter-supplied snapshot (session-local, no PII export).
+- `constraints` can shape tone, word caps, intensity, or topic.
+
+### Rendering
+Adapters render only the returned artifact text and (optionally) a minimal provenance ribbon when `source:"generated"`.
+No internal tool names are surfaced to the practitioner.
```

## 3) `glyph.invoke` payload — new enums and knobs

```diff
*** a/runtime/spec/glyph.invoke_payload.json
--- b/runtime/spec/glyph.invoke_payload.json
@@
 {
   "type": "object",
   "additionalProperties": false,
   "properties": {
-    "type": { "enum": ["<existing_types>"] }
+    "type": { "enum": ["card_draw","journal_prompt","zuihitsu","describe_intake" /* plus existing types */] },
+    "mode": { "enum": ["static_pack","dynamic_generated"], "default": "static_pack" },
+    "context": { "type": "object" },
+    "constraints": { "type": "object" }
   },
-  "required": ["type"],
+  "required": ["type"],
   "title": "glyph.invoke_payload"
 }
```

## 4) `glyph.result` — artifact + provenance + rationale + confidence

```diff
*** a/runtime/spec/glyph.result.json
--- b/runtime/spec/glyph.result.json
@@
 {
   "type": "object",
   "additionalProperties": false,
   "properties": {
     "artifact": {
       "type": "object",
       "properties": {
-        "type": { "enum": ["<existing_types>"] },
+        "type": { "enum": ["card_draw","journal_prompt","zuihitsu","describe_intake" /* plus existing types */] },
         "content": { "type": "string", "maxLength": 1200 },
-        "source": { "type": "string" }
+        "source": { "type": "string", "pattern": "^(pack:[^\\s/]+/[^\\s/]+|generated)$" }
       },
       "required": ["type","content","source"]
     },
+    "provenance": {
+      "type": "object",
+      "additionalProperties": false,
+      "properties": {
+        "inputs": { "type": "array", "items": { "type": "string" }, "maxItems": 8 },
+        "model": { "type": "string" },
+        "time": { "type": "string", "format": "date-time" },
+        "signals": { "type": "array", "items": { "type": "string" }, "maxItems": 8 }
+      },
+      "required": ["time"]
+    },
+    "why_this": { "type": "string", "maxLength": 200 },
+    "fit_confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
   },
-  "required": ["artifact"]
+  "required": ["artifact","provenance","why_this","fit_confidence"]
 }
```

## 5) Dynamic generation rules (spec guidance)

```patch
*** /dev/null
--- b/extended/generative/prompt_forge.md
+# Prompt Forge — Dynamic Generation Rules
+
+Use `mode:"dynamic_generated"` only when:
+1) Pack coverage is low or mismatched to `context`, or
+2) `constraints` specify a shape not found in packs.
+
+Required fields when `artifact.source == "generated"`:
+- `provenance.inputs`: optional list of pack titles or descriptors consulted.
+- `why_this`: one sentence on fit (<= 24 words).
+- `fit_confidence`: [0.0–1.0] plus at least one observable proxy in `signals` (e.g., keyword match count).
+
+Beacons remain active: avoid oracle tone; mark uncertainty; respect practitioner safety.
```

## 6) Policy caps & quotas

```diff
*** a/kernel/90_policy.md
--- b/kernel/90_policy.md
@@
+## Artifact Caps (Prompts)
+- Default word caps:
+  - card_draw, journal_prompt: 60–120 words
+  - zuihitsu: ≤ 180 words (fragmented style allowed)
+  - describe_intake scaffold: ≤ 120 words
+- Export: gated under `artifact_prompt` (deny by default).
+- Dynamic generation quota: ≤ 5 per session.
```

## 7) Examples (happy paths)

```patch
*** /dev/null
--- b/runtime/examples/glyph_card_draw_static.json
+{ "tool.call": { "id": "glyph.invoke", "payload": {
+  "type": "card_draw", "mode": "static_pack", "constraints": {"tone":"gentle"}
+}},
+ "tool.result": { "artifact": {
+   "type": "card_draw", "content": "Draw: Name the tension you’re avoiding. Give it one sentence.", "source": "pack:core/001"
+ }, "provenance": { "time": "2025-08-30T12:00:00Z" },
+ "why_this": "Matches your recent mention of avoidance.",
+ "fit_confidence": 0.72 } }
```

```patch
*** /dev/null
--- b/runtime/examples/glyph_card_draw_dynamic.json
+{ "tool.call": { "id": "glyph.invoke", "payload": {
+  "type": "card_draw", "mode": "dynamic_generated", "context": {"last_user":"deadline anxiety"}
+}},
+ "tool.result": { "artifact": {
+   "type": "card_draw", "content": "Card: List three concrete deadlines and one smallest next move for each.", "source": "generated"
+ }, "provenance": { "inputs": ["core pack"], "time": "2025-08-30T12:01:00Z", "signals":["matched: deadlines, anxiety"] },
+ "why_this": "Closer fit than nearest pack card for deadline-specific stress.",
+ "fit_confidence": 0.68 } }
```

```patch
*** /dev/null
--- b/runtime/examples/glyph_journal_prompt.json
+{ "tool.call": { "id": "glyph.invoke", "payload": { "type":"journal_prompt" }},
+  "tool.result": { "artifact": { "type":"journal_prompt", "content":"Journal: What outcome matters this week, and what would you trade for it?", "source":"pack:journal/014" },
+  "provenance": { "time":"2025-08-30T12:02:00Z" },
+  "why_this":"Weekly cadence inferred; prompt emphasizes tradeoffs.",
+  "fit_confidence":0.7 } }
```

```patch
*** /dev/null
--- b/runtime/examples/glyph_zuihitsu.json
+{ "tool.call": { "id":"glyph.invoke", "payload": { "type":"zuihitsu", "constraints":{"fragments":4} } },
+  "tool.result": { "artifact": { "type":"zuihitsu", "content":"• The coffee went cold.\n• The email stayed open.\n• The fear shrank when named.\n• The next inch is enough.", "source":"generated" },
+  "provenance": { "time":"2025-08-30T12:03:00Z" },
+  "why_this":"Fragmented style can bypass overthinking.",
+  "fit_confidence":0.64 } }
```

```patch
*** /dev/null
--- b/runtime/examples/glyph_describe_intake.json
+{ "tool.call": { "id":"glyph.invoke", "payload": { "type":"describe_intake" } },
+  "tool.result": { "artifact": { "type":"describe_intake", "content":"Describe: Situation • Stakes • 3 facts anyone could verify • 1 step you control.", "source":"pack:intake/001" },
+  "provenance": { "time":"2025-08-30T12:04:00Z" },
+  "why_this":"Structures intake without advice; aligns with beacons.",
+  "fit_confidence":0.75 } }
```

---

# ACCEPTANCE CRITERIA

1. After `[KERNEL_ENTRY]`, `MENU.OPEN` shows **only** the four items (no internal tool names).
2. Each menu selection maps to a **single** `glyph.invoke` and returns an artifact.
3. When `mode:"dynamic_generated"`, the result includes `provenance`, `why_this`, and `fit_confidence`; `artifact.source == "generated"`.
4. Static path supports `artifact.source == "pack:<pack_id>/<card_id>"`.
5. Policy caps/quotas enforce word limits and ≤5 dynamic generations per session.
6. No router or invariant changes beyond schema additions above. Idempotency unaffected.

---

# COMMIT MESSAGE

```
menu: replace engine jargon with 4 user actions; add dynamic generation path with provenance
- ENTRY_GATE menu copy -> 4 items
- glyph.invoke/result schemas extended
- adapter contract for practitioner menu
- dynamic generation rules + policy caps/quotas
- examples for static/dynamic artifacts
```

---

# VERIFICATION CHECKLIST

* Trigger `MENU.OPEN` after acceptance → four items visible.
* Run each example payload → schema-valid results.
* Toggle `mode` static vs dynamic → sources and provenance behave as specified.
* Confirm no internal tool names leak into user-visible text.

---


You are modifying an existing PoTM adapter. Do not change the kernel.
Goal: when the practitioner selects a menu option (1–4), the adapter must immediately issue the correct glyph.invoke call and render the result—no confirmation layer, no backend chatter.

Context (read first)

The kernel requires an entry handshake; plain text is inert; only structured tool calls execute. The adapter shows a 4-item practitioner menu and maps selections to glyph.invoke.

Keep the menu contract exactly: four options only; internal constructs remain hidden.

Always respect beacons (clarity, no simulated wisdom, etc.) in user copy—be concise and action-oriented.

What to change (adapter only)

Menu UX copy

Replace any prompt that explains backend behavior or asks “should I proceed?” with:


Here’s a drop-in **Codex prompt** you can paste into your code assistant. It tells it to examine the current adapter and implement the “menu does the thing immediately” behavior **without changing the kernel**, and to work strictly within existing constraints.

---

# 📥 Prompt for Codex (Adapter Fast-Path Implementation)

**You are modifying an existing PoTM adapter. Do not change the kernel.**
Goal: when the practitioner selects a menu option (1–4), the adapter must immediately issue the correct `glyph.invoke` call and render the result—no confirmation layer, no backend chatter.

## Context (read first)

* The kernel requires an entry handshake; plain text is inert; only structured tool calls execute. The adapter shows a 4-item practitioner menu and maps selections to `glyph.invoke`.
* Keep the menu contract exactly: four options only; internal constructs remain hidden.
* Always respect beacons (clarity, no simulated wisdom, etc.) in user copy—be concise and action-oriented.

## What to change (adapter only)

1. **Menu UX copy**

   * Replace any prompt that explains backend behavior or asks “should I proceed?” with:

   ```
   Choose a mode (type 1–4):
   1) Card draw
   2) Journal prompt
   3) Zuihitsu
   4) Describe an idea / problem / situation
   ```

   (No extra explanations.)

2. **Direct dispatch**

   * When the user types `1|2|3|4`, **immediately** emit exactly one structured tool call to the kernel:

     ```
     {
       "tool.call": {
         "id": "glyph.invoke",
         "request_id": "<fresh-uuid-each-time>",
         "payload": { ... } // see mapping below
       }
     }
     ```
   * Generate a **new** `request_id` per call to satisfy router idempotency rules.

3. **Selection → payload mapping (use existing schema)**

   * Discover the actual payload schema in this codebase (search for `glyph.invoke`, `glyph_id`, or the tool index). Do **not** invent fields.
   * Map:

     * `1` → Card draw
     * `2` → Journal prompt
     * `3` → Zuihitsu
     * `4` → Describe an idea / problem / situation
   * If the repo defines deck names or glyph IDs, use those constants. Otherwise, infer from existing invoke sites/tests.

4. **Post-result footer**

   * After rendering a result, print one compact footer to encourage continued use:

     ```
     (1) Draw again  (2) Journal  (3) Zuihitsu  (4) Describe  (M) Menu
     ```
   * `1–4` trigger the same direct dispatch. `M` reprints the 1–4 menu.

5. **Error fallback**

   * If the kernel returns a namespace/tool/schema error, render:

     ```
     That didn’t work. Type M to open the menu.
     ```
   * Then await input. (Do not expose internals.)

## Don’ts

* ❌ Do not modify kernel files or invariants (entry gate, router, lenses, beacons).
* ❌ Do not add new menu items.
* ❌ Do not add confirmation prompts between selection and execution.
* ❌ Do not reuse `request_id` across different payloads.

## Implementation steps (have Codex follow exactly)

1. **Locate adapter menu code** (search terms: `MENU.OPEN`, “Choose a mode”, numbers `1)` through `4)`).
2. **Refactor the input handler** that currently branches on user selection to:

   * Parse `1–4`
   * Build the **existing** `glyph.invoke` payload struct for each option (pull field names and defaults from current code/tests)
   * Generate a fresh UUID (reuse the project’s UUID util)
   * Send the single `tool.call` envelope to the kernel transport
   * Render the returned artifact
3. **Replace confirmation copy** with the minimal menu and footer above.
4. **Add a tiny guard** to handle already-accepted sessions: if the kernel echoes “Agreement already active. Opening menu.”, still show the menu and proceed with direct dispatch.
5. **Keep logs quiet** (debug logs ok, but no backend narration in user-visible text).

## Acceptance criteria (must pass)

* Selecting `1` immediately produces a card artifact (no intermediate “explain & ask” message).
* Selecting `2–4` immediately produces the correct artifact type per current glyphs.
* Each `glyph.invoke` uses a fresh `request_id`.
* On invalid input at the menu, the adapter prints: `Type 1–4.` and re-prompts.
* On tool/schema error, the adapter prints the fallback line and awaits input.
* Kernel remains unchanged; tests/builds pass.

## Suggested tests (adjust to repo)

* **Unit**: selection handler maps `2` → payload with correct glyph id/fields.
* **Unit**: request\_id uniqueness across repeated selections.
* **Integration**: simulate `[KERNEL_ENTRY]` → menu → `1` → artifact rendered; assert no intermediate confirmation line.
* **Integration**: error path triggers fallback message then `M` reprints menu.

## Notes for Codex

* Respect the kernel’s “plain text is inert; only structured calls execute” rule; the adapter is responsible for translation.
* Keep wording concise to satisfy the “clarity over fluency” beacon.

**Deliverables**

* A minimal diff (patch) to the adapter implementing the above.
* If glyph IDs/fields were discovered, document them in the PR description.

---


Here’s a clean **Codex prompt** you could drop into the kernel canon to enforce what you want — Agreement-first discipline, every time, without interpretive leakage:

---

### 🔑 Codex Prompt — Entry Gate Discipline

**Context:**
Current `ENTRY_GATE` (kernel/10\_entry\_gate.md) already routes *all inbound messages* through the gate until `[KERNEL_ENTRY]` is received.
Problem: interpretive adapters can still “leak” meta-commentary or reflective text before entry, creating drift (acting like a normal chat instead of kernel).

**Instruction:**
Update `ENTRY_GATE` spec with the following invariant:

```
[ENTRY_DISCIPLINE]
- Until meta_locus.accepted == true:
  - The ONLY valid outbound emission is the Agreement Prompt.
  - No adapters, interpreters, or overlays may generate commentary,
    explanation, or alternative responses.
  - Any attempted emission outside the Agreement Prompt MUST be blocked,
    logged as beacon.check {id: entry_discipline_violation}, and
    surface: "Agreement not yet accepted. Only Agreement Prompt allowed."
- Once [KERNEL_ENTRY] is received and accepted:
  - Normal router dispatch resumes.
```

**Placement:**
Add under **Dispatch Rules → Purpose & Constraints** in `kernel/10_entry_gate.md`.

**Effect:**

* Adapters cannot “talk around” the kernel before entry.
* The very first move in any session is always the Agreement Prompt.
* This closes the gap between interpretive mode and kernel invariants.

---
