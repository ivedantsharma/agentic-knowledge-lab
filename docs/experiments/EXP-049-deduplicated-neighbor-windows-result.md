# EXP-049 Result: Deduplicated Neighbor Windows

## Aggregate

```text
EvidenceRetentionRate=1.0000
AvgNaiveRetainedRawWords=27.33
AvgDeduplicatedWindowWords=23.33
AvgRetainedSectionWords=23.33
ReductionVsNaive=0.1463
ReductionVsSections=0.0000
```

## What worked

Deduplication removed overlap redundancy:

```text
27.33 → 23.33 words/query
```

This is a 14.63% reduction relative to naively returning overlapping chunks.

Evidence retention remains perfect:

```text
EvidenceRetentionRate=1.0000
```

## What did not improve

The deduplicated windows are exactly as large as the retained full sections:

```text
AvgDeduplicatedWindowWords=23.33
AvgRetainedSectionWords=23.33
```

Therefore the chunk level does not yet reduce context below section retrieval on this corpus.

## Why

The benchmark sections are very short.

For Atlas, Borealis, and Cirrus, the selected top chunk plus its neighbor spans the entire relevant section.

So merging adjacent ranges reconstructs the full section.

## Conclusion

EXP-049 validates deduplication but does not validate context savings versus section retrieval.

The next experiment must use longer sections where a local chunk window can be substantially smaller than the full section.
