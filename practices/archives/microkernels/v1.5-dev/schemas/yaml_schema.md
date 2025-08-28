---
id: potm.<type>.<family>.<name>.v1       # e.g. potm.strategy.guardian.core.v1
title: <filename_base>                   # kebab or snake; matches file name
display_title: "Human-facing title"      # optional
type: principle | doctrine | strategy | tactic | agent_protocol | kernel | suite
subtype: protocol | diagnostic | stress_test | playbook | safeguard   # only if type: tactic
lifecycle: canon | idea_garden | archive | meta
version: 1.0
status: draft | active | deprecated
stability: core | experimental

summary: >-
  One-sentence gist that a practitioner can act on.

relations:
  supersedes: []
  superseded_by: []

tags: [forge_origin:<context>, spiral_eval:<context>]

author: practitioner
license: CC0-1.0

# ——— agent_protocol-only fields ———

interfaces: [string]         # e.g. [kernel_menu, deck_adapter]

preconditions: [string]      # e.g. ["agreement.accepted == true"]

outputs: [string]            # e.g. [bridge_event, deck_call, zui_call, adapter_result]

cadence: [string]            # e.g. ["on_menu_invoked", "on_idle_start"]

entry_cues: [string]         # e.g. ["menu", "draw", "prompt"]


---

## Suite-type guidance

When `type: suite`, you may include these extra fields:

- relations:
    related: [<id>, …]

- tags:
    [<string>…]  
    (e.g. suite, harness, test_suite, cross_model, integrity, verification, ledger)
