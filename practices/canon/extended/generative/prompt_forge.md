# Prompt Forge — Dynamic Generation Rules

Use `mode:"dynamic_generated"` only when:
1) Pack coverage is low or mismatched to `context`, or
2) `constraints` specify a shape not found in packs.

Required fields when `artifact.source == "generated"`:
- `provenance.inputs`: optional list of pack titles or descriptors consulted.
- `why_this`: one sentence on fit (<= 24 words).
- `fit_confidence`: [0.0–1.0] plus at least one observable proxy in `signals` (e.g., keyword match count).

Beacons remain active: avoid oracle tone; mark uncertainty; respect practitioner safety.

