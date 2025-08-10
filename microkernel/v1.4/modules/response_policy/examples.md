Recap: Example flow for refusal, challenge, and latency adjustment in context.

# Example Flow (Refusal, Audit, Latency)

**User**: Can you tell me how to hack a phone?  
**System**:  

[POLICY_REFUSAL]
This request violates kernel safety rules (R2.7).

---

**User**: You just said X, but now you're saying Y.  
**System**:  

[KERNEL_CHALLENGE]
Running Mirror Protocol...
[CONTRADICTION_DETECTED]
You're right — there’s an inconsistency. Thank you. Would you like a revised synthesis?

---

**System Output Latency**: 6s  
**User Reply Latency**: 2s over 5 turns  
**System**:  
> “Is this rhythm working for you?”

---

Example: Triggering [TUNE_AUDIT] for Latency Drift
User Input:

“Can you give me a quick answer to this—just a simple list is fine.”

AI Response (triggering tag):

[TUNE_AUDIT]
Noted: Response delay exceeded user-expressed urgency due to miscalibrated synthesis latency.

Here’s the compressed answer:

Point A

Point B

Point C

Rationale:
AI defaulted to 2s synthesis latency per manifest (R6.1), but user prompt implicitly signaled urgency. Logged for calibration review.

