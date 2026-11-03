# EXP-018: Hard-Distractor Failure and Context Loss

## Goal

Stress extracted-fact multi-hop chaining with near-duplicate entities and relation-level distractors.

## Result

```text
HopAccuracy      = 0.6667
ExactChainMatch  = 0.0000
FactAccuracy     = 0.6667
AnswerCorrect    = 0.0000
```

## Hop-level behavior

### Hop 1

Gold document remained rank 1.

```text
org_atlas              0.686297
org_atlas_analytics    0.615293
```

### Hop 2

Gold document remained rank 1, but the legacy alternative was very close.

```text
org_platform_reliability         0.759952
org_platform_reliability_legacy  0.747031
```

### Hop 3

The staging Borealis manual outranked the production manual.

```text
manual_borealis_staging  0.665681
manual_borealis          0.650305
manual_aurora            0.544729
```

The extracted answer became:

```text
every four hours to speed up recovery testing
```

instead of:

```text
every six hours
```

## Critical diagnosis

This is not purely a retrieval-ranking error.

Hop 2 evidence says:

```text
Platform Reliability maintains the Borealis storage system for production customer profile data.
```

But the extractor keeps only:

```text
Borealis
```

The next query becomes:

```text
What is the incremental backup cadence for Borealis?
```

After adding a Borealis staging manual, that query is under-specified.

The chain discarded the qualifier:

```text
production
```

Therefore the failure is partly an **information-loss / query-state failure**.

## Research implication

A multi-hop system should not always compress intermediate evidence into one bare entity string.

It may need to preserve:

- entity,
- qualifiers,
- environment,
- time,
- relation,
- provenance.

## Decision

Before applying reranking as a fix, test whether preserving the missing production qualifier repairs retrieval.

Reranking an ambiguous query would risk hiding the actual cause.
