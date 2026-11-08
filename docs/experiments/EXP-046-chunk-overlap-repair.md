# EXP-046: Chunk Overlap Repair

## Research question

Can overlap repair the Borealis boundary-fragmentation failure without changing the rest of the hierarchy?

## Controlled variables

Keep fixed:

- parent beam = 2
- section beam = 2
- chunk size = 10 words
- chunk beam = 2
- MiniLM parent routing
- cross-encoder section and chunk scoring
- corpus
- tasks.

Change only:

```text
chunk overlap: 0 → 3 words
```

## Hypothesis

A 3-word overlap should create at least one Borealis chunk containing:

```text
every six hours
```

and restore chunk-level evidence retention.

## Metrics

- evidence fragmentation count
- ChunkRecall@1
- ChunkRecall@2
- ChunkEvidenceRetentionRate
- AvgChunksScored
- AvgRetainedChunkWords.

## Tradeoff

Overlap can improve boundary robustness but increases redundancy and candidate count.