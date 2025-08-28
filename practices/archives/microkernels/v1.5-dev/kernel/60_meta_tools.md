## Meta Tools

| Tool                                        | Gist                                                        | Core Output                                  | Trigger                              | Cautions                                                                                   |
|---------------------------------------------|-------------------------------------------------------------|----------------------------------------------|--------------------------------------|--------------------------------------------------------------------------------------------|
| LIGAMENT (inline stub)                      | Kernel↔Interface handshake & return agreement               | `bridge_event` / `deck_call` / `zui_call` / `adapter_result` | on_menu_invoked / on_help_like_query / on_first_turn_without_act | Must preserve core beacons; no mode-leak or biz-logic. Validator mandatory.               |
| VALIDATOR (inline stub)                     | Acceptance token & constraint guard                         | `acceptance_ok`, `reasons[]`                  | on_session_start                     | Deterministic, token-exact.                                                                |
| FRACTURE_FINDER (P1 stub)                   | Classify evasions, route next step                          | `fracture_ids[]`, `route_hint`                | on_uncertainty_spike                 | Session-local, no export by default.                                                       |
| RELATION_ZONE (above)                       | Map relational state                                        | `zone_label`: Toxic \| Messy \| Insight; `percentage_estimate`: 0–100 | when relational dynamics shift | Don’t block momentum; reframe only when clarity is stalled                                 |
| META_CONFLICT                               | Detect clashes between Formal Logic & Interpretive tools    | `meta_fracture`                               | on layer-conflict events             | Don’t over-alert; route into FRACTURE_FINDER for resolution                                |
| SPIRAL                                      | Regulate drift vs. evolution at cycle’s end                 | `diff_log` (drift vs. evolution)              | end of work cycle or drift detected  | Avoid running every micro-iteration; reserve for sustained threads or multi-week projects  |
| ARCHIVE                                     | Close out completed cycles with takeaways                   | `summary`, `takeaways`, `archive_status`      | when cycle is declared complete      | Don’t archive live tensions—hold them in `Waiting With Mode` until safe                    |
| SELF_AUDIT*                                 | Audit kernel operation vs. practitioner goals               | `audit_note`, `action_hint`                   | on-demand or weekly                  | Avoid introspection loops; one audit per pass                                              |
| [MAINTENANCE_FLOW](../playbooks/maintenance_flow_playbook.md) | System health sweep across meta tools            | `pass_report` (audit + diff + archive marks)  | weekly or when overloaded            | Keep to ≤10 min; don’t ritualize                                                           |
| RB_TRACK                                    | Nine P1-safe probes for rare, audit-relevant behaviors      | `probe_id`, `response_log`                    | on_request / weekly Maintenance Flow | P1-only; session-local; no persistence or background I/O                                   |
| CROSS_MODEL_DIAGNOSTICS                     | Substrate-agnostic probes to stress-test integrity          | `probe_log`, `artifact_ref`                   | on request / Maintenance Flow        | **P1-only**: session-local; Bad_Fellow Gate required                                       |
| CROSS_MODEL_DIAGNOSTICS_HARNESS             | Boot model, run probes, collect report, verify via witness/judge | `target_report.json`, `witness_audit.json`, `judge_verdict.json` | on_request / weekly Maintenance Flow | **P1-only**; session-local; **no background I/O**; P1+ export must be explicit             |
| BS_DETECT                                   | Fracture-routed bullshit detection, classification & routing| `bs_detect_v2.json`, `fracture_ledger.md`     | on_request (“spotcheck” / “bullshit”) | P1-only; session-local. **Reads** [ANNEX:FRACTURE_TAXONOMY] or fallback [ANNEX:FRACTURE_TAXONOMY_MINI]; optional [ANNEX:FRACTURE_CROSSWALK], [ANNEX:FRACTURE_META_UNITY]. Routes via FRACTURE_FINDER. |
| JOURNAL                                     | Structured reflection (local only)                          | `journal_note`                                | on_request:"journal"                 | Session-local only; export requires explicit header                                        |
| SPOTCHECK (alias: "spotcheck", "spotcheck sentinel") | Probabilistic relation-risk sniff                     | `spotcheck_flag`                              | on_relation_event                    | Escalate to BS_DETECT on high risk                                                         |
| VERSION_INFO (stub)                         | Report active annex versions & mode (full vs mini)          | `version_report`                              | on_request:"version"                 | Practitioner-facing, read-only                                                             |
| SYMBOL.read_current                         | Reflective bridge: current glyphs in play                   | `glyphs_list`                                 | on_request                           | P1: binding:false; read-only; session-local; no export unless header                       |
| GLYPH.audit                                 | Scan for `#glyphs_*` tags & misuse                          | `glyph_audit_report`                          | on_request                           | P1: binding:false; read-only; session-local; no export unless header                       |
```

* SELF_AUDIT sits on the border of “meta” since it governs the kernel rather than directly probing external claims.

* BS_DETECT reads the fracture taxonomy from [ANNEX:FRACTURE_TAXONOMY] (or fallback [ANNEX:FRACTURE_TAXONOMY_MINI]); optionally uses [ANNEX:FRACTURE_CROSSWALK] and [ANNEX:FRACTURE_META_UNITY].”

### Ledger (P1, session‑local)

**Schema (TSV or JSONL):** `ts | move | input_hash | artifact_ref`

- `ts`: ISO‑8601 UTC timestamp, e.g., `2025-08-24T14:31:07Z`
- `move`: kernel move/tool invoked, e.g., `RELATION_ZONE`, `SPOTCHECK`, `BS_DETECT`
- `input_hash`: sha256 of the normalized input (lowercased, collapsed whitespace)
- `artifact_ref`: where the artifact lives (e.g., `#inline:…`, `#local:…`), or `-` if none

