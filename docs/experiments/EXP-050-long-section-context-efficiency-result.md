# EXP-050 Result: Long-Section Context-Efficiency Stress Test

## Aggregate

```text
EvidenceRetentionRate=0.6667
AvgRetainedSectionWords=95.33
AvgDeduplicatedWindowWords=34.00
ReductionVsSections=0.6434
AvgChunksScored=13.67
```

## Success

The three-level hierarchy materially reduces downstream context:

```text
95.33 words/query
→ 34.00 words/query
```

which is a 64.34% reduction.

This validates the intended context-localization benefit of the chunk level on longer sections.

## Recall regression

Evidence retention falls to 0.6667.

Atlas and Borealis retain the target evidence.

Cirrus fails.

The retained Cirrus window ends at:

```text
"...A job that fails all retry attempts is moved"
```

while the answer-bearing destination appears immediately after that span in the source section.

## Diagnosis

The current local policy keeps:

```text
best chunk
+ best-scoring one of its immediate neighbors
```

That can choose the wrong direction at a boundary.

The failure is therefore not evidence fragmentation and not upper-level routing.

It is directional neighbor selection.

## Next step

Test a radius-1 local window:

```text
previous neighbor
+ best chunk
+ next neighbor
```

when available.

Then compare evidence retention against the additional context cost.
