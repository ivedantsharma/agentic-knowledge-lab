# EXP-045: Document → Section → Chunk Baseline

## Research question

Can a three-level hierarchy preserve answer-bearing evidence while reducing the final context passed downstream?

## Retrieval policy

```text
query
→ dense parent ranking
→ keep top 2 parents
→ cross-encoder rerank pooled sections
→ keep top 2 sections
→ split retained sections into 10-word chunks
→ cross-encoder rerank chunks
→ keep top 2 chunks
```

## Why this differs from Phase 2

Phase 2 searched chunks globally.

Phase 5 searches chunks only after document and section routing have narrowed the search space.

## Controlled settings

- parent beam = 2
- section beam = 2
- chunk size = 10 words
- chunk overlap = 0
- chunk beam = 2
- MiniLM for parent routing
- cross-encoder for section and chunk reranking

## Metrics

- ParentRecall@2
- SectionEvidenceRetentionRate
- ChunkRecall@1
- ChunkRecall@2
- ChunkEvidenceRetentionRate
- AvgSectionContextWords
- AvgRetainedChunkWords
- AvgChunksScored

## Hypothesis

The three-level hierarchy should preserve all evidence while reducing the amount of text retained after section selection.

## Limitation

This is still a tiny synthetic mechanism test. Chunk size and overlap are fixed rather than tuned.
