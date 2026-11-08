# EXP-055: Entity Resolution Stress Test

## Research question

Does the lexical entity resolver behave correctly on aliases, overlapping names, and questions with no explicit registered surface?

## Why this experiment comes before semantic entity linking

EXP-054 used only explicit canonical names and achieved perfect accuracy.

Before adding embeddings or an LLM, we need to understand exactly where the deterministic resolver succeeds and where it should abstain.

## Stress categories

1. exact canonical name,
2. registered alias,
3. overlapping canonical name,
4. overlapping alias,
5. implicit entity,
6. unregistered paraphrase.

## Controlled change

The resolver implementation remains unchanged.

Only the graph entity surface inventory and evaluation questions become harder.

## Expected behavior

For explicit names and registered aliases:

```text
resolve correctly
```

For implicit or unregistered paraphrases:

```text
abstain
```

Abstention is considered correct in this experiment.

## Metrics

- OverallAccuracy
- ResolvableEntityAccuracy
- AbstentionAccuracy
- FalsePositiveResolutionRate

## Why false-positive resolution matters

A wrong entity link can send the entire downstream graph traversal down the wrong path.

For graph systems, a calibrated abstention can therefore be safer than a confident guess.
