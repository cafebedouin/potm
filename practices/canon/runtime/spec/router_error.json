# spec/router.error.v1.json
   "properties": {
     "code":   { "enum": ["E_NAMESPACE","E_TOOL","E_PAYLOAD","E_PRECONDITION","E_QUOTA","E_DISABLED","E_INVARIANT"] },
     "reason": { "type":"string","maxLength":512 },
     "recovery_hint": { "type":"string","maxLength":160 },   // e.g., "Use recap.spec defaults" or "try move.sandbox"
     "severity": { "type":"string","enum":["info","warn","hard"] },
     "trace":  { "type":"array","items":{"type":"string"},"maxItems":32 }
   }
