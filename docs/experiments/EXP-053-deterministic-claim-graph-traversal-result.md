# EXP-053 Result: Deterministic Claim-Graph Traversal

## Aggregate

```text
tasks=4
AnswerAccuracy=1.0000
PathAccuracy=1.0000
ProvenanceCoverage=1.0000
```

## Interpretation

The oracle graph baseline succeeds on all four Phase 3-derived tasks.

This validates:

- entity/claim schema integrity,
- deterministic relation traversal,
- entity-valued intermediate hops,
- literal-valued final hops,
- claim-level evidence propagation.

## What this does not prove

The experiment supplies both:

- the correct start entity,
- the correct relation path.

Therefore it does not yet test natural-language graph access.

The next experiment removes only the gold start-entity assumption while keeping the relation path fixed.
