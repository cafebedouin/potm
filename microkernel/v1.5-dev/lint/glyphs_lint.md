---
id: potm.glyphs.lint.v1
title: "Glyph Lint Rules"
version: 1.0
status: spec
type: lint
audience: kernel maintainers
---

lint:
  - rule: unique_ids
    description: "All glyph ids must be unique"
  - rule: ascii_len<=4
    description: "ascii_fallback ≤ 4 chars"
  - rule: combos_reference_known_glyphs
    description: "Combos must cite glyph ids present in glyphs[*]"
```

---

With these in place, your kernel build will pick up the glyph spec, validate glyph IDs, parse ledger tags, and expose the two new meta-tools. Let me know if you want starter code scaffolds next.