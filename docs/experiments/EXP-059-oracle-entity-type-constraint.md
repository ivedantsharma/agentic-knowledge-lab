# EXP-059: Oracle Entity-Type Constrained Semantic Ranking

## Research question

Does constraining semantic candidates to the intended entity type repair the confident wrong-entity failures from EXP-058 without breaking abstention?

## Controlled change

Keep fixed:

- mention spans,
- MiniLM,
- entity profiles,
- cosine similarity,
- threshold = 0.39,
- held-out task concepts.

Change only:

    all graph entities
    -> entities matching the gold entity type

## Oracle caveat

The expected entity type is supplied directly. This does not solve type inference. It diagnoses whether type compatibility is sufficient to repair ranking.

## Metrics

- UnconstrainedResolvableAccuracy
- TypedResolvableAccuracy
- TypedAbstentionAccuracy
- TypedFalsePositiveResolutionRate
