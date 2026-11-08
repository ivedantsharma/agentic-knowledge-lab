# EXP-048 Result: Section-Aware Neighbor Expansion

## Aggregate

```text
DirectLocalTop1EvidenceRate=0.3333
NeighborRecoveryRate=0.6667
EvidenceRetentionRate=1.0000
AvgRetainedChunksPerQuery=3.33
AvgRetainedRawWordsPerQuery=27.33
```

## Interpretation

Neighbor expansion restores all answer-bearing evidence.

Atlas is solved directly by the best local chunk.

Borealis and Cirrus require the adjacent chunk:

```text
Borealis:
top local chunk = setup / cadence clue
neighbor        = "backups run every six hours."

Cirrus:
top local chunk = retry-exhaustion transition
neighbor        = "... dead-letter queue named CIRRUS-DLQ."
```

## Success

```text
EvidenceRetentionRate: 0.6667 → 1.0000
```

The repair is structural rather than benchmark-specific top-k expansion.

## New cost problem

The retained raw chunk text averages:

```text
27.33 words/query
```

whereas the earlier two retained full sections averaged:

```text
23.33 words/query
```

This happens because overlapping neighboring chunks duplicate words.

Therefore evidence retention is solved, but context efficiency is not.

## Next step

Merge adjacent overlapping chunks into one deduplicated local window per retained section and compare context size while preserving evidence.
