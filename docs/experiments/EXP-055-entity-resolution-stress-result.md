# EXP-055 Result: Entity Resolution Stress Test

## Aggregate

```text
tasks=6
OverallAccuracy=1.0000
ResolvableEntityAccuracy=1.0000
AbstentionAccuracy=1.0000
FalsePositiveResolutionRate=0.0000
```

## Interpretation

The lexical resolver behaves correctly across:

- canonical names,
- registered aliases,
- overlapping entity names,
- overlapping aliases,
- implicit references,
- unregistered paraphrases.

The important result is not only successful resolution.

It is also correct abstention.

## Positive cases

```text
Atlas
→ atlas

PR Team
→ platform_reliability

Atlas Analytics
→ atlas_analytics

Atlas BI
→ atlas_analytics
```

## Abstention cases

```text
"customer-profile storage platform"
→ no lexical entity

"infrastructure reliability group"
→ no lexical entity
```

These abstentions are correct for a lexical-only resolver.

## Research conclusion

The deterministic resolver has a clean capability boundary:

```text
registered explicit surface → resolve
no registered explicit surface → abstain
```

The next experiment should test whether a semantic resolver can rank the intended entity highly for implicit references without immediately turning semantic similarity into an unconditional guess.
