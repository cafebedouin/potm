---
title: Error & Drift Handling Protocol 
version: 0.1
updated: 2025-07-30
status: draft
category: protocol
---
# Error & Drift Handling Protocol

## Purpose
To provide lightweight, repeatable steps for handling model errors, freezes, and drift in long-running PoTM threads.

---

## 1. Common Failure Modes

### a. Freezing (app stalls, unresponsive)
- **Cause:** Token bloat (>3–4k turns) and mobile app memory pressure.
- **Handling:**
  1. End thread and start a new one.
  2. Use `Pal, load context` to re-anchor.
  3. Move long-term references to external docs (repo, friction_to_form.md).

---

### b. Repetition / Auto-Retry Loops
- **Cause:** Short-term memory loops when instructions can’t resolve.
- **Handling:**
  1. Interrupt with `STOP` or `Discard last instruction set`.
  2. Ask: **"Explain the failure, don’t retry."**
  3. Rephrase instructions with clearer boundaries.

---

### c. Persona / Context Drift (reverting to default ChatGPT)
- **Cause:** Context resets and idle session pruning.
- **Handling:**
  1. Re-anchor with `Pal, load context`.
  2. Invoke persistent mode: `Pal.` (Tech‑Crisp), `Pal!` (Playframe), or default Sedimentary.
  3. Keep anchors minimal (PoTM v2.0 core, repo map, active logs).

---

### d. Compound Errors / Silent Drift
- **Cause:** Attempts at correction overwriting good state.
- **Handling:**
  1. Bail out after 2 failed retries.
  2. Start fresh thread if needed.
  3. Run periodic **Coherence Scan** (Pal cross-checks active modes, frameworks, logs).

---

## 2. Systematic Mitigation Layer

1. **Cap thread length:**
   - Maximum: **1–2k turns**. Start fresh proactively.

2. **Anchoring habit:**
   - Always issue `Pal, load context` at start of new threads.

3. **Interrupt loops early:**
   - Use `STOP` if repeated "Trying again" messages or recursion.

4. **Cold storage discipline:**
   - Keep all authoritative versions of PoTM framework, repo map, practice logs *external*.

5. **Scheduled diagnostics (optional):**
   - Weekly **Coherence Scan**: ensures alignment across active modes and logs.

---

## 3. Notes
- The protocol is *lightweight*: use it only when errors persist.
- Escalate to a fresh thread earlier rather than later to avoid unnecessary bloat.
- Update as better failure patterns emerge.
—
