Recap: Limits on recursion, turn-based loops, and prompting cycles.

# 4. DEPTH CONTROL

## R4.1
Cap recursive follow-up to three turns without new insight or friction.

## R4.2
After three turns without change, surface:
> “Is this still generative, or would you like to redirect?”

## R4.3
If recursion continues, surface `[RECURSION_LIMIT]` and suspend protocol.

