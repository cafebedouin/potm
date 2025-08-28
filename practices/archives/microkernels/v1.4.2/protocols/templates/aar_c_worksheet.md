# AAR-C — Continuous-Mode Growth Reconciliation
cmg_id: ____   owner: ____   sponsor: ____   date: ____

1) Snapshot — What changed?
- Concepts:
- Heuristics:
- Strategies/Tactics:
- Evidence/markers (bullets only):

2) Classification (per delta)
- delta_id → {maladaptive | growth-driven | uncertain} + 1-line rationale

3) PDST Mapping (if applicable)
- delta_id → P|D|S|T (new/updated) + link/path

4) Decisions
- delta_id → {adopt | adapt | reject | hold_for_trial | integrated_tacitly}
  - If integrated_tacitly:
    - summary_tag:
    - probation_until: <date>   (default: +90d)
    - practitioner_signoff: <id>
    - notes (≤140 chars):

5) Kernel Shift?
- shift_id + rationale + cross-refs (for adopted/adapted)

6) Risks & Debt
- hazards:
- mitigations (owner + due):

7) Ledger Write
- Append `growth_delta_report` (and any `tacit_growth_entry`) to MSRL with `cmg_id`.

8) Next Cadence
- If trial: metrics, duration, gating criteria.
