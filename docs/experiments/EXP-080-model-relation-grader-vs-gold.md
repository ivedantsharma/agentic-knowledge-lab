# EXP-080: Model Relation Grader vs Deterministic Gold

## Research question

Can a small instruction model reliably judge relation alignment when compared with deterministic gold labels?

## Why this experiment comes now

Phase 8 has already built deterministic graders for:

- trace structure,
- evidence sufficiency,
- groundedness,
- relation alignment,
- evidence-path quality.

This gives us trusted labels against which a model grader can be evaluated.

Without deterministic references, a model judge could be wrong while appearing authoritative.

## Reused component

```text
QwenRelationVerifier
Qwen/Qwen2.5-1.5B-Instruct
```

The verifier receives:

- question,
- evidence,
- candidate answer,

and returns:

```text
YES / NO
```

for whether the candidate directly answers the requested relation and is supported by the evidence.

## Controlled grader set

Eight cases include:

- correct relation answers,
- grounded but wrong relation answers,
- unsupported answers,
- topically related wrong-type answers.

The gold label is written independently of the model.

## Metrics

- accuracy,
- positive precision,
- positive recall,
- negative accuracy,
- false positives,
- false negatives,
- format errors.

## Why negative accuracy matters

For a grader used as a STOP gate, false positives can be especially costly.

A false positive means:

```text
bad answer
→ grader says acceptable
→ agent stops
```

So we should not judge a grader only by aggregate accuracy.

## Success interpretation

High agreement would show the model grader is promising for cases where deterministic patterns are unavailable.

It would not prove open-domain grader reliability.

Any disagreement should be analyzed rather than prompt-tuned away immediately.
