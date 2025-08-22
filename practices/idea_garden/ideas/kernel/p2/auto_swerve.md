selector_policy:
  # ...existing...
  auto_swerve:
    enabled: true
    triggers:
      stagnation_turns: 3            # no net progress markers (e.g., no plan/decision delta)
      novelty_drop_threshold: 0.25   # semantic novelty vs last 3 turns
      contradiction_flag: true       # detected internal conflict or unverified core assumption
    action:
      suggest: "SWERVE"
      prompt: "Suggest orthogonal move to escape local optimum."
    confirm: "soft"   # soft = announce + proceed unless user objects; 'hard' = ask first

- id: SWERVE
  # ...existing...
  outputs:
    - "name the jump (which lens & why)"
    - "1 line on what new info it could reveal"
    - "auto_suggested: true|false"

