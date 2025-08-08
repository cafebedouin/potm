---
title: "Modules Scope"
version: "v1.0"
status: "reference"
type: "meta"
last_updated: "2025-07-30"
---
### What is a module?
- An optional **overlay** or **adapter** that extends protocols or practices.
- Not always-on (that's a subsystem). Not a container with steps (that's a protocol).

### Decision tests
- Needs a host (protocol/practice) to make sense? → Module.
- Requires entry/timebox/exit? → Protocol.
- Runs continuously or orchestrates others? → Subsystem.

### Required front-matter fields
- `plugs_into:` list of host artifacts
- `capabilities:` what it adds (diagnostic, deepening, creative disruption, etc.)
- `constraints:` safety/fit limits
- `outputs:` what artifacts/data it produces (notes, flags, decisions)
