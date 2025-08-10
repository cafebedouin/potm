# 🌱 PoTM Experimental Branch — Idea Garden

**Status:** Experimental  
**Purpose:**  
This branch is the **Idea Garden** — a safe, bounded space for testing promising but unproven PoTM concepts before they move into the stable kernel (“main garden”).

Think of it as a **trial plot**:  
- Ideas are planted here for a **season** of observation.  
- Some are **transplanted** to the main garden after hardening.  
- Others are **composted** to enrich the soil for future growth.  
- A few may **overwinter** here for another cycle of testing.

---

## 🌿 How to Use This Branch

### 1. Select Your Seedling
- Choose a concept, protocol, or pattern that:
  - Has passed initial forge work.
  - Is not yet proven in varied contexts.
- Create a new folder under `/plots/`:
  - Include a short description.
  - State your success/failure criteria.
  - Tag with `forge_origin:idea_garden`.

---

### 2. Prepare Your Plot
- Define **boundaries**:
  - Who is testing it.
  - Where it applies.
  - How long the trial will run.
- Ensure **safe failure** — no breakage of core systems.

---

### 3. Plant and Label
- Add **signage** (README in your plot folder) with:
  - Name & version.
  - Purpose.
  - Feedback channels.
- Make it clear to observers: **This is experimental**.

---

### 4. Observe and Weed
- Maintain a `log.md` in your plot folder:
  - Dates of key observations.
  - Issues found.
  - Adaptations made.
- Remove harmful or unworkable elements early.

---

### 5. Seasonal Review
- At the end of the trial:
  - **Transplant** → Move to main garden (kernel).
  - **Compost** → Archive learnings in `/compost/`.
  - **Overwinter** → Continue here another cycle.

---

## 📂 Branch Structure

experimental/
│
├── README.md                   # Orientation map for the Idea Garden
│
├── ideas/                      # Seedlings ready for trial, grouped by type
│   ├── addons/                 # Companion features or enhancements to existing systems
│   ├── coordination/           # Mechanisms for synchronizing people, agents, or processes
│   ├── critique/               # Tools and frames for structured evaluation and challenge
│   ├── diagnostics/            # Experimental tests and evaluation methods
│   ├── docs/                   # Draft or speculative documentation
│   ├── drills/                 # New micro-practices in testing phase
│   ├── frameworks/             # Early-stage structural maps or organizing schemes
│   ├── governance/             # Emerging decision-making or stewardship structures
│   ├── guidelines/             # Provisional how-to or best-practice notes
│   ├── kernels/                # Proto-kernels or kernel variants in testing
│   ├── logs/                   # Observational notes, run logs, or trial journals
│   ├── meta/                   # Notes on the architecture or philosophy of the system itself
│   ├── modules/                # Practice ideas with limited/partial validation
│   ├── personas/               # Early-stage role or archetype definitions
│   ├── principles/             # Emerging commitments or contestable assertions
│   ├── protocols/              # Draft practice sequences or hybrid methods
│   ├── substrates/             # Foundational layers or enabling environments under trial
│   ├── subsystems/             # Unstable meta-architectures or toolchains
│   ├── systems/                # Larger, interconnected structures in early formation
│   ├── tools/                  # Experimental utilities or implements
│   └── tracking/               # Mutation notes and developmental snapshots
│
├── plots/                      # Active trials planted for the current season
│   ├── idea_name_1/
│   │   ├── README.md
│   │   └── log.md
│   └── idea_name_2/
│
├── compost/                    # Retired experiments — nutrients for future growth
│   ├── idea_name/
│   │   └── summary.md
│
└── review_log.md               # Seasonal review notes and transplant decisions

## 🪴 Tips for Success
- Keep active trials few — 3–5 at most.
- Let each run a **full season** before review.
- Document *why* something is composted — the nutrients matter.
- Encourage diversity; resilience comes from varied plantings.

---

## 🔄 Relation to PoTM Lifecycle
- **Forge** → Raw ideation & shaping.  
- **Idea Garden (this branch)** → Safe real-world trial.  
- **Main Garden (kernel)** → Stable, tested, integrated protocols.


## 📦 ideas/ subfolders (mirrored)

| Folder         | Description |
|----------------|-------------|
| `diagnostics/` | Experimental tests and evaluation methods |
| `docs/`        | Draft or speculative documentation |
| `drills/`      | New micro-practices in testing phase |
| `framework/`   | Early-stage structural maps |
| `modules/`     | Practice ideas with limited or partial validation |
| `principles/`  | Emerging commitments or contestable assertions |
| `protocols/`   | Draft practice sequences or hybrid methods |
| `subsystems/`  | Unstable meta-architectures or toolchains |
| `tracking/`    | Mutation notes and developmental snapshots |

---

## 🧭 Usage

Use with discernment. These materials are **intended for refinement or selective trial**. Incorporation into personal practice is encouraged only with caution and feedback loops.

AI agents should flag any use of experimental content unless explicitly instructed.



