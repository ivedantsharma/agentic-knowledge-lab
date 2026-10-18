# EXP-004: Hybrid RRF on KnowledgeBench v2

## Goal

Test whether equal-weight Reciprocal Rank Fusion (RRF) can combine BM25's exact-match strength with dense retrieval's semantic strength.

## Systems

- BM25
- Dense: all-MiniLM-L6-v2 + cosine similarity
- Hybrid: equal-weight RRF with rrf_k = 60

## Result

| Metric | BM25 | Dense | Hybrid RRF |
|---|---:|---:|---:|
| Answerable Recall@1 | 1.0000 | 0.8571 | 0.8571 |
| Answerable Recall@3 | 1.0000 | 1.0000 | 1.0000 |
| MRR | 1.0000 | 0.9286 | 0.9286 |
| Lexical stress Recall@1 | 1.0000 | 0.6667 | 0.6667 |
| Semantic stress Recall@1 | 1.0000 | 1.0000 | 1.0000 |
| Distractor stress Recall@1 | 1.0000 | 1.0000 | 1.0000 |
| Unanswerable retrieval rate | 1.0000 | 1.0000 | 1.0000 |

## Key failure case

For query:

```text
ERR-KV-4097
```

BM25 ranked:

1. doc_err_target
2. doc_err_near

Dense ranked:

1. doc_err_near
2. doc_err_target

Under equal-weight RRF:

```text
score(target) = 1/(60+1) + 1/(60+2)
score(near)   = 1/(60+2) + 1/(60+1)
```

The scores are exactly equal.

Our implementation then uses document ID as a deterministic secondary sort key, which places `doc_err_near` before `doc_err_target`.

## Interpretation

Equal-weight RRF did not resolve a direct rank disagreement between BM25 and dense.

This does **not** prove hybrid retrieval is ineffective.

It shows that this simple fusion rule cannot distinguish two documents when the component retrievers swap symmetric ranks.

Possible future approaches include:
- weighted RRF,
- calibrated score fusion,
- identifier-aware routing,
- learned fusion,
- reranking.

## Phase 1 decision

Do not tune fusion weights on the current tiny benchmark.

Doing so would risk optimizing directly to a handful of evaluation examples.

Keep equal-weight RRF as a documented baseline and revisit hybrid strategy in a later phase with a larger development set.
