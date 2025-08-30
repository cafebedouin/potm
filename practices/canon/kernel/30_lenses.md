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
  Catalog of 18 read-only, schema-bound lenses. Each lens emits a deterministic
  artifact from session state or input. Invalid calls fail-closed.
author: practitioner
license: CC0-1.0
---

# Lenses — Contracted Views

## Invocation

See router envelope: `runtime/spec/router_envelope.json` (payload must satisfy each lens schema).

Invalid payload → `tool.error { code: "E_PAYLOAD" }`  
Unknown id → `tool.error { code: "E_NAMESPACE" }`

---

## Lens Catalog

| id               | Purpose                                | Schema                             | Example                                 |
|------------------|----------------------------------------|------------------------------------|-----------------------------------------|
| edge             | Surface edge cases & contradictions    | `schema/lens_edge.json`            | `examples/lens_edge_invoke.json`        |
| define           | Disambiguate key terms                 | `schema/lens_define.json`          | `examples/lens_define_invoke.json`      |
| self_audit       | Structured self-audit                  | `schema/lens_self_audit.json`      | `examples/lens_self_audit_invoke.json`  |
| open_questions   | Surface open questions                 | `schema/lens_open_questions.json`  | `examples/lens_open_questions_invoke.json` |
| facts            | Gather known facts                     | `schema/lens_facts.json`           | `examples/lens_facts_invoke.json`       |
| check            | Test a key assumption                  | `schema/lens_check.json`           | `examples/lens_check_invoke.json`       |
| trace            | Follow reasoning chain                 | `schema/lens_trace.json`           | `examples/lens_trace_invoke.json`       |
| boundary         | Identify scope & limits                | `schema/lens_boundary.json`        | `examples/lens_boundary_invoke.json`    |
| contrary         | Generate opposing view                 | `schema/lens_contrary.json`        | `examples/lens_contrary_invoke.json`    |
| forge            | Craft minimal prototype plan           | `schema/lens_forge.json`           | `examples/lens_forge_invoke.json`       |
| synth            | Synthesize discussion into action      | `schema/lens_synth.json`           | `examples/lens_synth_invoke.json`       |
| spiral           | Map drift/evolution over time          | `schema/lens_spiral.json`          | `examples/lens_spiral_invoke.json`      |
| archive          | Summarize or close a thread            | `schema/lens_archive.json`         | `examples/lens_archive_invoke.json`     |
| wait             | Hold context in suspension             | `schema/lens_wait.json`            | `examples/lens_wait_invoke.json`        |
| refuse           | Decline unsafe requests                | `schema/lens_refuse.json`          | `examples/lens_refuse_invoke.json`      |
| relation_zone    | Detect relational zone shifts          | `schema/lens_relation_zone.json`   | `examples/lens_relation_zone_log.json`  |
| meta_conflict    | Analyze cross-conflict patterns        | `schema/lens_meta_conflict.json`   | `examples/lens_meta_conflict_invoke.json` |
| meta             | Bundle multiple lenses                 | `schema/lens_meta.json`            | `examples/lens_meta_invoke_valid.json`  |
| fracture_status  | Show fracture queue state              | `runtime/spec/lens.fracture_status.json` | `runtime/examples/lens_fracture_status.json` |
| externalist      | Diagnostic overlay (modes)             | `runtime/spec/externalist.invoke_payload.json` | `runtime/examples/externalist_invoke.json` |

---

## Anti-Patterns

Strict `lens.meta` rejects these sequences with `E_ANTIPATTERN`:

- `edge` before `define`  
- `trace` without `check`  
- `open_questions` in toxic zones (use `refuse`)  
- Chaining without `align_scan`  
- Repeated self-audit loops  
- `spiral` on every micromove  
- `archive` on live tensions  

---

## Common Toolchains

- Clarify → Test → Question:  
  `define` → `edge` → `open_questions`  
- Ground → Validate → Extend:  
  `facts` → `check` → `trace`  
- Flip → Synthesize → Act:  
  `contrary` → `synth` → `forge`

---

## Failure Modes

| Condition                       | Emission code   |
|---------------------------------|-----------------|
| Invalid payload                 | `E_PAYLOAD`     |
| Unknown lens id                 | `E_NAMESPACE`   |
| Attempt to mutate state         | `E_INVARIANT`   |
| Anti-pattern chain              | `E_ANTIPATTERN` |

---

## References
n - bs_detect (practitioner): `extended/diagnostics/bs_detect.md`  n - sentinel_spotcheck (practitioner): `extended/diagnostics/sentinel_spotcheck.md`  
- Recap validator: `60_recap_validator.md`  
- Session state: `70_state.md`  
- Closure tools: `80_closure.md`  
- Policy & caps: `90_policy.md`
 - Externalist guidance (practitioner): `kernel/lenses/externalist_diagnostic_modes.md`
 - mirror_protocol (practitioner): `kernel/protocols/mirror_protocol.md`  
 - suspicion_first_protocol (practitioner): `kernel/protocols/suspicion_first_protocol.md`  
 - ai_integrity_protocol (practitioner): `kernel/protocols/ai_integrity_protocol.md`  
 - bs_detect (practitioner): `extended/diagnostics/bs_detect.md`  
 - sentinel_spotcheck (practitioner): `extended/diagnostics/sentinel_spotcheck.md`  
