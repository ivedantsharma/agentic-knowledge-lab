# EXP-020: Structured Retrieval State

## Goal

Test whether a structured state can carry both the extracted entity and a qualifier between hops.

## Result

```text
HopAccuracy      = 1.0000
ExactChainMatch  = 1.0000
FactAccuracy     = 1.0000
AnswerCorrect    = 1.0000
```

## Key state transition

Hop 2 produced:

```text
entity = Borealis
qualifiers = [production]
source_document_id = org_platform_reliability
```

Hop 3 then rendered:

```text
What is the incremental backup cadence for the production Borealis service?
```

The production manual ranked above the staging manual.

## Interpretation

Structured state repaired the information-loss failure without hard-coding the qualifier into the executor.

This supports carrying retrieval-relevant context between hops rather than compressing state into one bare entity string.

## Limitation

The result is still based on one benchmark task.

The next experiment expands the benchmark to multiple independent chains.
