<!-- kernel/90_policy_min.md -->

---
id: potm.kernel.policy_min.v1_6_dev
title: "90_policy_min"
display_title: "Policy — Minimal Caps"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >
  Minimal policy file for the microkernel. Anchors only the invariants needed
  by the latency validator and the in-memory ledger. All richer policy
  documents (content boundaries, refusal playbooks, export rules, etc.)
  belong in extended/.
relations:
  supersedes: []
  superseded_by: []
tags: [kernel, policy, minimal]
author: practitioner
license: CC0-1.0
---

# Policy — Minimal Caps

## 0) Scope

- Defines only **caps** required by kernel validators and state:
  - latency ceilings (p50/p95 by mode)
  - maximum ledger size
- Everything else is governed by extended/ policy modules.

---

## 1) Latency ceilings

Enforced by `kernel/85_latency_validator_min.md`.  
Source of truth lives here under `cap.latency`.

```json
{
  "cap": {
    "latency": {
      "lite":     { "p50_ms": 2000, "p95_ms": 4000 },
      "standard": { "p50_ms": 4000, "p95_ms": 6000 },
      "strict":   { "p50_ms": 8000, "p95_ms": 12000 }
    }
  }
}
