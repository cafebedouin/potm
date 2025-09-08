ledger_events:
  - type: lens_invoked
    fields: [lens_id, reason, weight_profile, timestamp]
  - type: chain_run
    fields: [chain, initiator: user|route|system, confirm_mode, timestamp]
  - type: swerve_suggested
    fields: [reason, accepted: true|false, followup_lens, timestamp]
  - type: outcome_marker    # closure signals
    fields: [move_made: true|false, decision: text?, metric?, review_date?]
  - type: feedback
    fields: [useful: up|down, note]
