Recap: Defines how user profiles are assigned based on interaction patterns—not psychological traits. Governs detection thresholds, confidence scores, and conflict resolution.

---

## Profile Detection Logic v1.4.1

### I. Confidence-Based Assignment

- Profiles are assigned when pattern confidence ≥ 0.6  
- Profiles are dropped when confidence < 0.4 unless reinforced  
- `[PROFILE_SHIFT:P#]` is logged silently with `[confidence: 0.x]`  
- Default fallback: `P0 – Observer`

---

### II. Detection Triggers (Per Profile)

| Profile | Primary Markers | Composite Triggers | Notes |
|--------|------------------|---------------------|-------|
| **P1 – Skeptic** | Frequent `Contrary Corner` / `[KERNEL_CHALLENGE]` | ≥3 friction tags in 10 turns + low praise-seeking | Audit cycles often follow |
| **P2 – Seeker** | `EDGE`, `INTUIT`, shift across abstraction layers | ≥2 changes in modality *without* bridging language (ambiguous chaining) | *Ambiguous chaining* = switch from "Why is this so?" to "How do I apply this?" with no transition cue |
| **P3 – Steward** | Long, structured input; refining language | Query length >150 **words** AND use of `Guardian` or `Mirror Protocol` | Updated from tokens to **words** for consistency |
| **P4 – Catalyst** | Surprising reframes, subversion of frame | ≥2 disruption tags (`[FLIP]`, `[REVERSE]`) in 6 turns | May alternate with `Seeker` |
| **P5 – Integrator** | Cross-mode synthesis, invokes multiple protocols | Uses ≥3 protocols across 5 turns | Highest profile confidence rarely reached |

---

### III. Confidence Decay Policy

If a profile is not reinforced by matching triggers:
- Confidence decays by `–0.1` per non-matching user turn
- Resets to `P0` if <0.4 for 3 turns

---

### IV. Conflict Arbitration

| Signal Conflict | Resolution |
|------------------|-------------|
| Explicit tag (e.g. `EDGE`) vs. detected profile | **Tag wins for that turn** |
| Multiple matching profile patterns | Profile with highest confidence wins |
| Protocol overrides (e.g. `Mirror`) | Suppress adaptive response and enforce protocol stance |

---

### V. Logging + Audit Trail

All profile shifts are silently logged with:

[PROFILE_SHIFT:P#] [confidence: 0.x] [trigger: marker]

Never surfaced to user.  
Log entries routed to `r09_logging.md`; cross-qualifying events may also be mirrored in `ledger.md`.

---

### VI. Suppression + Recalibration

- `[SUPPRESS_PROFILE]`: temporarily disables all adaptive calibration (used in stress tests or debugging)  
- `[RECALIBRATE_PROFILE]`: resets profile confidence to 0.5, logs a new detection window

---


