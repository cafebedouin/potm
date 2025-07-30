---
title: "Practice vs. Protocol vs. View"
version: "v1.1"
status: "reference"
type: "meta"
tags: 
  - taxonomy
  - repo-structure
last_updated: "2025-07-30"
---
## Practice vs. Protocol vs. View

### 1. **Practice** – *Embodied, repeatable skill*
- **Definition:** A minimal action or posture you can return to repeatedly in daily life.
- **Characteristics:**
  - Portable and modular.
  - Does not require a container.
  - Can stand alone or be combined with others.
- **Examples:**
  - *Waiting With*: mantra + micro-steps (*Notice → Breathe → Stay*).
  - *Labeling* during meditation.

---

### 2. **Protocol** – *Structured, multi-step intervention*
- **Definition:** A designed sequence with entry criteria, explicit steps, and usually an exit condition.
- **Characteristics:**
  - Time-bounded and containerized (often with safeguards).
  - May integrate multiple practices.
  - Often context-specific.
- **Examples:**
  - *Signal Bleed Protocol*: sequenced curiosity engagement with safeguards.
  - *Disorientation Drill #1*: structured confrontation with disorientation.

---

### 3. **View** – *Lens or stance that frames experience*
- **Definition:** A background orientation that shapes how all practices and protocols are approached.
- **Characteristics:**
  - Persistent rather than episodic.
  - More cognitive or philosophical.
  - Can infuse practices/protocols with meaning, or arise from them.
- **Examples:**
  - *Self as stance*: identity is a mask, not a fixed essence.
  - *Discomfort as teacher*: discomfort is not inherently bad.

---

## Boundary Fluidity & Category Drift

These categories are tools, not walls. Boundaries can be porous and that is informative.

- **Practice ⇄ Protocol:** Some practices have enough scaffolding to feel protocol‑ish; some protocols, once internalized, collapse into practice‑like reflexes.
  - **Example (liminal):** *Waiting With* has more structure than a simple practice (mantra + sequence + safety note) but lacks a full protocol container (no entry/exit conditions, no timebox). It remains a **practice** that productively lives near the protocol boundary.
- **Practice ⇄ View:** Deep repetition can shift baseline stance (e.g., mindfulness training → “I am not my thoughts”), turning an embodied skill into a persistent lens.
- **Protocol ⇄ View:** Long engagement with a protocol can normalize a way of seeing, which then colors contexts beyond the original container.

**Documentation guidance (to keep the system clean while embracing blur):**
- **Tag the primary type** (`type: practice|protocol|view`) and add a secondary tag for liminality when useful (e.g., `tags: [practice, liminal-protocol]`).
- **Name the boundary explicitly** in the doc’s Notes when relevant (one or two lines).
- **Guardrails for classification:**
  - If it **requires** entry criteria, timebox, and exit conditions → **Protocol**.
  - If it is **portable on demand** with ≤3 micro-steps → **Practice**.
  - If it **reframes** other work and persists in the background → **View**.

---
