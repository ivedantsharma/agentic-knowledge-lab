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

## Interpretation

Deduplication removes the redundancy introduced by overlapping chunks.

```text
27.33 words → 23.33 words
```

This is a 14.63% reduction versus naive concatenation.

Evidence retention remains perfect.

## Important negative result

The deduplicated local windows are exactly the same average size as the retained full sections.

Therefore, on the current short synthetic sections, chunk-level neighbor expansion provides no context-size advantage over returning the full retained sections.

## Why

The source sections are themselves only about 8–15 words each.

Once the best chunk and its neighbor are merged, their union covers the full section.

## Conclusion

The mechanism is correct, but the benchmark is too small to test the intended context-efficiency benefit of document → section → chunk retrieval.

The next experiment should use longer sections containing multiple facts and localized answer spans.
