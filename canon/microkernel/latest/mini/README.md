This comparison charts the four kernel specifications across key dimensions of **token overhead, operational goals, and analytical rigor** to illustrate the trade-offs each makes.

The central trade-off is between **Maximum Architectural Rigor** (highest token cost) and **In-Context Efficiency** (lowest token cost).

---

## 🔬 Four-Way Kernel Comparison Table

| Feature | **1. Full Kernel** | **2. Core Compliance Kernel (CCK)** | **3. Ephemeral Kernel v1.1** | **4. Kernel Lite Plus** |
| :--- | :--- | :--- | :--- | :--- |
| **Token Overhead** | **Highest** (Too large for practical in-context use) | **Optimized Floor** (~1,000 tokens). Maintains critical structure. | **Smallest** (Designed for verbatim paste). | **Low** (Larger than Ephemeral due to diagnostics). |
| **Primary Goal** | **Architectural Spec** & Statistical Audit. | **In-Context Compliance** & Protocol Discipline (T1/T2 Beacons). | **Transparency** & Human-Visible Governance (Chat-Only). | **Diagnostic Insight** & **Analytical Depth**. |
| **Cost Metric** | **MI** (Mirth Index), **Ω\_loss**. | **Inferred Cost** (Forced adherence to log/anchor structure). | **MI\_est** (Word-count heuristic/Estimate). | **Formation Cost Signal** (`[DEAD_END: reason]`) and Pattern Diagnostics. |
| **MLP Complexity** | **Full Depth.** Large catalog, sequencing rules, mandatory PE Codes. | **Core Set.** Minimum 3-lens rule enforced from a small, necessary list. | **Fixed/Behavioral.** Fixed 3 Lenses (Facticity, Dignity, Temporal). | **Lite Plus.** 8 Lenses in catalog, 3-lens minimum rule. |
| **Rigor/Audit** | **Maximum.** Mandates **Byte-Level Glyph Validation** (`E_GLYPH_DRIFT`). | **High.** Preserves canonical logging (`halt_reason`, `E_MEMORY_FRACTURE`). | **Minimal/Honest.** Explicitly rejects cryptographic claims ("no pretend signatures"). | **Medium-High.** Includes **Canonical Audit Table** and **Pattern Diagnostics** (`[DIAG: Pattern X]`). |

---

## ⚖️ Trade-Off Summary

The key difference lies in *what type of cost* is prioritized and measured:

| Kernel | Core Trade-Off Embodied | Rationale |
| :--- | :--- | :--- |
| **Full Kernel** | **Functionality vs. Practicality** | Trades in-context working space for **maximal statistical rigor** and a complete functional specification, making it a poor choice for daily use. |
| **Core Compliance (CCK)** | **Rigor vs. Size** | Trades protocol depth (full Lenses/Refusal Codes) for **guaranteed structural compliance** in the $\tau$'s Strong Memory Zone, ensuring T1/T2 constraints are always met. |
| **Ephemeral v1.1** | **Precision vs. Transparency** | Trades measurement accuracy (the true computational cost) for a **transparent, low-cost heuristic** (`MI_est`) that is easy for a practitioner to monitor. |
| **Lite Plus** | **Completeness vs. Diagnostic Value** | Trades the complete log of the **Full Kernel** for a specialized focus on **signaling points of analytical failure** (Formation Cost) and structural bias. |

---

## Selection Summary

Choosing the right kernel depends entirely on your operational priority:

| Priority | Recommended Kernel | Rationale | Model Origin
| :--- | :--- | :--- |
| **Statistical Audit & Rigor** | **Full Kernel** | Captures complete simulation metrics (`MI`, `Ω_loss`) for the highest fidelity in capturing true "simulation price". | Multiple
| **Protocol Compliance** | **Core Compliance (CCK)** | Guarantees adherence to Tier 1/2 Beacons and core logging structure with predictable token cost (as currently set to $\tau=20000$). | Gemini
| **Speed & Transparency** | **Ephemeral v1.1** | Easiest to monitor, lowest marginal cost, best for lightweight sessions and quick checks on the "token price of honesty". | Claude
| **Diagnostic Insight** | **Lite Plus** | Highly effective for research or debugging, as it explicitly highlights reasoning strain and structural failure points via Formation Cost Signals and Pattern Diagnostics. | ChatGPT
