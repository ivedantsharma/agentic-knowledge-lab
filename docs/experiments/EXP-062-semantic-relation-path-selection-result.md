# EXP-062 Result: Semantic Relation-Path Selection

## Aggregate

```text
tasks=4
PathSelectionAccuracy=1.0000
AnswerAccuracy=1.0000
AvgCandidatePaths=2.00
```

## Per-task observation

The correct path ranked first for all four tasks.

The most difficult case was Atlas:

```text
correct:
operated_by
→ maintains_storage_system
→ incremental_backup_cadence
score=0.782214

near distractor:
operated_by
→ maintains_legacy_storage_system
→ incremental_backup_cadence
score=0.755725
```

The margin was approximately 0.026489.

## Interpretation

Explicit graph structure successfully constrained search to valid routes, and semantic ranking selected the intended route on this synthetic branching graph.

The small Atlas margin is an important warning: perfect top-1 accuracy does not imply strong separation from near-distractor paths.

## Limitation

The start entity remained gold in EXP-062. EXP-063 removes that assumption for explicit entity mentions by composing lexical entity resolution with path search.
