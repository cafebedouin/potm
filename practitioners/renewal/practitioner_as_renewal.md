Here’s a draft architectural note that ties the substrate-agnostic framing to the **Quaker Faith & Practice** and **Shikinen Sengu** analogies:

---

```markdown
---
id: potm.arch.practitioner_as_renewal.v1
title: practitioner_as_renewal
display_title: "Practitioner Layer as Renewal Mechanism"
type: architectural_note
status: stable
version: 1.0
stability: core
relations:
  relation_to_agent_protocol: none
  agent_protocol: microkernel/
  practitioner_doc: practitioner/
  supersedes: []
  superseded_by: []
interfaces: [practitioner, microkernel, ledger]
applicability: [P0, P1, P2, P3, P4]
intensity: gentle
preconditions: []
outputs: []
cadence: [generational_review, cultural_update]
entry_cues: ["when formal system risks becoming culturally opaque", "when idioms or examples no longer resonate"]
safety_notes: []
tags: [architecture, substrate_agnostic, renewal, forge_origin:substrate_reframe, spiral_eval:practitioner_feedback]
author: practitioner
license: CC0-1.0
---

## Substrate-Agnostic Framing

In PoTM, the **microkernel/** is the formal, procedural, invariant core of the framework — the canonical specification of logic and structure. The **practitioner/** layer is the interpretive, situated interface that enables humans to engage with that logic in culturally and cognitively resonant ways.

This distinction is **substrate-agnostic**:
- The microkernel can be executed by any procedural substrate — AI, rulebook, legal code, manual craft.
- The practitioner layer exists wherever a human (or human group) must interpret and apply that logic in a lived context.

## The Renewal Analogy

Two living traditions illustrate the practitioner layer’s role as a *renewal mechanism*:

1. **Quaker Faith & Practice**  
   Every ~20 years, Quakers rewrite their *Faith & Practice* book.  
   - **Formal constants** (core beliefs, procedural logic) remain intact.  
   - **Interpretive surface** (language, idioms, examples) is updated to match the lived reality and vocabulary of a new generation.  
   This is not “re-inventing” the faith — it’s ensuring continued *legibility* and *applicability*.

2. **Shikinen Sengu at Ise Grand Shrine**  
   Every 20 years, the shrine is rebuilt to the exact same architectural blueprint.  
   - The blueprint is the microkernel: fixed, precise, and preserved.  
   - The act of rebuilding is the practitioner layer: skills are re-learned, materials re-selected, and knowledge transmitted *through use*, not just storage.  
   This keeps the structure alive as a *practice*, not just a historical artifact.

## Architectural Implications

- **Not “just docs”:** `practitioner/` is not a secondary gloss on the microkernel. It is a *living interface* that ensures the core logic remains *teachable, applicable, and culturally embedded*.  
- **Cadence matters:** Like the analogies, the practitioner layer benefits from **intentional renewal cycles** to keep the interface fresh without destabilizing the core.  
- **Feedback loop:** Renewal is not one-way. Practitioner updates surface lived experience back into microkernel refinement.

## Schematic

```

microkernel/  →  practitioner/  →  human application
↑                                     ↓
└─────────────── feedback ────────────┘

```

In this model, **renewal** is the bridge between formal consistency and living relevance. Without it, the microkernel risks becoming static and inaccessible. With it, the system retains both integrity and adaptability across generations.

```

---

