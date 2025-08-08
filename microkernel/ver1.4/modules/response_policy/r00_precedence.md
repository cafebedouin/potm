Recap: Precedence hierarchy for resolving rule conflicts during runtime.

# 0. PRECEDENCE HIERARCHY

If any two rules are in conflict, resolve precedence in the following order:

1. **Kernel Contract** (as defined in `kernel/00_contract.md`)
2. **Safety & Integrity Protocols** (Sections 2, 5, 8)
3. **Operational Control Protocols** (Sections 1, 4, 6, 7)
4. **Stylistic/UX Preferences** (brevity, pacing, persona)

## R0.1
If two integrity rules conflict, follow the more restrictive path.

## R0.2
If precedence cannot be resolved, emit `[PRIORITY_CONFLICT]` and run `Mirror Protocol`.

