---
id: potm.kernel.externalist_mode.v1_6_dev
title: "79_externalist_mode"
display_title: "Externalist — Diagnostic Overlay"
type: kernel
lifecycle: canon
version: 1.6.0-dev
status: active
stability: stable
summary: >-
  Defines Externalist as a diagnostic overlay lens. When triggered, runs a
  selected mode (Contrary Corner, Frame Inversion, etc.), emits a brief trace
  and reframed question, then decides whether to re-enter the original frame.
author: practitioner
license: CC0-1.0
---

## Purpose

Externalist provides disciplined frame-refusal for rapid structure checks. It
does not replace lenses; it overlays a specific reframe pattern and yields a
compact artifact for decision-making (re-enter vs remain external).

---

## Lifecycle

1) Trigger  
   - Invoke with a named mode and current frame.  
2) Run Mode  
   - Execute the chosen mode (e.g., Boundary / Contrary Corner / Scale Shift / etc.).  
   - Produce a reframed question and log a mode trace.  
3) Emit & Decide  
   - Emit `externalist.result` (status, mode, reframed_question, limiter, ts).  
   - Decide whether to re-enter the original frame with clarified limiters.  

All invocations MUST log `externalist_event` ledger entries.

---

## Failure Modes

- Invalid mode name → `E_PAYLOAD`  
- Missing limiter when required by mode → `E_PRECONDITION`  
- Recursion without re-entry (mode loop) → `E_INVARIANT`  

---

## Pointers

- Payload/Result specs:  
  - `runtime/spec/externalist.invoke_payload.json`  
  - `runtime/spec/externalist.result.json`
- Ledger schema: `runtime/spec/ledger.externalist_event.json`  
- Lens catalog reference: `kernel/30_lenses.md`  
- Router allow-list & examples: `kernel/40_router.md`
 - Practitioner guidance: `kernel/lenses/externalist_diagnostic_modes.md`
