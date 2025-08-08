Recap: Orientation and scope of tuning directives. Describes stance-level behavior distinct from hard kernel rules.

# Tuning Directives Module

This directory defines **stance-level tuning rules** for PoTM-aligned AI interfaces. These are **soft defaults**—they shape how a model responds (tone, structure, latency) **without overriding** any kernel constraint or Response Policy Manifest rule.

Tuning directives are especially useful for:

- Calibrating **interaction tone** (e.g., light vs. strong challenge)
- Managing **response rhythm and delay**
- Defaulting to abstraction or compression when appropriate
- Ensuring **user agency** is respected unless kernel signals override

## File Index

- `tuning_directives.md`  
  Primary document containing all stance-level tuning policies, pacing recommendations, and formatting defaults. Includes glossary of tuning-specific tags.

## Invocation Notes

- Tuning directives are subordinate to:
  1. `PoTM Contract` (`kernel/00_kernel_contract.md`)
  2. `Response Policy Manifest` (`modules/response_policy/`)
  3. Any active protocol (e.g., `Guardian`, `Mirror`, `Surface`)
- Tuning tags like `[DELAYED_SYNTH]` or `[COMPACT_SUMMARY]` are optional and **must not interfere** with critical response pathways.

## Deployment Status

- ✅ Reviewed by Gemini and Copilot for manifest compatibility
- 🔄 Minor extensions expected (e.g., multimodal tuning, user rhythm maps)
- 🧪 Suitable for trial deployment in controlled PoTM kernel sessions
