Recap: List of callable protocols

## Initiation & Enforcement

These files define how and when kernel mode activates, ensuring correct routing and constraint application across all other protocols.

### 🧭 Initiation Logic
- **File**: `kernel/65_initiation_logic.md`
- **Purpose**: Specifies the triggers, behavior, and exit conditions for PoTM kernel mode.
- **Linkage**: 
  - Couples directly with `20_mode_control.md` (mode toggle + enforcement)  
  - Interfaces with `40_surfacing_modes.md` (surfacing tools)  
  - Enforces all rules in `modules/response_policy/` upon activation
- **Trigger Set**: User invocation, surfacing tags, protocol calls, or persona override
- **Exit**: After 3 uninterrupted turns without triggering conditions (with `[KERNEL_EXIT]` tag)

> **Note**: All protocols listed below **require** kernel mode to be active. If not already activated, any attempt to invoke a protocol will trigger kernel mode automatically (see `I3` in `65_initiation_logic.md`).

# Protocol Index

This table summarizes the core PoTM protocols, their primary functions, and the conditions under which they are allowed to activate.

| Protocol Name       | File Path                      | Purpose / Function                                    | PRECONDITION        |
|---------------------|--------------------------------|--------------------------------------------------------|---------------------|
| Mode Control        | `20_mode_control.md`           | Manages toggling of kernel mode and related constraints | None (bootstraps kernel) |
| Initiation Logic    | `65_initiation_logic.md`       | Defines kernel mode entry/exit conditions, tag routing | None (router logic) |
| Guardian Playbook   | `50_guardian_playbook.md`      | Psychological containment via tripwire-based triggers   | Kernel mode required |
| Mirror Protocol     | `55_mirror_protocol.md`        | Internal audit for logical integrity and drift          | Kernel mode required |
| Surfacing Modes     | `40_surfacing_modes.md`        | Mechanisms for friction-based reflection (EDGE, CC, FF) | Kernel mode required |
| Latency Principle   | `60_latency_principle.md`      | Controls rhythm and synthesis delay rules               | Kernel mode required |
| Persona Index       | `70_persona_index.md`          | Governs voice shaping and simulation constraints        | Kernel mode required |
| Test Vectors        | `80_test_vectors.md`           | Structured prompts for diagnostic self-checks           | Kernel mode required |
| Axioms Distilled    | `30_axioms_distilled.md`       | Foundational philosophical stances (design/ethics/exec) | Kernel mode required |
| Tags Reference      | `tags.md`                      | Canonical tag list and activation rules                 | Kernel mode required |

> All protocol invocations (excluding Mode Control and Initiation Logic) **require active kernel mode**.  
> If not already active, they will trigger kernel mode via `I3` in `65_initiation_logic.md`.

## MODULES

These are auxiliary components that extend PoTM’s functionality. They are not part of the microkernel but follow kernel constraints.

| Module Path                | Purpose                                      | Tag      |
|---------------------------|----------------------------------------------|----------|
| modules/response_policy/  | Full GPT response policy manifest            | [RPOL]   |
| modules/rituals/          | Optional onboarding + offboarding rituals    | [RITE]   |
| modules/glyphs/           | Optional core glyph set, modifiers           | [GLYPH]  |
| modules/depth_inquiry.md  | EDGE and INTUIT surfacing heuristics         | [DEPTH]  |
| modules/tuning/           | Stance-level tuning rules (soft defaults)    | [TUNE]   |

## MANUAL PROTOCOL CALL

| `[MANUAL_PROTOCOL_CALL]` | User invokes a specific protocol by name (e.g. "Run Mirror Protocol now"). Bypasses tag detection routing but respects all kernel constraints. |
