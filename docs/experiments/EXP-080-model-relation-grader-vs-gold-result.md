# EXP-080 Result: Model Relation Grader vs Deterministic Gold

## Validation

```text
222 tests passed
ruff passed
```

## Model

```text
Qwen/Qwen2.5-1.5B-Instruct
```

used through the existing `QwenRelationVerifier`.

## Results

```text
cases=8
valid_predictions=8
format_errors=0
true_positive=3
true_negative=4
false_positive=0
false_negative=1
accuracy=0.8750
positive_precision=1.0000
positive_recall=0.7500
negative_accuracy=1.0000
```

## Disagreement

The only disagreement was:

```text
rel-001
category=correct_relation
expected=True
predicted=False
```

Question:

```text
What incremental backup cadence is used by the production Borealis service?
```

Evidence contains:

```text
Full backups run every Sunday.
Incremental backups run every six hours.
```

Candidate:

```text
every six hours
```

The deterministic gold label is relation-aligned.

The model rejected it.

## Interpretation

The grader produced no false positives on this controlled set.

That is important for a STOP-gate use case:

```text
false positive
→ bad answer accepted
→ agent may stop incorrectly
```

The observed error is instead conservative:

```text
valid answer
→ grader rejects
→ agent may continue searching
```

This still harms efficiency and can create unnecessary search loops, but it is different from accepting a wrong answer.

## Main conclusion

A model grader should itself be treated as an evaluated component.

```text
model judge output
!=
ground truth
```

Even with high aggregate agreement and perfect negative accuracy, the grader can reject valid relation-aligned answers.

Do not prompt-tune this one case immediately.

The next step is disagreement robustness analysis.
