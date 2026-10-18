# EXP-002: BM25 vs Dense Retrieval on KnowledgeBench v1

## Question

Do BM25 and dense retrieval exhibit different strengths on lexical, semantic, and distractor tasks?

## Systems

### BM25
Custom Phase 1 BM25 implementation.

### Dense
`sentence-transformers/all-MiniLM-L6-v2` with cosine similarity.

## Controlled variables

- Same 8 benchmark tasks
- Same 10-document corpus
- Same relevance judgments
- Same top_k = 3
- Same evaluator
- Same task categories

## Results

### Aggregate

| Metric | BM25 | Dense |
|---|---:|---:|
| Recall@3 | 1.0000 | 1.0000 |
| Precision@3 | 0.3333 | 0.3333 |
| MRR | 0.9286 | 1.0000 |
| Unanswerable retrieval rate | 1.0000 | 1.0000 |

## Rank-level observations

### Lexical tasks

Both BM25 and dense ranked the relevant document first for all three lexical tasks:

- ERR_CONNECTION_REFUSED
- RFC 7231 Section 4.3
- CUBLAS_STATUS_ALLOC_FAILED

The current lexical tasks therefore do not distinguish the two retrievers.

### Semantic tasks

For:

```text
How do I stop one Python project's libraries from interfering with another project's libraries?
```

BM25 ranked the correct document second.

Dense ranked it first.

For the reinforcement-learning paraphrase, both ranked the correct document first.

### Distractor tasks

Both systems ranked the relevant document first on both distractor tasks.

### Unanswerable task

Both systems returned three documents even though no relevant document existed.

This is expected for fixed top-k retrieval without abstention.

## Interpretation

The experiment does **not** yet justify a hybrid retriever.

It provides limited evidence that dense retrieval is stronger on at least one semantic paraphrase task.

It does not provide evidence that BM25 is stronger on lexical tasks because dense also ranked all lexical targets first.

The benchmark is still too easy at Recall@3.

MRR exposed one difference because it is sensitive to ranking position.

## Next experiment

Evaluate:
- Recall@1
- category-level metrics

Then create harder lexical cases where:
- exact identifiers are arbitrary or opaque,
- semantic similarity provides little useful signal,
- distractor documents are semantically similar but lack the exact identifier.

This should better test the hypothesis that BM25 has an advantage on exact lexical retrieval.
