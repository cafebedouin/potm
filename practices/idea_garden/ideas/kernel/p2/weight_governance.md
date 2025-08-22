selector_policy:
  weight_profiles:
    balanced:
      uncertainty: 0.35
      risk: 0.25
      novelty: 0.20
      redundancy: -0.20
      match_trigger: 0.20
      cognitive_cost: -0.10
    exploratory:
      uncertainty: 0.25
      risk: 0.15
      novelty: 0.40
      redundancy: -0.15
      match_trigger: 0.20
      cognitive_cost: -0.05
    conservative:
      uncertainty: 0.40
      risk: 0.35
      novelty: 0.10
      redundancy: -0.25
      match_trigger: 0.15
      cognitive_cost: -0.20
  active_profile: balanced
  governance:
    change_rules:
      - "User may switch profile via [META] weight_profile:<name>"
      - "Model may propose profile switch if misalignment persists 3+ turns (soft confirm)."
