# EXP-011: Cirrus Similarity Failure Analysis

## Query

```text
Where are Cirrus jobs sent after exhausting all retries?
```

## Rich contextual chunk scores

| Rank | Section | Cosine score |
|---|---|---:|
| 1 | Retry Policy | 0.665840 |
| 2 | Dead Letter Handling | 0.633207 |
| 3 | Queue Overview | 0.570137 |
| 4 | Observability | 0.416852 |

## Gap

Top-1 minus relevant top-2:

```text
0.665840 - 0.633207 = 0.032633
```

The relevant chunk is close to the top result.

## Interpretation

The retriever has found the correct semantic neighborhood.

The main failure is candidate ordering rather than candidate recall.

That makes retrieve-then-rerank a justified next experiment.

## Decision

Test a cross-encoder reranker over dense top-3 candidates before changing embedding models or adding more contextual prose.
