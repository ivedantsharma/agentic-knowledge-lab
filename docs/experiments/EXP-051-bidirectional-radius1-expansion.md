# EXP-051: Bidirectional Radius-1 Neighbor Expansion

## Research question

Can retaining both immediate neighbors around the best local chunk recover the Cirrus evidence while preserving most of the context reduction from EXP-050?

## Fixed components

- long-section corpus
- parent beam = 2
- section beam = 2
- chunk size = 10 words
- overlap = 3 words
- same MiniLM parent retriever
- same cross-encoder
- same deduplicated source-window reconstruction

## Change

EXP-050:

```text
top chunk + best one adjacent neighbor
```

EXP-051:

```text
previous neighbor + top chunk + next neighbor
```

when those neighbors exist.

## Metrics

- EvidenceRetentionRate
- AvgRetainedSectionWords
- AvgRadius1WindowWords
- ReductionVsSections
- additional words versus EXP-050
- AvgChunksScored

## Hypothesis

Cirrus should recover because the forward neighbor containing CIRRUS-DLQ will remain in the local window.

Context should increase relative to EXP-050, but remain substantially smaller than full retained sections.
