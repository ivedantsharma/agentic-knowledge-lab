# EXP-056: Semantic Entity Ranking Diagnostic

## Research question

Can semantic entity profiles rank the intended graph node highly for implicit or paraphrased references, and are their scores separated from unrelated questions?

## Motivation

EXP-055 established a safe lexical boundary:

```text
explicit registered surface → resolve
otherwise → abstain
```

The next step is not to replace that resolver.

It is to determine whether semantic similarity can provide a useful fallback.

## Entity profile

Each entity is represented by:

- canonical name,
- entity type,
- aliases,
- evidence text from claims where the entity is subject or object.

Example Borealis profile includes evidence describing it as a storage system for customer profile data.

## Diagnostic only

EXP-056 does not choose an acceptance threshold.

It ranks entities and records scores.

This prevents selecting an arbitrary threshold before observing the score distribution.

## Task groups

Positive semantic cases:

- implicit Borealis reference,
- paraphrased Platform Reliability reference.

Negative cases:

- unrelated payroll database question,
- unrelated office catering question.

## Metrics

- LexicalAbstentionRate
- SemanticHit@1
- SemanticHit@3
- positive top scores
- negative top scores

## Decision rule after the experiment

If positive questions rank correctly and their scores are clearly separated from negatives, a thresholded hybrid resolver becomes justified.

If scores overlap strongly, semantic top-1 should not automatically become an entity link.
