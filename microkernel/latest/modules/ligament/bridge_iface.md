---
id: potm.proto.bridge.ligament.v1
title: bridge_iface
display_title: "Kernel↔Interface Ligament"
type: agent_protocol
status: draft
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: equivalent
  agent_protocol: ver1.4/potm_bootpack_combined.md
  practitioner_doc: modules/practices/practice_menu.md
  supersedes: []
  superseded_by: []
interfaces: [kernel_menu, deck_adapter, journal_adapter, ledger]
applicability: [P0, P1, P2, P3, P4]
intensity: gentle
preconditions: ["contract.accepted == true"]
outputs: [bridge_event, deck_call, adapter_result]
cadence: ["on_menu_invoked", "on_help_like_query", "on_idle_start"]
entry_cues: ["menu", "help", "what can you do?", "draw", "card", "prompt"]
safety_notes:
  - "No mode leakage: kernel constraints remain active; adapters cannot relax them."
  - "No hidden dependencies: ligament contains no business logic for decks."
tags: [bridge, interface, kernel, deck, forge_origin:PoTM, spiral_eval:2025-08-11]
author: "practitioner"
license: CC0-1.0
---

# Purpose
Define the handshake + return contract so the kernel can invoke any engagement surface (deck, journal, checklist) without knowing internals.

## State Envelope
state_envelope:
  context_id: "<uuid>"
  profile: "P0|P1|P2|P3|P4"
  mode: "kernel"
  locale: "en-US"
  safety_flags: {high_stakes: false, hazard: false}
  seed: "<uint32>"
  last_action: "<bridge_event or null>"
  trace: []  # list of (timestamp, event, note)

## Events
events:
  - MENU.OPEN
  - INTERFACE.DISCOVER      # NEW: query an adapter's capabilities
  - INTERFACE.REQUEST
  - INTERFACE.RETURN
  - LOOP.NEXT

## Surface Registry (baseline; discovery may override at runtime)
surface_registry:
  - name: "deck"
    cap_version: "1.0"
    capabilities: ["draw_1", "draw_5", "show_detail", "reflect"]
  - name: "journal"
    cap_version: "1.0"
    capabilities: ["seed_prompt", "collect_entry"]
  - name: "checklist"
    cap_version: "1.0"
    capabilities: ["select", "walkthrough"]

## Return Contract
adapter_return:
  ok: true|false
  surface: "deck|journal|checklist"
  action: "present|options|reflection|error"
  payload: {}                           # surface-specific, never kernel logic
  hints: {suggest_next: "LOOP.NEXT|MENU.OPEN|done"}
  errors?: [{code, message}]

## Error Set
errors:
  - code: E_MODE_LEAK      # adapter tried to change kernel mode/flags
  - code: E_CONTRACT       # missing/invalid fields in adapter_return
  - code: E_CAPABILITY     # surface doesn’t support requested capability
  - code: E_SAFETY         # high-stakes or hazard tripped

## Kernel-side Bridge Logic
bridge_logic:
  on MENU.OPEN:
    render(practice_menu_minimal)

  on INTERFACE.DISCOVER(surface):
    route -> adapter.<surface>.discover(state_envelope)

  on INTERFACE.REQUEST(surface, capability, args?):
    route -> adapter.<surface>.<capability>(state_envelope, args)

  on INTERFACE.RETURN(adapter_return):
    if adapter_return.ok == false:
      handle_error(adapter_return.errors)
    update(state_envelope.trace, adapter_return)
    switch adapter_return.hints.suggest_next:
      case "LOOP.NEXT": offer_next_step()
      case "MENU.OPEN": emit MENU.OPEN
      case "done":      finalize_and_exit()

  on LOOP.NEXT:
    offer_next_step()

## Offer-Next-Step UI
- Talk about something specific
- Draw five new options
- Zoom in on this card
- Reflect & save a note
- Back to menu
