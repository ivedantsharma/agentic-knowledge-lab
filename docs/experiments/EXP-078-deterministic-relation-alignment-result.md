# EXP-078 Result: Deterministic Relation-Alignment Grader

## Validation

```text
218 tests passed
ruff passed
```

## Rule-based planner

All four stopped known-intent tasks were:

```text
answer_correct=True
answer_grounded=True
final_evidence_consumed=True
relation_aligned=True
```

Aggregate:

```text
stopped_count=4
grounded_stop_rate=1.0000
relation_aligned_stop_rate=1.0000
grounded_wrong_relation_rate=0.0000
```

The OOD task failed before reaching evidence.

## Semantic planner

The four known-intent tasks were correct, grounded, and relation-aligned.

For `ood-001`:

```text
answer_correct=False
answer_grounded=True
final_evidence_consumed=True
extracted_relation_answer='CIRRUS-DLQ'
relation_aligned=False
grounded_wrong_relation=True
```

Aggregate:

```text
stopped_count=5
grounded_stop_rate=1.0000
relation_aligned_stop_rate=0.8000
grounded_wrong_relation_rate=0.2000
```

## Main conclusion

The experiment separates four distinct properties:

```text
evidence availability
→ answer groundedness
→ relation alignment
→ final correctness
```

The semantic planner satisfied the first two properties on the OOD task but failed the final two.

Therefore document-level groundedness is insufficient for judging whether an agent answered the requested semantic relation.