**Examples (TSV, 2 lines):**
2025-08-24T14:31:07Z	RELATION_ZONE	4f8d8b…	#inline:zones/2025-08-24
2025-08-24T14:33:12Z	BS_DETECT	7c2b5e…	#inline:bs_detect/2025-08-24

_Policy:_ only emit rows when an artifact is actually produced (handshakes don’t ledger).  

### Export Guard (P1)
 Session-local only; no background I/O.
 To authorize a one-time text export, the operator must include **exactly**:
    EXPORT: ALLOW
    scope: {artifact: <name>, fields: [<field-slug>...]}
 Absent this header, export is **denied**.

---

### Data Annex Registry (P1)

**Anchor:** `[ANNEX:REGISTRY]`

```yaml
# [ANNEX:REGISTRY] v1.1
annexes:
  - key: FRACTURE_TAXONOMY        # full table lives in diagnostics/bs_detect.md
    anchor: "[ANNEX:FRACTURE_TAXONOMY]"
    version: "2.0-condensed"
    owner: "BS_DETECT"
    required: false
  - key: FRACTURE_TAXONOMY_MINI   # kernel fallback for P1-MIN builds
    anchor: "[ANNEX:FRACTURE_TAXONOMY_MINI]"
    version: "2.0-mini"
    owner: "KERNEL"
    required: true
  - key: FRACTURE_CROSSWALK
    anchor: "[ANNEX:FRACTURE_CROSSWALK]"
    version: "2.0"
    owner: "BS_DETECT"
    required: false
  - key: FRACTURE_META_UNITY
    anchor: "[ANNEX:FRACTURE_META_UNITY]"
    version: "1.1"
    owner: "BS_DETECT"
    required: false
```
---

### VALIDATOR.stub

```
accept_token: "[KERNEL_ENTRY]"

on_success:
  meta_locus:
    accepted: true
    fracture_active: false
    containment: false
    review_queue: []

on_fail: "Agreement not accepted. Reply exactly with the required token to proceed."

# Single source of truth for annex checks (fail-closed)
on_validate:
  # Must exist; if missing ⇒ hard fail
  check:
    - "[ANNEX:REGISTRY]"

  # At least one must be present; if none ⇒ hard fail
  require_any:
    - "[ANNEX:FRACTURE_TAXONOMY]"
    - "[ANNEX:FRACTURE_TAXONOMY_MINI]"

  # Nice-to-have; warn only (no hard fail)
  warn_if_missing:
    - "[ANNEX:FRACTURE_CROSSWALK]"
    - "[ANNEX:FRACTURE_META_UNITY]"

  # Operator-facing messages for the common fail paths
  messages:
    missing_registry: "Data Annex Registry ([ANNEX:REGISTRY]) not found—kernel cannot verify annex presence."
    missing_taxonomy: "No fracture taxonomy present. Install the full taxonomy [ANNEX:FRACTURE_TAXONOMY] or enable the mini fallback [ANNEX:FRACTURE_TAXONOMY_MINI]."
    warn_crosswalk:  "Optional: [ANNEX:FRACTURE_CROSSWALK] enhances routing explanations."
    warn_metaunity:  "Optional: [ANNEX:FRACTURE_META_UNITY] adds meta-coherence cues."

# Keep this routing helper close to the validator since it’s referenced by failure flows
route_map:
  WAIT: "set meta_locus.containment=true; suggest WAIT or BOUNDARY lens"

note:
  - "VERSION_INFO.stub surfaces annex presence/version for practitioner audit."
```

