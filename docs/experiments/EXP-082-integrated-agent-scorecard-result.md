# EXP-082 Result: Integrated Agent Evaluation Scorecard

## Validation

```text
222 tests passed
ruff passed
```

## Rule-based planner

```text
answer_correct_rate=0.8000
full_evidence_rate=0.8000
ordered_path_rate=0.8000
exact_path_rate=0.8000
grounded_rate=0.8000
relation_aligned_rate=0.8000
efficient_rate=1.0000
premature_stop_rate=0.0000
planner_failure_rate=0.2000
```

The OOD task failed before search.

Therefore its dominant failure is planner capability.

## Semantic planner

```text
answer_correct_rate=0.8000
full_evidence_rate=1.0000
ordered_path_rate=1.0000
exact_path_rate=1.0000
grounded_rate=1.0000
relation_aligned_rate=0.8000
efficient_rate=1.0000
premature_stop_rate=0.0000
planner_failure_rate=0.0000
```

The OOD task had:

```text
FullEvidence=True
OrderedPathComplete=True
ExactPathMatch=True
AnswerGrounded=True
RelationAligned=False
AnswerCorrect=False
```

## Main comparison

Both planners have:

```text
AnswerCorrectRate=0.8000
```

but their failures are different.

Rule-based:

```text
cannot form initial query
→ no retrieval
→ no evidence
```

Semantic:

```text
correct query path
→ full evidence
→ grounded answer
→ wrong relation selection
```

## Conclusion

The integrated scorecard successfully decomposes agent failure into interpretable stages.

A single answer-accuracy number would hide this distinction.

This validates the Phase 8 layered evaluation architecture.
