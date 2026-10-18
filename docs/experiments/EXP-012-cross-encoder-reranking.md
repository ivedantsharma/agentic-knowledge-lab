# EXP-012: Cross-Encoder Reranking

## Goal

Test whether a second-stage cross-encoder can correct dense ranking errors when the correct chunk is already present in the candidate set.

## Pipeline

```text
dense retrieval
↓ top 3
cross-encoder reranker
↓
final ranking
```

Dense model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Reranker:

```text
cross-encoder/ms-marco-MiniLM-L6-v2
```

## Results

| Metric | Dense | Dense + reranker |
|---|---:|---:|
| Hit@1 | 0.6667 | 1.0000 |
| Recall@1 | 0.6667 | 1.0000 |
| Recall@3 | 1.0000 | 1.0000 |
| MRR | 0.8333 | 1.0000 |

## Cirrus failure correction

Dense ranking:

1. Retry Policy
2. Dead Letter Handling
3. Queue Overview

Cross-encoder scores:

```text
Retry Policy        1.777717
Dead Letter         4.062158
Queue Overview     -1.263042
```

Reranked:

1. Dead Letter Handling
2. Retry Policy
3. Queue Overview

The reranker correctly identified the answer-bearing chunk as the best match.

## Interpretation

The dense retriever already had sufficient recall.

The main issue was final candidate ordering.

A cross-encoder was effective because it scored the query and candidate passage jointly.

This supports a two-stage architecture:

```text
fast retriever for recall
+
slower reranker for precision
```

## Important limitation

This result is based on a tiny synthetic benchmark.

It demonstrates mechanism and failure correction, not general production superiority.

## Phase 2 implication

Reranking is justified when:
- the relevant chunk is already in top-k,
- candidate scores are close,
- first-stage ordering is the main failure.

Do not use reranking as a substitute for poor first-stage recall.
