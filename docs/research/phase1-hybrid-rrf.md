# Phase 1 — Hybrid Retrieval with Reciprocal Rank Fusion

## Why not add BM25 and cosine scores directly?

BM25 and cosine similarity have different numerical meanings and ranges.

Example:

```text
BM25 score: 7.4
cosine score: 0.63
```

Adding them directly would make the larger numerical scale dominate even if that scale is not more important.

## Reciprocal Rank Fusion

RRF combines rankings rather than raw scores.

For a document d:

```text
RRF(d) = sum(1 / (rrf_k + rank_i(d)))
```

where each rank_i is the document's rank in one retriever.

A document ranked highly by both systems receives contributions from both.

A document ranked highly by only one system can still survive.

We use the conventional smoothing constant:

```text
rrf_k = 60
```

For our tiny benchmark the exact value is not being tuned.

That is intentional: tuning on these evaluation tasks would blur baseline comparison with benchmark optimization.

## Example

BM25:

```text
1. A
2. B
3. C
```

Dense:

```text
1. B
2. D
3. A
```

RRF gives:

- A credit from BM25 rank 1 and dense rank 3
- B credit from BM25 rank 2 and dense rank 1

Documents supported by both rankings tend to rise.

## Research question

Does simple rank fusion preserve BM25's exact-match strength while retaining dense retrieval's semantic strength?
