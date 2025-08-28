---
id: potm.kernel.v1_2_1
title: potm_bootpack_kernel
display_title: "PoTM Boot Pack Kernel v1.2.1 (Single-File, P1)"
type: kernel 
lifecycle: canon
version: 1.2.1
status: active
stability: core
summary: "Self-contained P1 kernel with embedded bridge, validator, and deck data. No external authority required."
relations:
  supersedes: [potm.kernel.v1_2]
  superseded_by: []
tags: [kernel, bootpack, reference, P1, single_file]
author: practitioner
license: CC0-1.0
---
# PoTM Kernel — Part 04 (of 8)
Version: v1.2 | Generated: 2025-08-20

> **Note on Parts**  
> This kernel may be delivered as a **single file** or split into **multiple parts** (e.g. Part 01 of 03) depending on model or platform byte-limits. Content is identical across delivery modes; only packaging differs.

---8<--- FILE: kernel/60_meta_tools.md ---8<---
## Meta Tools

| Tool                                        | Gist                                                        | Core Output                                  | Trigger                              | Cautions                                                                                   |
|---------------------------------------------|-------------------------------------------------------------|-----------------------------------------------|--------------------------------------|--------------------------------------------------------------------------------------------|
| [FRACTURE_FINDER](../diagnostics/fracture_finder.md) | Surface and route logical/interpretive contradictions       | `fracture_list`                              | On interpretive mismatch             | Avoid over-routing; keep focus on actionable fractures                                     |
| RELATION_ZONE (above)                        | Reclassify the entire interaction by mapping relational state | `relation_map`                               | When relational dynamics shift       | Don’t block momentum; use sparingly to reframe only when clarity is stalled                |
| META_CONFLICT                                | Detect clashes between Formal Logic & Interpretive tools     | `meta_fracture`                              | On layer-conflict events             | Don’t over-alert; immediately route into FRACTURE_FINDER for resolution                   |
| SPIRAL                                       | Regulate thread drift vs. evolution at cycle’s end          | `diff_log` (drift vs. evolution)             | End of work cycle or drift detected  | Avoid running every micro-iteration; reserve for sustained threads or multi-week projects   |
| ARCHIVE                                      | Close out completed cycles with takeaways                   | `summary`, `takeaways`, `archive_status`     | When cycle is declared complete      | Don’t archive live tensions or paradoxes—hold them in `Waiting With Mode` until safe       |
| SELF_AUDIT*                                  | Audit the kernel’s own operation vs. practitioner goals     | `audit_note`, `action_hint`                  | On-demand or weekly                  | Avoid introspection loops; schedule deliberately and limit to one audit per pass           |
| [MAINTENANCE_FLOW](../playbooks/maintenance_flow_playbook.md) | System health sweep across meta tools                       | `pass_report` (audit + diff + archive marks) | Weekly or whenever overloaded        | Keep to ≤10 min; don’t turn into a checklist ritual—preserve its lightweight, on-demand nature |
| LIGAMENT  | Kernel↔Interface handshake & return contract     | `bridge_event` / `deck_call` / `adapter_result` | on_menu_invoked / on_help_like_query / on_idle_start | Must preserve core beacons; no mode-leak or biz-logic. Validator mandatory. |

\* SELF_AUDIT sits on the border of “meta” since it governs the kernel rather than directly probing external claims.

> Footnote: See `../interfaces/ligament.md` for the Ligament spec and `../interfaces/validators/ligament_validator.md` for the validator.

---8<--- /END FILE: kernel/60_meta_tools.md ---8<---

---8<--- FILE: kernel/70_closure_tools.md ---8<---
## Closure Tools

### SPIRAL
- **Trigger:** End of a work cycle or when drift/evolution feels possible
- **Outputs:** `diff_log` (initial vs. current state; drift vs. evolution)
- **Example:** “This project expanded from X to Y; drift = scope creep, evolution = refined aim.”
- **Cautions:**
  - Don’t run on every micro-iteration — burns cycles on noise
  - Reserve for sustained threads or projects

### ARCHIVE
- **Trigger:** Practitioner declares a cycle complete
- **Outputs:** `summary`, `takeaways`, `archive_status` (resolved, parked, stalled)
- **Example:** “Archived: draft review. Takeaways = 3; status = resolved.”
- **Cautions:**
  - Don’t archive live tensions or paradoxes — hold them in `Waiting With Mode`
  - Use only when closure is safe

