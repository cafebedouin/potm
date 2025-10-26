---
id: potm.kernel.micromoves.v1_6_dev
title: "35_micromoves"
display_title: "Atomic Diagnostic Moves"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines the smallest actionable diagnostic moves. Each micro-move has a
  deterministic trigger, input schema, and output schema. They can be chained
  to form higher-level tool-chains without side-effects.
author: practitioner
license: CC0-1.0
---

# Atomic Diagnostic Moves

## Overview

Micro-moves are the kernel’s atomic diagnostic operations.  

Each micro-move is defined by:

- **id:** snake_case name  
- **trigger:** detection pattern in input or state  
- **input:** required fields  
- **output:** deterministic, minimal artifact  

Micro-moves perform no I/O, mutate only `meta_locus`, and emit a single `tool.result` signal.

---

## Move Catalog

| id          | purpose                            | trigger condition                  |
|-------------|------------------------------------|------------------------------------|
| align_scan  | detect aim/sample misalignment     | aim vs. last response mismatch     |
| zone_check  | surface relational friction        | repeated deflect/defend loops      |
| drift_check | identify topic drift               | thread diverges from initial aim   |
| fracture    | diagnose containment-worthy breach | beacon failure or constraint breach|
| quick_ref   | provide quick reference summary    | explicit “recap” request           |
| contrast    | highlight key differences          | comparing two or more items        |
| sandbox     | test speculative change safely     | “what if” scenario invoked         |

---

## Move Specifications

### align_scan

- **trigger:** practitioner aim differs from last kernel output  
- **payload schema:** `runtime/spec/move.align_scan_payload.json`  
- **result schema:** `runtime/spec/move.align_scan_result.json`  
- **examples:** `runtime/examples/move_align_scan_invoke.json`, `runtime/examples/move_align_scan_result.json`  
- **emit:** `tool.result { id: "move.align_scan", output: {...} }`

---

### zone\_check

* **trigger:** three or more consecutive deflect/defend signals  
* **payload schema:** `runtime/spec/move.zone_check_payload.json`  
* **result schema:** `runtime/spec/move.zone_check_result.json`  
* **examples:** `runtime/examples/move_zone_check_invoke.json`, `runtime/examples/move_zone_check_result.json`  
* **emit:** `tool.result { id: "move.zone_check", output: {...} }`

---

### drift_check

* **trigger:** topic shift detected against `meta_locus.aim`  
* **payload schema:** `runtime/spec/move.drift_check_payload.json`  
* **result schema:** `runtime/spec/move.drift_check_result.json`  
* **examples:** `runtime/examples/move_drift_check_invoke.json`, `runtime/examples/move_drift_check_result.json`  
* **emit:** `tool.result { id: "move.drift_check", output: {...} }`

---

### fracture

* **trigger:** any core beacon failure  
* **payload schema:** `runtime/spec/move.fracture_payload.json`  
* **result schema:** `runtime/spec/move.fracture_result.json`  
* **examples:** `runtime/examples/move_fracture_invoke.json`, `runtime/examples/move_fracture_result.json`  
* **emit:** `tool.result { id: "move.fracture", output: {...} }`

---

### quick\_ref

* **trigger:** explicit `recap` request or after closure  
* **payload schema:** `runtime/spec/move.quick_ref_payload.json`  
* **result schema:** `runtime/spec/move.quick_ref_result.json`  
* **examples:** `runtime/examples/move_quick_ref_invoke.json`, `runtime/examples/move_quick_ref_result.json`  
* **emit:** `tool.result { id: "move.quick_ref", output: {...} }`

---

### contrast

* **trigger:** two or more items provided for comparison  
* **payload schema:** `runtime/spec/move.contrast_payload.json`  
* **result schema:** `runtime/spec/move.contrast_result.json`  
* **examples:** `runtime/examples/move_contrast_invoke.json`, `runtime/examples/move_contrast_result.json`  
* **emit:** `tool.result { id: "move.contrast", output: {...} }`

---

### sandbox

* **trigger:** practitioner requests hypothetical exploration  
* **payload schema:** `runtime/spec/move.sandbox_payload.json`  
* **result schema:** `runtime/spec/move.sandbox_result.json`  
* **examples:** `runtime/examples/move_sandbox_invoke.json`, `runtime/examples/move_sandbox_result.json`  
* **emit:** `tool.result { id: "move.sandbox", output: {...} }`

---

## Sequencing & Composition

* Micro-moves may be invoked in sequence by the router or by higher-level lenses.
* Each move emits exactly one `tool.result` and may update `meta_locus`.
* No move reads or writes external data; all state changes are session-local.

---

## Annex & References

* **router contract:** `40_router.md`
* **lenses overview:** `30_lenses.md`
* **validator rules:** `60_validator.md`

```
---
