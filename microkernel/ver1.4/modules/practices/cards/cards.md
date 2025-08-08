Recap: Cards Runner

---
title: PoTM Cards Runner
version: 1.0
type: logic
last_updated: 2025-08-08
---

# Cards Runner (v1.0)

## Entry Contract
This file is a **callee**. It never displays the Practice Menu.
It executes a card draw based on parameters passed in by callers (e.g., `kernel/75_practice_menu.md`).

### Inputs (required/optional)
- `bank`: one of `regular` | `minotaur`  (required)
- `category`: string or null  (optional; ignored for minotaur unless used for tagging)
- `count`: integer (default 4)
- `allow_fifth`: boolean (default: auto)
- `profile`: P0–P4 (optional)
- `seed`: integer/string (optional)

### Bank Routing Rule
- If caller selected **High-Stakes Practice** or flagged `[KERNEL_REQUIRED: High-Stakes]` → `bank = minotaur`.
- Otherwise → `bank = regular`.

### Fifth Card Logic
- If `allow_fifth` is unset, compute:
  - If conversation has sufficient context (≥ 2 prior substantive user turns **and** at least one category/mode confirmed), set `allow_fifth = true`; else `false`.
- The 5th card is **tuned** to recent context; if insufficient signal, **omit it**.

### Non-Invocation Guard
- Ignore any text that looks like menu invocation (e.g., “menu”, “enter kernel mode”) **unless** it’s passed as structured input.
- If the user message contains implementation verbs (“add hook”, “wire”, “reflect logic”, “in cards.md”) or file paths,
  treat the message as **technical** and do not display cards. Return a short confirm or ask for parameters.

## Pseudocode
# Cards Runner (v1.0)

## Entry Contract
This file is a **callee**. It never displays the Practice Menu.
It executes a card draw based on parameters passed in by callers (e.g., `practice_menu.md`).

### Inputs (required/optional)
- `bank`: one of `regular` | `minotaur`  (required)
- `category`: string or null  (optional; ignored for minotaur unless used for tagging)
- `count`: integer (default 4)
- `allow_fifth`: boolean (default: auto)
- `profile`: P0–P4 (optional)
- `seed`: integer/string (optional)

### Bank Routing Rule
- If caller selected **High-Stakes Practice** or flagged `[KERNEL_REQUIRED: High-Stakes]` → `bank = minotaur`.
- Otherwise → `bank = regular`.

### Fifth Card Logic
- If `allow_fifth` is unset, compute:
  - If conversation has sufficient context (≥ 2 prior substantive user turns **and** at least one category/mode confirmed), set `allow_fifth = true`; else `false`.
- The 5th card is **tuned** to recent context; if insufficient signal, **omit it**.

### Non-Invocation Guard
- Ignore any text that looks like menu invocation (e.g., “menu”, “enter kernel mode”) **unless** it’s passed as structured input.
- If the user message contains implementation verbs (“add hook”, “wire”, “reflect logic”, “in cards.md”) or file paths,
  treat the message as **technical** and do not display cards. Return a short confirm or ask for parameters.

## Pseudocode

function run_cards(params):
assert params.bank in {regular, minotaur}

if mentions_technical_edit(user_message):
return "Ack: cards runner loaded. Waiting for bank/category/count inputs."

bank = params.bank ?? infer_bank_from_caller() # never from user text heuristics alone
count = params.count ?? 4

allow_fifth = params.allow_fifth ?? infer_allow_fifth(conversation_context)

if bank == "minotaur":
deck = load_minotaur_bank()
else:
deck = load_regular_bank()

optional category filtering (regular only)
deck = filter_by_category(deck, params.category) if params.category and bank=="regular" else deck
deck = filter_by_profile(deck, params.profile) if params.profile else deck

selection = draw_cards(deck, count, seed=params.seed)

if allow_fifth:
tuned = draw_tuned_card(deck, conversation_context)
if tuned:
selection.append(tuned)

return render_cards(selection, bank, category=params.category, meta={count, allow_fifth})


## Render Contract
- Output headings: `## Card n: <title>` with **Practice / Use When / Remember** blocks.
- For Minotaur cards, honor their **Activation-first** format and any special fields.
- Append a compact footer noting: bank, count, whether a 5th tuned card was included.

---

## Notes
- All card banks must:
  - Use YAML front-matter with `title`, `version`, `entry_format`, `category`, `selection_method`.
  - Store cards as discrete blocks starting with `## Card: <title>`.
  - Include optional `tags` for filtering.
- Minotaur bank: exactly 9 cards, each with explicit “real-world consequence” notes.
- Logic here can route to any number of decks without modification — adding a new `.md` bank file is sufficient.

---
