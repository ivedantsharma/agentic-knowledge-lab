# EXP-049: Deduplicated Neighbor Windows

## Research question

Can we keep the recall benefit of overlapping neighbor expansion while removing duplicated context?

## Fixed components

- parent beam = 2
- section beam = 2
- chunk size = 10 words
- chunk overlap = 3
- local cross-encoder chunk ranking
- best local chunk + best adjacent neighbor
- same corpus and tasks

## Treatment

For each retained section:

1. choose the best local chunk;
2. choose its best immediate neighbor;
3. merge their source word ranges;
4. reconstruct one deduplicated local window.

## Metrics

- EvidenceRetentionRate
- AvgNaiveRetainedRawWords
- AvgDeduplicatedWindowWords
- AvgRetainedSectionWords
- context reduction versus naive chunks
- context reduction versus full retained sections

## Hypothesis

Evidence retention should remain 1.0 while deduplicated windows use fewer words than naive overlapping chunk concatenation.
