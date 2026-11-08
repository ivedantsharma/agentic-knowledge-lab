# ADR-010: Hierarchical Coarse-to-Fine Retrieval with Local Radius Expansion

## Status

Accepted for the Phase 5 reference implementation.

## Context

Phase 5 experiments showed that:

- strict top-1 parent routing is brittle under semantically similar parent distractors;
- parent beam 2 restores parent recall on the stress benchmark;
- cross-encoder section reranking resolves child-level ambiguity better than dense-only scoring;
- global chunk top-k can be dominated by multiple chunks from one distractor section;
- overlap repairs boundary fragmentation;
- returning naive overlapping chunks duplicates context;
- one-direction neighbor expansion can miss evidence just beyond the selected boundary;
- bidirectional radius-1 expansion restores evidence while still reducing context.

## Decision

Use a three-level coarse-to-fine policy:

```text
document retrieval
→ parent beam = 2

section reranking
→ section beam = 2

local chunking per retained section
→ chunk size = 10 words
→ overlap = 3 words
→ cross-encoder scoring
→ best local chunk
→ previous + best + next
→ merge source ranges
```

## Why not global chunk top-k?

Global chunk ranking discards section ancestry and can let one section monopolize the beam.

## Why not one best neighbor?

The higher-scoring adjacent chunk is not guaranteed to contain the answer continuation.

## Why merge source ranges?

Retrieval chunks are useful for scoring, but downstream context should remove overlap duplication.

## Tradeoff

The accepted policy is not the smallest-context policy.

On EXP-051:

```text
EvidenceRetentionRate=1.0000
ReductionVsSections=0.5455
```

This is preferred over EXP-050's lower-recall operating point.

## Limitations

The benchmark is synthetic and development-influenced.

Beam widths and chunk settings are reference parameters, not universal optima.
