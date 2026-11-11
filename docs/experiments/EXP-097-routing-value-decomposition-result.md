# EXP-097 Result: Paired Benchmark Routing Value Decomposition

## Validation

```text
249 tests passed
ruff passed
```

## Fixed strategies

```text
BM25 MRR=0.8194
Dense MRR=0.7778
Hybrid RRF MRR=0.8333
```

## Oracle

```text
oracle_mrr=0.8750
best_fixed_strategy=hybrid_rrf
best_fixed_mrr=0.8333
absolute_headroom=0.0417
relative_headroom=0.0500
unique_winner_counts={'bm25': 1}
tied_tasks=11
```

## Interpretation

The routing ceiling above always-Hybrid is small.

Only one of twelve tasks has a unique winner.

Eleven of twelve tasks have tied best strategies.

Therefore the benchmark provides insufficient evidence for a sophisticated retriever-selection router.

## Decision

Do not train or hand-design a complex BM25-vs-Dense-vs-Hybrid router from this dataset.

Move to another Phase 10 adaptation axis:

```text
adaptive retrieval budget
```

The next question is:

> How many candidates should each query retrieve?

This is directly connected to context cost, latency, and adversarial/distractor exposure.
