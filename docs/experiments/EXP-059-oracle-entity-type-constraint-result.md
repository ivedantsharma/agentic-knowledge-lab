# EXP-059 Result: Oracle Entity-Type Constrained Semantic Ranking

## Aggregate

```text
Threshold=0.39
UnconstrainedResolvableAccuracy=0.5000
TypedResolvableAccuracy=1.0000
TypedAbstentionAccuracy=1.0000
TypedFalsePositiveResolutionRate=0.0000
```

## Main result

Adding a gold entity-type constraint repaired both confident wrong-node failures from EXP-058.

```text
"group that runs the Atlas authentication service"
unrestricted -> atlas (service)
typed(team)  -> platform_reliability

"team that maintains the production session-metadata cache"
unrestricted -> solstice (service)
typed(team)  -> identity_foundations
```

## Interpretation

The semantic ranker was retrieving strongly related graph neighbors but sometimes assigning the wrong semantic role.

Entity type provides a useful symbolic constraint:

```text
mention semantics
+ entity type compatibility
+ semantic ranking
+ confidence threshold
```

performed better than unconstrained semantic ranking on this held-out set.

## Caveat

The entity type was oracle-provided.

EXP-059 therefore justifies building and evaluating a type inference component; it does not prove automatic type inference works.
