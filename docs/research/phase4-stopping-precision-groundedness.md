# Phase 4 — Stopping Precision and Groundedness

## Why stopping is asymmetric

Suppose an agent makes a poor SEARCH query.

It may still recover on a later step.

Suppose an agent makes a poor STOP decision.

The trajectory ends.

Therefore false-positive stopping is often more damaging than an extra search.

## Binary-classification view

Treat stopping as:

```text
positive = STOP
negative = SEARCH
```

Then:

- false positive = stop too early,
- false negative = search even though enough evidence exists.

In many knowledge-agent settings we prefer higher STOP precision, even at the cost of some extra searches.

## Groundedness

An answer is grounded when it is supported by retrieved evidence.

For this experiment we use a very strict operational definition:

```text
the answer must be an exact span from the evidence
```

This is not the final definition of groundedness.

It is a deterministic baseline.

## Why combine model judgment and deterministic validation?

The model is useful for semantic judgment:

```text
Does this evidence appear to answer the question?
```

Deterministic code is useful for enforcing an invariant:

```text
Do not return an answer that is absent from the evidence.
```

The hybrid STOP policy therefore becomes:

```text
semantic sufficiency
AND
evidence grounding
```

This is a common pattern in robust agent systems: use models for flexible reasoning and deterministic checks for hard safety/correctness constraints.
