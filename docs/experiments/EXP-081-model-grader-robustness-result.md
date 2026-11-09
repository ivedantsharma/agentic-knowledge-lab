# EXP-081 Result: Model-Grader Robustness and Disagreement Analysis

## Validation

```text
222 tests passed
ruff passed
```

## Overall

```text
cases=8
format_errors=0
accuracy=0.7500
```

## Borealis family

Positive variants produced:

```text
original                → False
evidence_order_reversed → True
question_paraphrase     → False
minimal_evidence        → True
```

Therefore:

```text
stable_positive=False
```

The wrong-relation control was correctly rejected.

## Cirrus family

Positive variants produced:

```text
original            → True
question_paraphrase → True
```

The wrong-relation control was correctly rejected.

Therefore:

```text
stable_positive=True
```

## Interpretation

The Borealis failure is not a stable conceptual rejection of the relation.

The model judgment changes under meaning-preserving changes to:

- evidence order,
- question wording,
- evidence length.

This is input-form sensitivity.

## Main conclusion

Model graders must be evaluated for robustness, not only point accuracy.

```text
same semantics
!=
same model-grader judgment
```

on the Borealis family.

The result argues against immediate prompt tuning on one example.

A stronger evaluation stack should prefer deterministic graders when benchmark structure makes them available and treat model graders as fallible components with measured disagreement.