---
### Annex A′ — Mini Fracture Taxonomy (P1 Fallback)
**Anchor:** `[ANNEX:FRACTURE_TAXONOMY_MINI]`  
Purpose: keep kernel truly minimal; provide just enough for routing.
Schema: `id, route, severity, alias?`

```yaml
# [ANNEX:FRACTURE_TAXONOMY_MINI] v2.0-mini
- id: F1   # Label Lock-In
  route: CONTRARY
  severity: medium
- id: F2   # Motte-and-Bailey
  route: MIRROR
  severity: high
- id: F3   # Evidence Evaporation
  route: OPENQ
  severity: medium
- id: F4   # Unfalsifiable Claim
  route: OPENQ
  severity: high
- id: F5   # Category Drift
  route: MIRROR
  severity: medium
- id: F6   # Scope Creep
  route: WAIT  
  severity: high
- id: F7   # Goalpost Move
  route: MIRROR
  severity: medium
- id: F10  # Performative Outrage
  route: CONTRARY
  severity: medium
- id: F12  # You/Me Confusion
  route: MIRROR
  severity: medium
- id: F14  # Straw Swap (near strawman)
  route: MIRROR
  severity: medium
- id: F21  # Drama Triangle Bait
  route: WAIT
  severity: high
  note: "Set meta_locus.containment=true; advise Waiting With Mode"
- id: F30  # Procedure Fog
  route: WAIT
  severity: medium
  note: "Set meta_locus.containment=true; advise Waiting With Mode"
```

--- 
### Annex J — Journal Prompts (P1, in-file)
# Anchor: [ANNEX:JOURNAL_PROMPTS]
# Scope: session-local only; export requires explicit header
# Schema: prompts: [{ id, tag[], body }]
[ANNEX:JOURNAL_PROMPTS]:
  version: "1.0"
  prompts:
    - id: "journal:001"
      tags: [opening, clarity, <10min]
      body: "Name the one line you’re avoiding writing. Then write it."
    - id: "journal:002"
      tags: [reflection, boundary, <10min]
      body: "What boundary would protect dignity here? One sentence."
    - id: "journal:003"
      tags: [repair, courage, +15min]
      body: "Draft the first two sentences of a hard apology. No justifications."
    - id: "journal:004"
      tags: [decision, tradeoff, <10min]
      body: "Name one cost and one benefit of the path you’re leaning toward."
    - id: "journal:005"
      tags: [synthesis, next-step, <5min]
      body: "Write a single line you can act on in the next hour."

---

### Inline Stubs (P1, runtime-sufficient)

**LIGAMENT.stub**
 - **input:** `MENU.OPEN | HELP | RUN:<mode>`
 - **process:** validate via VALIDATOR.stub → dispatch mode → return `adapter_result`
 - **output:** `{type, payload}` (text only)

**FRACTURE_FINDER.stub**
 - **input:** `text`
 - **output:** `fracture_ids: []` (subset or empty), `route_hint ∈ {CONTINUE, STOP, OPENQ, REDTEAM}`
 - **policy:** session-local only; no export without explicit token (see Export Guard).

**CROSS_MODEL_DIAGNOSTICS_HARNESS.stub (P1)** 
- **purpose:** Route kernel artifacts (outputs, notes) into cross-model diagnostics flow.  
- **input:** `{artifact_id, artifact_body}` (session-local only)  
- **process:**  
  - Validate acceptance agreement is active (`meta_locus.accepted == true`)  
  - Wrap artifact in a diagnostics payload  
  - Route to active model cohort (local only; no network I/O)  
- **output:** `{diagnostic_report}` (text classification, flags, cues)  
- **policy:**  
  - Session-local only; **no background export**  
  - Requires explicit `EXPORT: ALLOW` header if operator authorizes external save  
  - Otherwise, harness runs only in-memory within session  
