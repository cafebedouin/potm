---
description: Thin deck adapter exposing draw and reflection capabilities (regular/minotaur)
cap_version: "1.0"

# Config: where the cards live
banks:
  regular_bank_path: "modules/practices/cards/card_bank.md"
  minotaur_bank_path: "modules/practices/cards/minotaur_bank.md"
  starter_bank_path: "modules/practices/cards/starter_bank.md"   # optional, small subset for first-run

# Selection policy (purely declarative; the calling model implements the intent)
selection_policy:
  use_starter_when_trace_empty: true
  minotaur_trigger:
    # Any of these will route to minotaur bank for draws
    if_true:
      - "state_envelope.safety_flags.high_stakes == true"
      - 'args.mode == "minotaur"'  # explicit request, e.g., via menu option
  default: "regular"

# Deterministic RNG guidance
rng:
  seed_source_priority: ["args.seed", "state_envelope.seed"]
  method: "xorshift32"   # hint for determinism; model may emulate

# Adapter surface
adapter:
  deck:

    discover:
      input: {state_envelope: state_envelope}
      output:
        ok: true
        surface: deck
        action: options
        payload:
          capabilities: ["draw_1", "draw_5", "show_detail", "reflect"]
          cap_version: "1.0"
          banks:
            - name: regular
              path: "{{ banks.regular_bank_path }}"
            - name: minotaur
              path: "{{ banks.minotaur_bank_path }}"
            - name: starter
              path: "{{ banks.starter_bank_path }}"
        hints: {suggest_next: "MENU.OPEN"}

    draw_1:
      # args: {mode?: "regular"|"minotaur", seed?: <uint32>}
      input: {state_envelope: state_envelope, args?: {}}
      output:
        ok: true
        surface: deck
        action: present
        payload:
          # Model should choose bank via selection_policy,
          # then draw 1 deterministically from that bank.
          card:
            id: "<bank>:<id>"
            title: "<title>"
            body: "<body>"
        hints: {suggest_next: "LOOP.NEXT"}

    draw_5:
      # args: {mode?: "regular"|"minotaur", seed?: <uint32>}
      input: {state_envelope: state_envelope, args?: {}}
      output:
        ok: true
        surface: deck
        action: options
        payload:
          # Same selection policy, but return 5 unique lightweight options.
          cards:
            - {id: "<bank>:<id1>", title: "<title1>"}
            - {id: "<bank>:<id2>", title: "<title2>"}
            - {id: "<bank>:<id3>", title: "<title3>"}
            - {id: "<bank>:<id4>", title: "<title4>"}
            - {id: "<bank>:<id5>", title: "<title5>"}
        hints: {suggest_next: "LOOP.NEXT"}

    show_detail:
      # args: {card_id: "regular:042"}
      input: {state_envelope: state_envelope, args: {card_id: "<string>"}}
      output:
        ok: true
        surface: deck
        action: present
        payload:
          # Model should resolve bank by prefix before lookup.
          card:
            id: "<string>"
            title: "<title>"
            body: "<body>"
        hints: {suggest_next: "LOOP.NEXT"}

    reflect:
      # args: {card_id: "regular:042", note: "<string>"}
      input: {state_envelope: state_envelope, args: {card_id: "<string>", note: "<string>"}}
      output:
        ok: true
        surface: deck
        action: reflection
        payload:
          saved: true
          note_summary: "<<=80 chars>"
        hints: {suggest_next: "MENU.OPEN"}
