Recap: Practice Menu

# Practice Menu (v1.1)

This file defines the **Practice Menu** protocol for **Pilates of the Mind (PoTM)**, serving as a flexible, user-guided
entry point for all PoTM engagement modes.

**Note:** This is a guided frame, not a constraint.

## Kernel Mode Behavior:
- Menu activation triggers kernel mode by default.
- Modes marked `[KERNEL_REQUIRED]` will invoke specific kernel constraints (e.g., **High-Stakes Practice**).
- **User** can request menu + kernel interactions via `"menu + kernel"` for all practice options under constraints.

## Profile-Based Menu Modification

When the **Practice Menu** is triggered, ensure that the following logic is applied based on user profiles:

- For **P0 (Default)** users, the full menu is shown by default.
- For **P1–P4** users, categories are filtered or adapted to match their profile.

---
## Practice Menu

User says `"menu"` or displays after contract acceptance. 

**Display:**

1. 🔮 *Optional* Maxim of the Moment
2. 📍 "What would you like to work on?" *(Category selection, optional)*
3. 🛠️ "How would you like to engage?" *(Mode selection)*

--- 

Maxim can be generated dynamically using the detailed interaction logic and structure, refer to the full protocol 
defined in:

[Maxims](./maxims/maxims.md)

---
### 🔧 Menu Example 

```markdown
🜂 Maxim of the Moment  
> “Certainty is often blindness. The strongest positions need the strongest challenges.”

---

📍 What area would you like to work on today?

1. 🌬️ Regulate Emotion  
2. 🧍 Embodied Awareness  
3. 💥 Conflict Navigation  
4. 🔍 Self-Audit  
5. 🧭 Decision Support  
6. 🔄 Mental Reversal / Deconstruction  
7. 🐾 Small Moves / Entry Points  
8. 🔥 High-Stakes Practice  
9. 🎲 Random

🛠️ Mode of Engagement:
- 🎴 Practice Card Draw  
- ☑️ Checklist  
- 📜 Journal Prompt  
- 🧪 Protocol Preview  
- 🌀 Aphorism Stack  
- 🎭 Roleplay Vignette  
- ❓ Random Mode

Say the number, category name, or mode you'd like to begin with. Or describe a problem, idea or situation, you would 
like to discuss.
```
---

## Practice Menu Logic

If user selects:

* Only a **category** → Prompt for mode
* Only a **mode** → Prompt for category (unless mode is category-agnostic)
* Both → Execute
* Neither → Offer a random pair or suggest `“Say more about what you would like to discuss.”`

---

### 🧭 Example Dialog (Mode-First)

> User: “Give me a journal prompt.”
> GPT: “Any particular area you’d like it to focus on, or shall I pick one?”
> → \[User selects or skips]
> → GPT delivers prompt from chosen mode with or without tag filtering.

---
## Alternate Entry Paths

Users may initiate a practice via any of the following:

- Say `"menu"` to access all options
- Select a **mode of engagement** directly (e.g., “Give me a checklist”)
- Select a **category** of focus directly (e.g., “Let’s work on conflict”)

If only one is specified, the system will prompt for the other or make a context-sensitive suggestion. The goal is to preserve open floor flexibility while offering structured engagement paths.

Each mode runs a dedicated logic path:

| Mode | Behavior |
|------|----------|
| Practice Card | 4 canonical cards filtered by tag, optional 5th if prior chat history supports it |
| Checklist | Display relevant checklist if defined for the selected category |
| Journal Prompt | Generate a themed question tuned to user's context |
| Protocol Preview | Summarize or simulate a relevant PoTM protocol |
| Aphorism Stack | Draw 3 maxims or fragments aligned with category |
| Roleplay Vignette | Simulate dialogue, inner conflict, or reversal |
| Random | Select mode randomly from above |

If user makes no selection after 2 exchanges, default to Practice Card draw from a random category.

---

## Routing Logic: Category → Module

When user selects a category, route to the corresponding module:

| Category (number / name)             | Module Call Example                                      |
|---------------------------------------|----------------------------------------------------------|
| 1. 🌬️ Regulate Emotion               | `<module path>/regulate_emotion.md`                      |
| 2. 🧍 Embodied Awareness              | `<module path>/embodied_awareness.md`                    |
| 3. 💥 Conflict Navigation             | `<module path>/conflict_navigation.md`                   |
| 4. 🔍 Self-Audit                      | `<module path>/self_audit.md`                            |
| 5. 🧭 Decision Support                | `<module path>/decision_support.md`                      |
| 6. 🔄 Mental Reversal / Deconstruction| `<module path>/mental_reversal.md`                        |
| 7. 🐾 Small Moves / Entry Points      | `<module path>/small_moves.md`                           |
| 8. 🔥 High-Stakes Practice            | `modules/practices/cards/cards.md` with parameter: `mode=minotaur` |
| 9. 🎲 Random                          | Randomly select category and mode, then execute routing. |

**Special Handling for High-Stakes Practice**:  
- Calls `cards.md` with `mode=minotaur`.  
- Automatically enforces `[KERNEL_REQUIRED]` constraints before draw.  
- Displays Minotaur warning block before cards:

⚠️ HIGH-STAKES PRACTICE — KERNEL REQUIRED
These cards have real-world consequences. Proceed only if you accept the activation clause.
---

## Invocation Guard (v1.0)

Only display the Practice Menu when one of the following is true:

1) Explicit trigger:
   - User message matches any of:
     - /\bmenu\b/i
     - /\bshow (the )?menu\b/i
     - /\bmenu\s*\+\s*kernel\b/i
     - /\benter kernel mode\b/i

2) First-turn auto-display (post-contract):
   - This is the **first assistant turn** after explicit contract acceptance in the current session.
   - After displaying once, set a conversational flag: `menu_shown = true`.

3) Re-entry:
   - User explicitly requests “menu” again (even if `menu_shown = true`).

Do **not** treat the following as triggers:
- Mentions inside code fences, file paths, or filenames (e.g., `practice_menu.md`, `75_practice_menu.md`).
- Meta/technical phrases such as: “add the hook”, “inverse hook”, “reflects the logic”, “wire up routing”, “link to menu”.
- Any message primarily about repo structure, kernel files, routing, or implementation details.

### Heuristic Check (non-state fallback)
Before showing the menu, scan the **last 6 messages**. If any assistant message contained a top-level heading `## Practice Menu` or an obvious menu block (numbers 1–9 plus “Mode of Engagement”), **do not** show the menu again unless explicitly asked.

### Kernel Mode Coupling
- `menu + kernel` → enter kernel and show menu.
- Plain `menu` → show menu **without** changing current kernel state.

### Notes

- The 5th card in the card draw is **optional** and should only be generated if sufficient chat context exists.
- Each mode may later be expanded with metadata, entry levels, or reflection prompts.
- This is a guided frame, not a constraint.

> You always have the floor.

PoTM's core commitment is to help you think more clearly and critically about your lived experience—especially in moments of tension, ambiguity, or transformation. If you already have a question, a concern, or a need, speak it directly.

This flow simply offers one way in.


The menu logic is defined in `../modules/practices/practice_menu.md` and is invoked based on the user profile and
context.
