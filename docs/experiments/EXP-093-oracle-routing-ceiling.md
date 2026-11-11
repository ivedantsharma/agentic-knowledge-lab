# EXP-093: Fixed Retriever Comparison and Oracle Routing Ceiling

## Research question

Is there enough per-query variation among BM25, Dense, and Hybrid retrieval to justify adaptive routing?

## Controlled setup

Dataset:

```text
KnowledgeBench v2 hard v0
```

Candidate strategies:

- BM25,
- Dense MiniLM,
- equal-weight RRF hybrid.

Fixed:

```text
top_k=3
Dense model=sentence-transformers/all-MiniLM-L6-v2
RRF k=60
```

Only answerable tasks are used for the initial routing ceiling.

## Why answerable-only?

Fixed top-k retrievers always return candidates.

Unanswerable and ambiguity tasks require a different decision space:

- search,
- clarify,
- abstain.

They should not be forced into a BM25-vs-Dense winner label.

## Metrics

For each strategy:

- mean Supporting Recall@3,
- mean Reciprocal Rank,
- mean Evidence-Chain Coverage.

For each task:

- retrieved IDs,
- Supporting Recall@3,
- Reciprocal Rank.

## Oracle

Per task:

1. maximize Supporting Recall@3,
2. break ties with Reciprocal Rank.

Ties remain ties.

Report:

- mean oracle supporting recall,
- mean oracle reciprocal rank,
- unique winner counts,
- number of tied tasks.

## Interpretation

### If oracle ≈ best fixed retriever

There is little evidence that routing is useful on this benchmark.

### If oracle > every fixed retriever

There is measurable routing headroom.

### If different strategies uniquely win different tasks

The benchmark supports learning a query-to-retriever mapping.

No routing policy is introduced yet.
