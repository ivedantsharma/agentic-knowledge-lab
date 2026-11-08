# EXP-047: Per-Section Chunk Rank Diagnostic

## Research question

Is the Cirrus answer-bearing chunk weak even inside its correct section, or is it only pushed down because multiple chunks from the distractor section dominate the global ranking?

## Why this matters

If the relevant chunk ranks highly within its own section, the next fix should preserve section diversity.

If it ranks poorly even within its own section, the problem is the chunk scorer or chunk representation.

## Experiment

For each retained section:

- rank only that section's chunks,
- record the evidence-bearing chunk's within-section rank,
- compare that rank with its pooled global rank.

## Metrics

- global relevant chunk rank
- within-section relevant chunk rank
- number of chunks per retained section
- section-level candidate concentration.

## No architecture change

This is diagnostic only.