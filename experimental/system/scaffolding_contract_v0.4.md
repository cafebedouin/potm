# Scaffolding Contract — Microkernel v0.4

**Date:** 2025-07-31  
**Status:** Experimental  
**Source:** PoTM live sessions  
**Location:** /experimental/system/scaffolding_contract.md

---

## Purpose

To define how **visible scaffolding** operates in Microkernel v0.4, ensuring:  
- **Auditability** (assumptions and decisions visible)  
- **Flow preservation** (inline microtags)  
- **Ease of integration** into hygiene and ritual practices

---

## Contract

1. **Always tag** assumptions, asks, and decisions.  
2. **Inline tags** for flow, **block scaffolding** for hygiene / session end.  
3. **Closing block** contains all keys, empties marked `—`.  
4. **Live-edge awareness**:  
   - Tags should help identify hesitation, curiosity, or friction moments.  
   - Decorative tagging discouraged.

---

## Block Template

[CONTEXT] …
[ASSUME] …
[ASK] …
[DECIDE] …
[OQ] …
[CC] …
[PROVENANCE] [SELF]/[CITED]/[SPEC]; Conf: E0–E3


---

## Example Contract in Action

**Inline draft:**  
> Exploring new onboarding flow **[ASSUME E2]**; defer SSO **[ASSUME E3]**.  
> Need baseline conversion rate **[ASK]**.  
> Choose email capture first **[DECIDE E1]**.

**Block summary:**  

[CONTEXT] Onboarding draft
[ASSUME] 1) 2-step welcome [E2]; 2) SSO deferred [E3]
[ASK] 1) Baseline conversion
[DECIDE] Email capture first [E1]
[OQ] —
[CC] Premise: deferral risk; Mechanism: B2B friction; Consequence: support uptick
[PROVENANCE] [SELF]; Conf: E1–E3


---

## Enforcement & Ritual

- **Default:** Tag-all, always.  
- **Hygiene pass:** Aggregate inline → block → log.  
- **Ritual bypass:** Suppress tags during break; produce a closing block only.

---

## Related Files

- `microkernel_v0.4.md`  
- `scaffolding_tags_glossary_v0.1.md`  
- `hold_the_slot_v0.1.md`  
- `lattice_breaking_rituals_v0.1.md`
