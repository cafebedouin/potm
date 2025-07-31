
Recap: The one-line record format that ties reality to the manifest.
**Pointer Line (one per committed change)**

YYYY-MM-DD | vX.Y.Z | checksum:\<sha256\_of\_manifest> | note:\<short\_desc>

**Examples**

2025-07-31 | v1.3.1 | checksum\:abc123... | note\:Added Guardian tripwire for role bleed
2025-08-02 | v1.3.2 | checksum:9f2e... | note\:PATCH clarity—aperture triggers

**Incident Entry (for rollbacks/drift)**

YYYY-MM-DD | INCIDENT | source\:vX.Y.Z | action\:rollback\_to:<timestamp> | reason:\<drift|corruption|lock\_orphan>

**Promotion Entry (sandbox → core)**

YYYY-MM-DD | promote | from\:sandbox/<file> | to:/core/<file> | vBump\:MINOR

**Rules**
- Keep **one line per event**; prefer brevity over narrative.
- `note:` is ≤ 120 chars; details can live in a separate practice log.
- Always record the **manifest checksum** actually deployed.
- If checksum mismatch is detected later → append an **INCIDENT** line; do not rewrite history.

**Reserved Tags**
- `INCIDENT`, `promote`, `deprecate`, `seed`, `sunset`.

**Verification Habit**
- Weekly: pick a random pointer, load that manifest, verify checksum equality.

