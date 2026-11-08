# EXP-048: Section-Aware Neighbor Expansion

## Research question

Can section-aware local chunk retrieval plus one-hop neighbor expansion preserve all evidence without relying on a global chunk beam?

## Fixed components

- parent beam = 2
- section beam = 2
- chunk size = 10 words
- chunk overlap = 3
- MiniLM parent routing
- cross-encoder section ranking
- cross-encoder chunk scoring
- same stress corpus
- same tasks

## Treatment

For each retained section:

```text
score chunks locally
→ choose best local chunk
→ retain that chunk plus one immediate neighbor
```

The final retained set is the union across the two retained sections.

## Why this is hierarchy-aware

The policy preserves representation from each retained section instead of allowing one section to monopolize a global chunk beam.

## Metrics

- EvidenceRetentionRate
- RetainedChunksPerQuery
- RetainedRawWordsPerQuery
- evidence retained by direct local top-1
- evidence recovered by neighbor expansion

## Hypothesis

Borealis and Cirrus should both recover their evidence through neighbor expansion because their answer-bearing chunks are adjacent to the strongest local chunk.
