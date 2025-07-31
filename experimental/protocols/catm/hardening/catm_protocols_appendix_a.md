{
  "properties": {
    "survivorship": { "enum": ["survived_0x", "survived_1x", "survived_2x", "survived_3x_plus"] },
    "guardian_hook": { "enum": ["required", "optional", "none"] },
    "guardian_state": { "enum": ["none", "observed", "elevated", "quarantined"] },
    "review_basis": { "enum": ["timebox", "incident", "evidence_threshold"] },
    "next_review_date": { "type": ["string", "null"], "format": "date" },
    "sunset_policy": { "type": "string" },
    "sunset_trigger": { "type": "array", "items": { "type": "string" } },
    "handoff_notes": { "type": "string" },
    "meta_digest": { "type": "string", "maxLength": 280 },
    "last_benefit_date": { "type": ["string", "null"], "format": "date" },
    "benefit_count_30d": { "type": "integer", "minimum": 0 }
  },
  "required": [
    "survivorship",
    "guardian_hook",
    "guardian_state",
    "review_basis",
    "benefit_count_30d",
    "last_benefit_date"
  ]
}
