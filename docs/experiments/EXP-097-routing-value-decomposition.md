# EXP-097: Paired Benchmark Routing Value Decomposition

## Research question

How much MRR headroom remains above the strongest fixed retriever on the expanded paired routing benchmark?

## Trigger from EXP-096

EXP-096 showed:

```text
winner shifts in 4 / 6 query pairs
```

but also:

```text
Hybrid MRR=0.8333
```

for both lexical-explicit and semantic-paraphrase styles.

Therefore query style alone cannot justify a useful router.

## Goal

Separate two questions:

1. Does query wording affect retriever winners?
2. Is there enough per-query value above always-Hybrid to justify a more expressive router?

EXP-096 answered the first.

EXP-097 measures the second.

## Metric

Because all retrievers achieved Recall@3=1.0 on the paired benchmark, the routing objective is:

```text
Reciprocal Rank
```

The oracle selects the highest-RR retriever for each task.

## Report

- MRR for every fixed strategy,
- oracle MRR,
- absolute headroom,
- relative headroom,
- unique winner counts,
- tied-task count,
- per-task winner sets.

## Interpretation

If oracle MRR is only marginally above always-Hybrid, a sophisticated router is unlikely to be justified on this dataset.

If the gap is meaningful, the next step is to design a router using richer query/retrieval representations.

## Important constraint

The oracle is diagnostic only.

It uses observed task outcomes and is not available at inference time.
