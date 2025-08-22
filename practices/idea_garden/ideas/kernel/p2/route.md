- id: ROUTE
  gist: "pick a chain"
  intent: "Select and (optionally) execute a short chain of lenses based on goal, time, and difficulty."
  outputs:
    - "proposed_chain: [L1, L2, L3]"
    - "rationale in 1 line"
    - "run_first_step_output"
  params:
    confirm: "soft"   # inherits runtime_flags.confirm_routes
    max_len: 3
