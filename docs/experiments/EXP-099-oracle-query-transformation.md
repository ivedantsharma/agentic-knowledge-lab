# EXP-099: Oracle Query Transformation Upper Bound

## Research question

Can focused query decomposition recover multi-hop evidence that a larger single-shot retrieval budget misses?

## Trigger from EXP-098

kbv2-hard-005 saturated at:

```text
Recall@3=0.3333
Recall@5=0.3333
```

Therefore its failure is not explained by insufficient k alone.

## Hypothesis

A long indirect query asks one retriever to bridge several relations simultaneously.

Breaking it into focused relation queries may align each search step with one document in the evidence chain.

## Controlled setup

Keep fixed:

- KnowledgeBench v2 hard corpus,
- Hybrid RRF retriever,
- MiniLM dense model.

Compare:

### Single shot

```text
original question
→ Hybrid top-5
```

### Oracle transformation

```text
focused subquery 1 → top-1
focused subquery 2 → top-1
...
union retrieved IDs
```

## Tasks

Use multi-hop tasks where the original question exposes a valid starting entity or organization:

- kbv2-hard-001,
- kbv2-hard-005,
- kbv2-hard-006.

## Why this is an oracle

The transformed queries use benchmark-known intermediate entities.

This is not an autonomous query transformation system.

It answers only:

> Is good decomposition capable of repairing the retrieval failure?

If no, there is little value in building a learned query transformer.

If yes, later experiments can replace oracle transformations with generated ones.

## Metrics

Per task:

- single-shot recall,
- transformed recall,
- single-shot candidate budget,
- transformed candidate budget.

Aggregate:

- mean recall,
- mean retrieval budget.

## Important interpretation

A positive result establishes the value of query transformation as a mechanism.

It does not establish that the system can discover the transformations automatically.
