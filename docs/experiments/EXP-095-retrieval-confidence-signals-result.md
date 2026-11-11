# EXP-095 Result: Retrieval Confidence Signal Diagnostic

## Validation

```text
245 tests passed
ruff passed
```

## Main finding

Ranking-confidence signals did not cleanly separate unique retriever winners.

### Dense-only winner: hard-001

```text
BM25 margin=3.1678
Dense margin=0.0084
top1 agreement=False
top3 Jaccard=0.2000
```

### BM25-only winner: hard-005

```text
BM25 margin=3.1678
Dense margin=0.0068
top1 agreement=False
top3 Jaccard=0.2000
```

These signatures are nearly identical despite opposite winner labels.

## Other observations

hard-002 is a BM25-only winner even though BM25 and Dense agree on top-1.

hard-010 favors Dense/Hybrid despite BM25 having a large top-1 margin.

Therefore:

```text
large margin
!=
correct retriever confidence
```

and:

```text
retriever disagreement
!=
which retriever is right
```

## Decision

Do not build a confidence-rule router from this six-task sample.

Expand the routing benchmark with controlled paired query variants before introducing a policy.
