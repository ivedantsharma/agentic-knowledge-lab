# EXP-079 Result: Deterministic Evidence-Path Grading

## Validation

```text
222 tests passed
ruff passed
```

## Rule-based planner

The four known-intent tasks followed the exact annotated evidence path.

The OOD task failed before search.

Aggregate:

```text
MeanPathCoverage=0.8000
OrderedPathCompleteRate=0.8000
ExactPathMatchRate=0.8000
AverageExtraDocuments=0.0000
```

## Semantic planner

All five tasks followed the exact annotated evidence path:

```text
MeanPathCoverage=1.0000
OrderedPathCompleteRate=1.0000
ExactPathMatchRate=1.0000
AverageExtraDocuments=0.0000
```

## Critical OOD result

For `ood-001`, the semantic planner had:

```text
ExactPathMatch=True
```

while EXP-078 showed:

```text
RelationAligned=False
AnswerCorrect=False
```

## Main conclusion

Perfect evidence-path execution does not imply correct answer selection.

The evaluation stack now distinguishes:

```text
path quality
from
relation selection
from
final answer correctness
```

This provides a clean basis for evaluating model-based graders in EXP-080.
