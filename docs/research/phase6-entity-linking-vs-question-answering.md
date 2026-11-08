# Phase 6 — Entity Linking Is Not Question Answering

## The EXP-056 failure

Question:

```text
Which service is maintained by the infrastructure reliability group?
```

Gold start entity:

```text
Platform Reliability
```

Semantic whole-question top 1:

```text
Borealis
```

## Why this can happen

The full question describes both:

- the entity mention: `infrastructure reliability group`,
- the requested answer type: `service`.

A whole-question embedding mixes these roles.

Borealis is semantically compatible with the requested answer type, while Platform Reliability corresponds to the entity mention.

## Entity linking objective

Entity linking should answer:

```text
What graph node does this mention refer to?
```

It should not answer:

```text
What entity best matches the whole question?
```

Those are different tasks.

## Decomposition

A cleaner architecture is:

```text
question
→ mention detection
→ mention-to-entity mapping
→ relation planning
→ graph traversal
```

EXP-057 isolates the second step by providing the mention span as gold.

## Research principle

When a semantic model fails, first check whether the model was given the correct representation of the subproblem.

Do not immediately escalate model size.
