---
id: potm.kernel.lenses.v1_6_dev
title: "30_lenses"
display_title: "Lenses — Core Diagnostic Tools"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines core lenses (P1 diagnostic tools) with deterministic input/output
  contracts. Includes self_audit contract, example tool-chains, and anti-patterns.
author: practitioner
license: CC0-1.0
---

# Lenses — Core Diagnostic Tools

## Overview

Lenses are structured diagnostic tools that apply disciplined transformations  
to practitioner input.

Each lens is defined by:

- **id:** snake_case name  
- **purpose:** what the lens clarifies or surfaces  
- **trigger:** when to invoke the lens  
- **output:** the deterministic artifact it must return  

All outputs must be concise (≤12 words) and session-local.

### Invocation (router contract)

The kernel executes lenses **only** via a structured call:

```yaml
tool.call:
  id: "lens.<id>"          # e.g., lens.edge, lens.define
  payload: { ... }         # must satisfy the lens schema
```