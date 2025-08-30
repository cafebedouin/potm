# Practitioner Menu — Adapter Contract

## Options (exact strings)
1) Card draw
2) Journal prompt
3) Zuihitsu
4) Describe an idea / problem / situation

## Mapping to Kernel Call
All options invoke `glyph.invoke` with a single payload:
- Card draw → `{ "type":"card_draw", "mode":"static_pack" | "dynamic_generated", "context"?:{}, "constraints"?:{} }`
- Journal prompt → `{ "type":"journal_prompt", ... }`
- Zuihitsu → `{ "type":"zuihitsu", ... }`
- Describe… → `{ "type":"describe_intake", ... }`

### Context & Constraints (optional)
- `context` is an adapter-supplied snapshot (session-local, no PII export).
- `constraints` can shape tone, word caps, intensity, or topic.

### Rendering
Adapters render the returned artifact text. When `artifact.source == "generated"`, adapters MAY render a minimal provenance ribbon derived from `provenance`, `why_this`, and `fit_confidence`.  
No internal tool names (lenses, micro-moves, beacons, modes) are surfaced.

