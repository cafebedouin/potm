# Adapter Checklist (P1)

- Translate prose → `tool.call` with:
  - `meta.request_id` (UUIDv4); stable across retries of the *same* intent.
  - canonicalized payload before compute of `request_id` digest (router will re-check).
- Prefer sequence:
  1) `policy.query(target:"ledger.append")` (preflight)
  2) intended `tool.call`
  3) if `warnings` present, surface briefly + suggest `closure.spiral`.
- For “swerve”: enable `bounded_unskillfulness`, call `move.sandbox{constraints:{fail_soft:true}}`.
