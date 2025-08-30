# Runtime Examples Index

Canonical JSON instances used by kernel invariants.  
Each file validates against schemas in `runtime/schema/`.  
Kernel files (e.g. `70_state.md`) reference these examples by pointer only.

---

## State (70_state)

- state_meta_locus.json — default session state snapshot  
- state_ledger_buffer.json — baseline empty ledger buffer  
- state_accept_entry.json — entry gate accepted (`accepted=true`)  
- state_open_fracture.json — review_queue populated with fracture id  
- state_record_latency_breach.json — ledger entry for latency breach  
- state_set_latency_mode.json — latency mode switched to `lite`  
- state_log_latency_breach.json — latency breach logged + lens output  
- state_set_mode_profile.json — manual mode_profile override → strict  
- state_read_mode_profile.json — lens output of current profile  
- state_record_mode_profile_change.json — ledger entry recording profile change  
- state_record_canary_report.json — ledger entry for canary emission  
- state_canary_status.json — lens output reporting last canary signal  
- state_escalation_tier2.json — Tier 2 escalation (escalate_profile)  
- state_escalation_tier3_fracture.json — Tier 3 escalation (fracture trigger)  
- state_escalation_tier4_containment.json — Tier 4 escalation (containment enabled)  
- state_escalation_status.json — lens output reporting last escalation event  
- state_escalation_quota_exceeded.json — escalation attempt blocked by quota
