# EXP-046 Result: Chunk Overlap Repair

## Aggregate

```text
EvidenceFragmentationCount=0
ChunkRecall@1=0.3333
ChunkRecall@2=0.6667
ChunkEvidenceRetentionRate=0.6667
AvgChunksScored=3.33
AvgRetainedRawChunkWords=14.67
```

## What overlap fixed

In EXP-045, the Borealis evidence phrase:

```text
every six hours
```

was split across a zero-overlap chunk boundary.

With a 3-word overlap, a chunk now contains:

```text
backups run every six hours.
```

So:

```text
EvidenceFragmentationCount: 1 → 0
```

This validates overlap as a boundary-robustness mechanism.

## What overlap did not fix

Cirrus still fails evidence retention.

The relevant chunk exists but ranks fourth globally.

Two chunks from the same hard distractor section occupy the retained top-2 slots.

Therefore the remaining problem is no longer fragmentation.

It is candidate concentration during chunk ranking.

## Conclusion

Overlap repairs missing evidence spans, but overlap also creates more nearby/redundant chunk candidates.

The next diagnostic should examine chunk ranking by parent section before changing the scoring model.