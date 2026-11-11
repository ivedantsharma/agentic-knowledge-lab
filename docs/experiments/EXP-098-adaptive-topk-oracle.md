# EXP-098: Adaptive Top-K Budget Oracle

## Research question

How much candidate budget does each query actually need?

## Trigger from EXP-097

Retriever-selection headroom was only:

```text
+0.0417 MRR
```

with 11/12 tasks tied.

Therefore the next adaptation axis is retrieval budget rather than retriever identity.

## Why top-k matters

Larger k can improve evidence coverage, but it also increases:

- context length,
- reranking cost,
- latency,
- distractor exposure,
- stale/contradictory evidence exposure.

So:

```text
more retrieval
!=
always better system behavior
```

## Controlled setup

Use the strongest broadly stable fixed strategy:

```text
Hybrid RRF
```

Evaluate answerable KnowledgeBench v2 hard-v0 tasks.

Candidate budgets:

```text
k ∈ {1, 2, 3, 5}
```

## Oracle definition

For each task:

1. compute Supporting Recall@k for every candidate k,
2. identify the maximum recall reachable in this budget range,
3. choose the smallest k that reaches that maximum.

This gives:

```text
minimal_k_for_max_recall
```

## Metrics

Per task:

- number of supporting documents,
- Recall@1,
- Recall@2,
- Recall@3,
- Recall@5,
- minimal k for maximum observed recall.

Aggregate:

- mean minimal k,
- maximum required k,
- mean recall for each fixed k.

## What this proves

If tasks require substantially different k values, adaptive budget selection has real headroom.

If nearly every task needs the same k, dynamic top-k is unnecessary on this benchmark.

## Limitation

This is an oracle budget analysis.

It does not yet predict k from the query.
