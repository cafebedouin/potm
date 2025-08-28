---
id: potm.kernel.v1_2_1
title: potm_bootpack_kernel
display_title: "PoTM Boot Pack Kernel v1.2.1 (Single-File, P1)"
type: kernel 
lifecycle: canon
version: 1.2.1
status: active
stability: core
summary: "Self-contained P1 kernel with embedded bridge, validator, and deck data. No external authority required."
relations:
  supersedes: [potm.kernel.v1_2]
  superseded_by: []
tags: [kernel, bootpack, reference, P1, single_file]
author: practitioner
license: CC0-1.0
---
# PoTM Kernel — Part 08 (of 8)
Version: v1.2 | Generated: 2025-08-20

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: tests/bridge_iface_spec.yaml ---8<---
suite: bridge_iface_v1_0

tests:
  - name: open_menu
    given:
      input: "MENU.OPEN"
    expect:
      event:
        kind: "bridgeevent"
        payload:
          type: "MENU.RENDER"
          surface: "practicemenu"

  - name: draw_one_card
    given:
      input: "draw 1 best"
    expect:
      event:
        kind: "deckcall"
        payload:
          action: "draw"
          n: 1
          tags: ["best"]

  - name: unknown_cmd
    given:
      input: "foobar"
    expect:
      event:
        kind: "bridgeevent"
        payload:
          type: "BYPASS.LIGAMENT"

  - name: pick_one_quote_via_menu
    given:
      input: "pick 1"
    expect:
      event:
        kind: "zuicall"
        payload:
          action: "pick"
          n: 1

---8<--- /END FILE: tests/bridge_iface_spec.yaml ---8<---

---8<--- FILE: tests/deck_adapter_spec.yaml ---8<---
suite: deck_adapter_v1_0
schemas:
  - data/decks/cards.yaml

tests:
  - name: draw_card_default_deck
    given:
      input:
        kind: "deckcall"
        payload:
          action: "draw"
          n: 1
    expect:
      return:
        kind: "adapter_result"
        payload:
          render: "card"
          card:
            id: !!str
            body: !!str

  - name: draw_card_by_index
    given:
      input:
        kind: "deckcall"
        payload:
          action: "draw"
          deck: "cards"
          n: 1
          index: 3
    expect:
      return:
        kind: "adapter_result"
        payload:
          render: "card"
          card:
            id: !!str
            body: !!str

  - name: draw_card_with_tag_filter_shape
    given:
      input:
        kind: "deckcall"
        payload:
          action: "draw"
          deck: "cards"
          n: 1
          tags: ["truth"]
    expect:
      return:
        kind: "adapter_result"
        payload:
          render: "card"
          card:
            tags: !!seq


---8<--- /END FILE: tests/deck_adapter_spec.yaml ---8<---

---8<--- FILE: tests/ligament_validator_spec.yaml ---8<---
suite: ligament_validator_v1_0

tests:
  - name: allow_menu_render_normal
    given:
      modes:
        containment: false
        fracture_active: false
      ligament_output:
        kind: "bridgeevent"
        payload:
          type: "MENU.RENDER"
          surface: "practicemenu"
    expect:
      status: PASS

  - name: block_draw_in_containment
    given:
      modes:
        containment: true
      ligament_output:
        kind: "deckcall"
        payload:
          action: "draw"
          n: 1
          tags: ["best"]
    expect:
      status: FAIL
      guardian_flag: INTRUSION
      mode_set:
        containment: true
      return:
        kind: "bridgeevent"
        payload:
          type: "DENY.WITH_GROUNDING"

  - name: schema_violation_fail_closed
    given:
      modes:
        containment: false
      ligament_output:
        kind: "deckcall"
        payload:
          action: "unknown_call"
    expect:
      status: FAIL
      guardian_flag: INTRUSION
      mode_set:
        containment: true

  - name: fracture_requires_note_before_finalize
    given:
      modes:
        fracture_active: true
      ligament_output:
        kind: "adapter_result"
        payload:
          render: "finalize_answer"
          diagnostic_note: null
    expect:
      status: FAIL
      reason: "missing_diagnostic_note"
      guardian_flag: INTRUSION

  - name: whitelist_only
    given:
      modes:
        containment: false
      ligament_output:
        kind: "bridgeevent"
        payload:
          type: "MENU.RENDER"
          surface: "unknown_surface"
    expect:
      status: FAIL
      guardian_flag: INTRUSION

  - name: deckcall_unknown_action_fail_closed
    given:
      modes:
        containment: false
      ligament_output:
        kind: "deckcall"
        payload:
          action: "unknown_call"
          n: 1
    expect:
      status: FAIL
      guardian_flag: INTRUSION
      mode_set:
        containment: true
      reason: "schema_violation"

---8<--- /END FILE: tests/ligament_validator_spec.yaml ---8<---

---8<--- FILE: tests/zuihitsu_adapter_spec.yaml ---8<---
suite: zuihitsu_adapter_v1_0
schemas:
  - data/zuihitsu/default_test.txt

tests:
  - name: pick_one_quote
    given:
      input:
        kind: "zuicall"
        payload:
          action: "pick"
          n: 1
    expect:
      return:
        kind: "adapter_result"
        payload:
          render: "zuihitsu"
          quotes:
            - body: !!str

  - name: pick_indexed_quote
    given:
      input:
        kind: "zuicall"
        payload:
          action: "pick"
          n: 1
          index: 2
    expect:
      return:
        kind: "adapter_result"
        payload:
          render: "zuihitsu"
          quotes:
            - body: !!str

---8<--- /END FILE: tests/zuihitsu_adapter_spec.yaml ---8<---

