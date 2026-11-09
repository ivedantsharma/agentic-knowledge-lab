# EXP-077 Result: Groundedness Is Not Task Correctness

## Rule-based planner

Four stopped known-intent tasks were both correct and grounded.

The OOD task did not run because the rule planner could not form an initial query.

```text
stopped_count=4
grounded_stop_rate=1.0000
grounded_but_wrong_rate=0.0000
```

## Semantic planner

Known-intent tasks were correct and grounded.

For `ood-001`:

```text
EvidenceCoverage=1.0000
AnswerCorrect=False
AnswerGrounded=True
GroundedButWrong=True
GroundingDocuments=['manual_cirrus']
```

Aggregate:

```text
stopped_count=5
grounded_stop_rate=1.0000
grounded_but_wrong_rate=0.2000
```

## Main conclusion

A 100% grounded-stop rate can coexist with wrong answers.

The semantic planner retrieved and consumed the correct Cirrus manual, then selected a real but relation-misaligned fact from it.

Therefore:

```text
grounded
!=
correct
```

and document-level groundedness is not sufficient for evaluating agent answer quality.

EXP-078 adds a deterministic relation-alignment grader using the existing final-hop extraction patterns.
