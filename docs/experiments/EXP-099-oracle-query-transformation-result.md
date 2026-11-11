# EXP-099 Result: Oracle Query Transformation Upper Bound

## Validation

```text
253 tests passed
ruff passed
```

## Per-task result

### kbv2-hard-001

```text
single-shot recall=1.0000
transformed recall=0.6667
single budget=5
transformed budget=3
```

The transformed chain retrieved:

- Atlas ownership,
- Borealis current,

but missed the Platform Reliability → Borealis bridge document.

### kbv2-hard-005

```text
single-shot recall=0.3333
transformed recall=0.6667
single budget=5
transformed budget=3
```

The transformation recovered:

- Helios ownership,
- Identity Foundations → Solstice,

but the final transformed query retrieved stale Solstice policy instead of the current policy.

### kbv2-hard-006

```text
single-shot recall=1.0000
transformed recall=1.0000
single budget=5
transformed budget=2
```

The focused transformation preserved full recall with lower budget.

## Aggregate

```text
single_shot_mean_recall=0.7778
transformed_mean_recall=0.7778
mean_single_budget=5.0000
mean_transformed_budget=2.6667
```

## Interpretation

Oracle decomposition did not improve aggregate recall.

However, it did improve the saturated Helios task from:

```text
0.3333 → 0.6667
```

while using fewer retrieved candidates.

This shows decomposition can expose missing intermediate evidence, but decomposition alone is insufficient.

## New failure mode

The transformed queries can lose or weaken qualifiers such as:

- current,
- production,
- relation context.

This can cause:

- wrong intermediate retrieval,
- stale-document selection.

## Decision

The next controlled experiment should preserve task qualifiers explicitly across transformed queries.

The variable under study is:

```text
query decomposition
vs
query decomposition + qualifier preservation
```

with retriever, corpus, and per-query budget fixed.
