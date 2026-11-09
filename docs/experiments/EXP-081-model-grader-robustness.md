# EXP-081: Model-Grader Robustness and Disagreement Analysis

## Research question

Is the model relation grader stable under small meaning-preserving changes, or does its decision depend on superficial wording/order?

## Trigger from EXP-080

The grader achieved:

```text
Accuracy=0.8750
FalsePositives=0
FalseNegatives=1
```

The only false negative was the Borealis incremental-backup case.

## Why not tune the prompt immediately?

One failed example does not tell us whether the problem is:

- question wording,
- evidence ordering,
- competing facts in the same evidence,
- candidate phrasing,
- broader grader weakness.

Prompt tuning before diagnosis risks overfitting one case.

## Controlled robustness variants

For the Borealis case, keep the semantic answer fixed while varying:

- original evidence,
- evidence sentence order,
- question paraphrase,
- minimal evidence.

Also include a wrong-relation control.

A second Cirrus relation provides another comparison family.

## Robustness concept

A good grader should be approximately invariant to meaning-preserving transformations.

For positive variants:

```text
same meaning
→ same judgment
```

For negative controls:

```text
wrong requested relation
→ reject
```

## Metrics

- per-case correctness,
- format errors,
- overall accuracy,
- within-pair positive prediction consistency.

## Interpretation

If the Borealis false negative disappears under a minor rewrite, that suggests prompt/input sensitivity rather than a stable conceptual failure.

If every equivalent variant fails, that suggests a deeper relation-understanding weakness.

No prompt changes are made in this experiment.