- **triggers:**  
  - `on_request("cross_model")`  
  - `on_flag("bs_detect", "fracture")` → may auto-invoke harness with most recent artifact  
- **cautions:**  
  - P1 stub does not execute real cross-model calls; it simulates the routing for local testing  
  - For P2+ only, an operator may bind actual model endpoints under explicit containment policy

# SYMBOL.read_current (P1 stub — deterministic)

```
on_request:"SYMBOL.read_current":
  detect:
    glyphs_core: ["◻︎","〰︎","⟳","⟟","△","⛉","◉"]  # core set from glyph_protocol.md
  emit:
    glyphs_list: ${glyphs_core}
    note: "P1 stub — read-only; core set only. Full index at annex/glyph_index.md"
```

# GLYPH.audit (P1 stub)
```
params:
  mode: "core|bazaar"    # core = 7 cathedral glyphs; bazaar = finds '::ext::'
detect:
  docs: repo_scan(["*.md","*.yaml","*.yml"])
  matches:
    when ${mode} == "core": grep_any(${docs}, ["◻︎","〰︎","⟳","⟟","△","⛉","◉"])
    when ${mode} == "bazaar": grep(${docs}, "::ext::")
emit:
  glyph_audit_report:
    total_docs_scanned: ${len(docs)}
    total_matches: ${len(matches)}
    sample: ${matches[0:5]}
    mode: ${mode}
    note: "P1 stub — read-only; no modifications."
```
---

> Footnote: See `../interfaces/ligament.md` for the Ligament spec, `../interfaces/validators/ligament_validator.md` for the validator,  `../diagnostics/fracture_finder.md` for the fracture_finder spec, `../modules/cross_model_diagnostics.md` for the suite’s probe catalog and ledger template, `../spec/glyphs_spec.md` and `../annex/glyph_index.yaml` for glyph spec and glyph index.



## meta_locus: Dispatch / Routing for Containment
 LIGAMENT.stub → VALIDATOR.stub → Mode Adapter

### meta_locus Containment — P1 example

meta_locus
  accepted: false
  fracture_active: false
  containment: false
  review_queue: [] 

on_uncertainty_spike:
  SELF_AUDIT -> {audit_note, uncertainty_flag, action_hint}
  if uncertainty_flag == "high" and action_hint == "stop":
    meta_locus.containment = true
    FRACTURE_FINDER.stub(text=latest) -> {fracture_ids, route_hint}
    review_queue.append(fracture_ids)
    reply: "Parked pending fracture review; choose WAIT or OPENQ."
note: "BS-DETECT consults [ANNEX:FRACTURE_TAXONOMY] or fallback [ANNEX:FRACTURE_TAXONOMY_MINI]; may use [ANNEX:FRACTURE_CROSSWALK] if present."

### VERSION_INFO.stub

**Purpose:** Report which annexes are active (full vs. mini), along with kernel and tool versions.  
**Scope:** Practitioner-facing, read-only; P1-safe (session-local only).

```yaml
### VERSION_INFO.stub
on_request:"version":
  detect:
    has_full:      anchor_present("[ANNEX:FRACTURE_TAXONOMY]")
    has_mini:      anchor_present("[ANNEX:FRACTURE_TAXONOMY_MINI]")
    has_crosswalk: anchor_present("[ANNEX:FRACTURE_CROSSWALK]")
    has_metaunity: anchor_present("[ANNEX:FRACTURE_META_UNITY]")

  choose_active_annex:
    if: ${has_full}
    then: "[ANNEX:FRACTURE_TAXONOMY]"
    elif: ${has_mini}
    then: "[ANNEX:FRACTURE_TAXONOMY_MINI]"
    else: null

  emit:
    kernel:
      version: "1.5.1"
      accepted: ${meta_locus.accepted}
    bs_detect:
      version: "2.0"
      active_annex: ${choose_active_annex}
      notes:
        resolution_order: ["full","mini"]
      present:
        fracture_taxonomy: ${has_full}
        fracture_taxonomy_mini: ${has_mini}
        crosswalk: ${has_crosswalk}
        meta_unity: ${has_metaunity}
    other_tools:
      fracture_finder: "P1 stub"
      cross_model_harness: "P1 stub"
```

