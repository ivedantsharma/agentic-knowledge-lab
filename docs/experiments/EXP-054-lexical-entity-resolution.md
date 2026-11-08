# EXP-054: Lexical Entity Resolution + Gold Relation Path

## Research question

Can the system identify the graph start entity directly from the natural-language question without being given its entity ID?

## Controlled change

EXP-053:

```text
gold start entity
+ gold relation path
```

EXP-054:

```text
lexically resolved start entity
+ gold relation path
```

The graph, claims, traversal logic, tasks, and relation paths remain unchanged.

## Baseline resolver

The resolver uses normalized entity names and aliases.

Example:

```text
question:
"What backup cadence is used ... team that operates Atlas?"

entity surface:
"Atlas"

resolved entity:
atlas
```

This is intentionally not an embedding or LLM resolver.

Exact lexical mentions should be handled by deterministic software first.

## Metrics

- EntityLinkAccuracy
- EntityResolutionFailureRate
- AnswerAccuracy
- PathAccuracy
- ProvenanceCoverage

## Hypothesis

The current four tasks should resolve perfectly because each question explicitly contains the intended start entity name.

## Limitation

Success on these tasks only establishes an exact/alias entity-linking baseline.

It does not test:

- paraphrased entity mentions,
- abbreviations not registered as aliases,
- misspellings,
- multiple competing entity mentions,
- implicit entities.