---8<--- /END FILE: kernel/70_closure_tools.md ---8<---

---8<--- FILE: data/decks/cards.yaml ---8<---
# data/decks/cards.yaml
id: cards
title: "Card Deck"
cards:
  - id: "minotaur:001"
    title: "The Truth Tell"
    tags: [truth, confession, vulnerability, rupture]
    body: |-
      **Action:**
      Confess something you concealed from someone it directly affects.

      **Activation Clause:**
      Do not draw this card unless you are willing to say it out loud to them within 48 hours.

      **Point of No Return:**
      Once you text, call, or set the meeting: you commit to not backing out.

      Do not embellish the truth.

  - id: "minotaur:002"
    title: "The Pattern Break"
    tags: [pattern, disruption, witness, integrity]
    body: |-
      **Action:**
      Publicly interrupt a behavior others associate with you but that is corrosive.

      **Activation Clause:**
      This must be witnessed by at least one person who knows your pattern.

      **Examples:**
      Gossip, chronic lateness, subtle control, false modesty or passive-aggression.

      Don't pick a small issue.

  - id: "minotaur:003"
    title: "The Ask Impossible"
    tags: [request, vulnerability, intimacy, risk]
    body: |-
      **Action:**
      Make a vulnerable request to someone that risks rejection, rupture, or deep contact.

      **Activation Clause:**
      You must deliver the ask without hedging or disclaimers.

      **Examples:**
      “Can you forgive me?” "Will you stay?" “Will you stop doing this to me?” “I need help.”

      Don't soften to avoid vulnerability.

  - id: "minotaur:004"
    title: "The Debt Pay"
    tags: [apology, accountability, repair, humility]
    body: |-
      **Action:**
      Apologize for something you’ve previously justified, minimized, or avoided.

      **Activation Clause:**
      You must accept that forgiveness may not be offered.

      **Requirements:**
      • Speak only to the person affected.
      • State the harm without defending yourself.
      • Ask nothing in return.
      • Do not say, "I'm sorry you feel that way..."

  - id: "minotaur:005"
    title: "The Legacy Break"
    tags: [inheritance, autonomy, refusal, identity]
    body: |-
      **Action:**
      Refuse an inheritance: a family script, identity, or obligation you no longer consent to carry.

      **Activation Clause:**
      Name it out loud to family, peer or journal.

      **Point of No Return:**
      If they say yes, the door is opened.

      If you do it with someone who wants you to refuse, then it is only theater.

  - id: "minotaur:006"
    title: "The Witness Invitation"
    tags: [witness, courage, visibility, exposure]
    body: |-
      **Action:**
      Choose someone you trust. Invite them to witness you perform a Minotaur card.

      **Activation Clause:**
      You must accept the possibility of being seen and still misunderstood.

      **Requirements:**
      • Tell them what you’re doing.
      • Ask only for presence, not reassurance.

      Performing for praise is theater.

  - id: "minotaur:007"
    title: "The Unshielded Ear"
    tags: [listening, critique, humility, feedback]
    body: |-
      **Action:**
      Invite someone you trust (or harmed) to tell you their unfiltered critique of your behavior or impact.

      **Activation Clause:**
      Listen without interruption, defense, or visible reaction.

      **Requirements:**
      • Minimum of five minutes.
      • When they are done, say "Thank you."

      No rebuttals. Walk away or close the conversation.

  - id: "minotaur:008"
    title: "The Physical Hold"
    tags: [presence, body, attention, intensity]
    body: |-
      **Action:**
      During another Minotaur card action, keep sustained eye contact and physical presence

      **Activation Clause:**
      Once contact is made, do not look away, fidget or gesture nervously.

      **Requirements:**
      • Remain bodily present throughout.
      • Give your undivided attention.

      Do not use this as a power move.

  - id: "minotaur:009"
    title: "The Inventory"
    tags: [accountability, reflection, avoidance, honesty]
    body: |-
      **Action:**
      Name aloud the Minotaur cards you have not performed. Name why.

      **Activation Clause:**
      Commit to finding what you are avoiding.

      **Requirements:**
      • Say it to a trusted friend, peer, partner, or even a mirror.
      • No explanation. No reframing.

      Once named, avoidance has structure. Rationalize delays are only justification.

---8<--- /END FILE: data/decks/cards.yaml ---8<---

