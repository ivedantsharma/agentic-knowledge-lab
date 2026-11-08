# Phase 5 — Recall–Context Tradeoff

## EXP-050

Long sections finally expose the intended benefit of hierarchical chunk retrieval.

```text
ReductionVsSections=0.6434
```

But the smaller context window loses one answer.

This demonstrates that context compression is not free.

## Directional boundary failure

The current policy selects only one adjacent chunk:

```text
top chunk
+ max(previous_score, next_score)
```

This assumes the higher-scoring neighbor contains the useful continuation.

That assumption can fail when:

- the query-matching clue is in the top chunk,
- the exact answer is in the lower-scoring forward chunk,
- the backward chunk is semantically similar and scores higher.

## Radius-based expansion

A more robust local policy is:

```text
previous + top + next
```

when both neighbors exist.

This is still local and bounded.

It trades a small amount of additional context for greater boundary robustness.

## Research objective

We should measure the Pareto frontier:

```text
evidence retention
vs
returned context size
```

rather than optimizing either metric in isolation.
