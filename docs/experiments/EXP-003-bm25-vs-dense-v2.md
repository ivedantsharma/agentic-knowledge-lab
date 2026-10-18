# EXP-003: KnowledgeBench v2 BM25 vs Dense

## Goal

Test whether BM25 and dense retrieval show complementary strengths under lexical, semantic, and distractor stress.

## Results

| Metric | BM25 | Dense |
|---|---:|---:|
| Answerable Recall@1 | 1.0000 | 0.8571 |
| Answerable Recall@3 | 1.0000 | 1.0000 |
| MRR | 1.0000 | 0.9286 |
| Unanswerable retrieval rate | 1.0000 | 1.0000 |

### Category Recall@1

| Category | BM25 | Dense |
|---|---:|---:|
| lexical_stress | 1.0000 | 0.6667 |
| semantic_stress | 1.0000 | 1.0000 |
| distractor_stress | 1.0000 | 1.0000 |

## Key failure

Dense retrieval failed rank 1 on:

```text
ERR-KV-4097
```

It ranked the near-match document containing:

```text
ERR-KV-4098
```

above the exact identifier match.

BM25 ranked the exact identifier first.

## Interpretation

v2 provides evidence that lexical retrieval adds value for opaque exact identifiers.

v1 previously showed a semantic paraphrase case where dense retrieval ranked the correct document first while BM25 ranked it second.

Across v1 and v2, the systems therefore show complementary failure modes:

- BM25 can be stronger for exact lexical identifiers.
- Dense retrieval can be stronger for semantic paraphrases.

This is sufficient evidence to justify testing a hybrid baseline.

It does not prove hybrid retrieval will be better. That must be measured.

## Next experiment

Use Reciprocal Rank Fusion (RRF) to combine BM25 and dense rankings without directly mixing incompatible score scales.
