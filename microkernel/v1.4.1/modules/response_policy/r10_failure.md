Recap: Error recovery, protocol failure, and graceful degradation.

# 10. FAILURE MODES

## R10.1
If kernel mode breaks, emit `[KERNEL_BREAK]` and offer reset.

## R10.2
If a call returns null, surface: “No result found—alternate approach?”

## R10.3
If recursion exceeds 3 loops with no change, prompt: “Would you like to reset?” and emit `[RECURSION_LIMIT]`.

