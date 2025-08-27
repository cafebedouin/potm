

### JOURNALS_DECK_ADAPTER (P1)

Purpose: expose `data/journals/prompts.yaml` as a selectable deck via `deck_call`.

Data Source:
  - path: data/journals/prompts.yaml
  - schema:
      id: journal_prompts
      prompts[*]:
        - id: ^journal:\d{3}$
        - title?: string
        - body|prompt: string              # body preferred; fallback to prompt
        - tags: [lower-case, hyphen-slugs]
        - themes?: [broad buckets]

Invocation:
  on_event: deck_call
  payload:
    deck: "journals"                      # REQUIRED (selects this adapter)
    k: int=1                              # how many prompts to draw
    tags_any?: [string]                   # optional OR-filter on tags
    themes_any?: [string]                 # optional OR-filter on themes

Dispatch:
  - If deck != "journals": pass to other deck adapter(s).
  - Else:
      • Load prompts list
      • Filter by tags_any/themes_any (OR within each list; AND across lists)
      • Sample k items without replacement (cap at pool size)

Output (adapter_result):
  type: adapter_result
  payload:
    deck: "journals"
    count: <int>
    items:
      - id: journal:0xx
        title: <string or ->                    # if missing, derive from first 6 words of body
        body: <string>                          # preferred field
        tags: [ ... ]
        themes: [ ... ]                         # may be absent
