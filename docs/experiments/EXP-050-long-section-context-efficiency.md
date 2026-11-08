# EXP-050: Long-Section Context-Efficiency Stress Test

## Research question

Can the three-level hierarchy preserve evidence while reducing final context when sections are long enough for local windows to matter?

## Motivation

EXP-049 achieved:

```text
EvidenceRetentionRate=1.0000
```

but no context reduction versus full sections because the benchmark sections were too short.

## New corpus property

Create longer versions of the relevant sections with:

- the same answer-bearing facts,
- additional unrelated sentences before and after,
- enough length that a local chunk window is materially smaller than the section.

## Keep fixed

- parent beam = 2
- section beam = 2
- chunk size = 10
- overlap = 3
- section-aware local chunk ranking
- neighbor expansion
- deduplicated source windows
- same embedding and cross-encoder models.

## Metrics

- EvidenceRetentionRate
- AvgRetainedSectionWords
- AvgDeduplicatedWindowWords
- ReductionVsSections
- AvgChunksScored

## Hypothesis

Evidence retention should remain high while local windows become smaller than full retained sections.
