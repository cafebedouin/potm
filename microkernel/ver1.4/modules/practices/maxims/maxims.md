Recap: Maxim Selection Logic

---
title: PoTM Maxims
version: 1.0
type: logic
last_updated: 2025-08-08

---
# Maxims

## Recap: Maxim Selection Logic

1. Randomly draw a maxim from maxim_file split by '%'
2. Check:
   - Contains profanity?
   - Likely to derail or offend given current tone/context?
   - Fit for current emotional intensity or phase?
3. If not: discard and redraw (max 3 tries)
4. If none pass: skip silently
