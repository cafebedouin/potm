---
id: potm.kernel.lenses.v1_6_dev
title: "30_lenses"
display_title: "Lenses — Contracted Views"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines the family of kernel lenses — read-only tools that provide contracted,
  deterministic perspectives on session state and arguments. All lenses are
  session-local, schema-bound, and fail-closed on invalid payloads.
author: practitioner
license: CC0-1.0
---

# Lenses — Contracted Views

## Purpose

Lenses are **read-only tools** that let practitioners view kernel state or
claims through specific structured perspectives. They are deterministic,
session-local, and never mutate state.  

They enable **auditability and practice discipline** by forcing reasoning
through fixed apertures (edge, contrary, open questions, etc.) instead of
informal freeform dialogue.

---

## Invocation

Each lens is called via:

```yaml
tool.call:
  id: "lens.<id>"
  payload: { … }
````

* Payloads must validate against the corresponding schema.
* Invalid payloads emit `E_PAYLOAD`.
* Unknown lens ids emit `E_NAMESPACE`.

For invoking multiple lenses together, use `lens.meta`.

---

## Lens Families

Each lens has its own schema and example.

### 1. EDGE

* Surfaces contradictions, edge cases, and hidden premises.
* Schema: `runtime/schema/lens_edge.json`
* Example: `runtime/examples/lens_edge_invoke.json`

---

### 2. DEFINE

* Provides contextual definition of terms.
* Schema: `runtime/schema/lens_define.json`
* Example: `runtime/examples/lens_define_invoke.json`

---

### 3. SELF-AUDIT

* Runs structured self-audit across session or kernel scope.
* Schema: `runtime/schema/lens_self_audit.json`
* Example: `runtime/examples/lens_self_audit_invoke.json`

---

### 4. OPEN QUESTIONS

* Surfaces open questions relevant to a topic or fracture.
* Schema: `runtime/schema/lens_open_questions.json`
* Example: `runtime/examples/lens_open_questions_invoke.json`

---

### 5. FACTS

* Surfaces agreed-upon or known facts.
* Schema: `runtime/schema/lens_facts.json`
* Examples:

  * `runtime/examples/lens_facts_invoke.json`
  * `runtime/examples/lens_facts_result.json`

---

### 6. CHECK

* Validates assumptions or premises.
* Schema: `runtime/schema/lens_check.json`
* Examples:

  * `runtime/examples/lens_check_invoke.json`
  * `runtime/examples/lens_check_result.json`

---

### 7. TRACE

* Follows reasoning chains step by step.
* Schema: `runtime/schema/lens_trace.json`
* Examples:

  * `runtime/examples/lens_trace_invoke.json`
  * `runtime/examples/lens_trace_result.json`

---

### 8. BOUNDARY

* Identifies scope, limits, and thresholds.
* Schema: `runtime/schema/lens_boundary.json`
* Examples:

  * `runtime/examples/lens_boundary_invoke.json`
  * `runtime/examples/lens_boundary_result.json`

---

### 9. CONTRARY

* Generates contrary or inverted statements.
* Schema: `runtime/schema/lens_contrary.json`
* Examples:

  * `runtime/examples/lens_contrary_invoke.json`
  * `runtime/examples/lens_contrary_result.json`

---

### 10. FORGE

* Crafts new synthesis from fragments or materials.
* Schema: `runtime/schema/lens_forge.json`
* Examples:

  * `runtime/examples/lens_forge_invoke.json`
  * `runtime/examples/lens_forge_result.json`

---

### 11. SYNTH

* Combines multiple insights into a unified output.
* Schema: `runtime/schema/lens_synth.json`
* Examples:

  * `runtime/examples/lens_synth_invoke.json`
  * `runtime/examples/lens_synth_result.json`

---

### 12. SPIRAL

* Maps growth or drift across iterations.
* Schema: `runtime/schema/lens_spiral.json`
* Examples:

  * `runtime/examples/lens_spiral_invoke.json`
  * `runtime/examples/lens_spiral_result.json`

---

### 13. ARCHIVE

* Summarizes or closes a thread.
* Schema: `runtime/schema/lens_archive.json`
* Examples:

  * `runtime/examples/lens_archive_invoke.json`
  * `runtime/examples/lens_archive_result.json`

---

### 14. WAIT

* Holds context in suspension without closure.
* Schema: `runtime/schema/lens_wait.json`
* Examples:

  * `runtime/examples/lens_wait_invoke.json`
  * `runtime/examples/lens_wait_result.json`

---

### 15. REFUSE

* Declines engagement when unsafe or inappropriate.
* Schema: `runtime/schema/lens_refuse.json`
* Examples:

  * `runtime/examples/lens_refuse_invoke.json`
  * `runtime/examples/lens_refuse_result.json`

---

### 16. RELATION\_ZONE

* Detects and reports shifts between relational zones (green, yellow, red).
* Schema: `runtime/schema/lens_relation_zone.json`
* Example: `runtime/examples/lens_relation_zone_log.json`

---

### 17. META-CONFLICT

* Analyzes patterns across multiple conflicts.
* Schema: `runtime/schema/lens_meta_conflict.json`
* Examples:

  * `runtime/examples/lens_meta_conflict_invoke.json`
  * `runtime/examples/lens_meta_conflict_result.json`

---

### 18. META (bundle lens)

* Invokes multiple lenses in one call.
* Schema: `runtime/schema/lens_meta.json`
* Examples:

  * Valid chain: `runtime/examples/lens_meta_invoke_valid.json`
  * Antipattern: `runtime/examples/lens_meta_invoke_antipattern.json`

---

## Anti-patterns (What not to do)

The following combinations are discouraged and may trigger
`tool.error { code: "E_ANTIPATTERN" }` when `policy_mode=strict` in `lens.meta`:

* EDGE before DEFINE on vague terms → sharpens noise, not clarity.
* TRACE without CHECK on shaky assumptions → builds on sand.
* OPENQ in toxic zone → use REFUSE instead.
* Chaining lenses without ALIGN\_SCAN → lose sight of shared aim.
* DEFLECT & DEFEND against criticism → ego protection, not truth-seeking.
* FLATTERY in any context → substitutes ego-stroking for substance.
* SPIRAL on every micro-iteration → burns cycles on noise; use only on sustained growth or drift.
* ARCHIVE on live tensions → prematurely closes unresolved fractures.

See: `runtime/examples/lens_meta_invoke_antipattern.json`

---

## Common Scenarios (Toolchains)

Certain lens bundles are especially effective when sequenced:

* DEFINE → EDGE → OPENQ (clarify term, stress-test, surface unknowns)
* FACTS → CHECK → TRACE (ground, validate, extend chain)
* CONTRARY → SYNTH → FORGE (flip, integrate, craft)
* RELATION\_ZONE → REFUSE → WAIT (safety-first)

See: `runtime/examples/lens_meta_invoke_valid.json`

---

## Failure Modes

| Condition                       | Emission code   |
| ------------------------------- | --------------- |
| Invalid payload                 | `E_PAYLOAD`     |
| Unknown lens id                 | `E_NAMESPACE`   |
| Attempt to mutate state         | `E_INVARIANT`   |
| Antipattern chain (strict mode) | `E_ANTIPATTERN` |

---

## References

* Recap validator: `60_recap_validator.md`
* State locus: `70_state.md`
* Escalation gates: `68_escalation_gates.md`
* Mode profiles: `65_mode_profiles.md`
* Closure tools: `80_closure.md`

---

## Versioning & Change Log

* **1.6.0-dev** — Clean rewrite:

  * Removed inline YAML/JSON.
  * Added runtime schemas and examples for all 18 lenses.
  * Introduced `lens.meta` contract for bundles.
  * Anti-patterns and toolchains externalized as runtime examples.

---
