---
title: "Forking Guidelines for Protocol Development"
version: 1.0
status: stable
type: guidelines
last_updated: 2025-07-28
authors:
  - cafebedouin
  - ChatGPT
related:
  - depth_inquiry_v1.4.1
  - depth_inquiry_v1.5-dev
  - human_conflict_protocol_v1.0
  - disorientation_drills
  - epistemic_integrity_checklist
location_suggestion: guidelines/forking_guidelines.md
---
# Forking Guidelines for Protocol Development

This document provides a general-purpose structure for forking *Pilates of the Mind* protocols when single-branch versions cannot serve the full range of user needs—from first-time practitioners to advanced facilitators.

It is based on successful bifurcation cases like the **Depth Inquiry Principle** and is intended to guide future forks to maintain clarity, coherence, and mutual intelligibility.

---

## 🪚 When to Fork a Protocol

Fork when:

- You observe **increased divergence** between beginner and advanced usage.
- Attempts to serve both audiences in one document create **bloat or confusion**.
- User feedback indicates that **different facilitation styles** or levels of abstraction are needed.
- There's a need to **field test** something without compromising depth documentation.

---

## 🍴 Fork Pattern Template

| Branch Name      | Use Case                               | Location Template                                      |
|------------------|-----------------------------------------|--------------------------------------------------------|
| `vX.Y`           | 🪴 *Practitioner Field Use*             | `core/{domain}/{protocol_name}_vX.Y.md`                |
| `vX.Y-dev`       | 🧠 *Trainer / Facilitator Expansion*    | `core/{domain}/{protocol_name}_vX.Y-dev.md`            |

- The `stable` version is for clarity, speed, and low-friction application.
- The `dev` version supports scaffolding, lineage awareness, and adaptation.

---

## 🧭 Navigation Cues for Users

| User Goal                         | Recommended Branch               |
|----------------------------------|----------------------------------|
| Immediate application             | `vX.Y` (field version)           |
| Learning to teach or adapt        | `vX.Y-dev` (pedagogical fork)    |
| Comparative evaluation            | Start with `vX.Y`, review `dev`  |

Each branch should include:
- A “fork map” reference to its counterpart.
- Clear purpose and audience labeling.
- Optional shared meta-README (recommended for major principles).

---

## 🔁 Fork Synchronization Logic

Forks are not permanent divergences. They **co-evolve** through feedback loops:

- `Stable` forks feed user insights, confusion points, or new edge cases back into `dev`.
- `Dev` forks feed mature modules or refined language forward into future `stable` versions.

Forks should be cross-referenced explicitly and updated together when appropriate.

---

## 🧷 Cross-Application Guidance

| Protocol                   | Fork Needed? | Status                    |
|----------------------------|--------------|---------------------------|
| Depth Inquiry              | ✅ Yes       | Forked and active         |
| Conflict Navigation        | 🟡 Likely    | Needs meta distinction    |
| Inhale/Exhale Rhythms      | 🟡 Possible  | Seasonal/group forks?     |
| Dialogic Edge Work         | ✅ Yes       | Pending split             |
| Epistemic Integrity        | ❌ No        | Layered, not forked       |
| Disorientation Drills      | ✅ Yes       | Type-based split likely   |

Fork only when:
- Iteration pressure requires divergent simplification or elaboration.
- Subaudience needs diverge structurally, not just pedagogically.

---

## 🧳 Additional Fork Types (For Future Use)

In rare cases, forks may serve:
- **Cross-cultural adaptation**
- **Therapeutic containment versions**
- **Language-translated versions**
- **AI-facing vs. human-facing protocol scaffolds**

These require distinct governance and are considered advanced cases.

---

## ✅ Final Notes

If you fork a protocol:
- Update the associated README to reflect the new structure.
- Link all forks in a common metadata block for discoverability.
- Document version drift explicitly if it affects function or usage norms.

Forking is not failure—it is **fitness through form**. Let the protocol breathe.
