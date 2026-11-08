# EXP-051 Result: Bidirectional Radius-1 Neighbor Expansion

## Aggregate

```text
EvidenceRetentionRate=1.0000
AvgRetainedSectionWords=95.33
AvgRadius1WindowWords=43.33
ReductionVsSections=0.5455
AvgChunksScored=13.67
```

## Comparison with EXP-050

```text
EXP-050
EvidenceRetentionRate=0.6667
ReductionVsSections=0.6434

EXP-051
EvidenceRetentionRate=1.0000
ReductionVsSections=0.5455
```

EXP-051 gives up some context reduction in exchange for full evidence retention.

## Cirrus repair

The radius-1 window now includes:

```text
"...A job that fails all retry attempts is moved
to the dead-letter queue named CIRRUS-DLQ..."
```

The forward neighbor that EXP-050 dropped is now preserved.

## Interpretation

The final local policy should not choose only the higher-scoring adjacent chunk.

A bounded bidirectional radius is more robust at chunk boundaries:

```text
previous + best chunk + next
```

when available.

## Phase 5 candidate policy

```text
dense parent routing
→ keep top 2 parents
→ cross-encoder section reranking
→ keep top 2 sections
→ overlapping local chunks
→ cross-encoder local chunk scoring
→ choose best chunk per section
→ expand radius 1
→ merge source ranges into deduplicated windows
```

This policy is now ready to move from experiment scripts into reusable retrieval code.
