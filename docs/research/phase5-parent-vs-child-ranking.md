# Phase 5 — Parent Routing vs Child Ranking

## Two independent decisions

Hierarchical retrieval has at least two ranking problems:

```text
1. Which parent document should we search?
2. Which child section inside that parent is relevant?
```

A correct parent does not imply a correct child.

## EXP-039 example

For the Cirrus question:

```text
Where are Cirrus jobs sent after exhausting all retries?
```

the system correctly chooses:

```text
Cirrus Worker Manual
```

but then ranks:

```text
Retry Policy
```

above:

```text
Dead Letter Handling
```

The query mentions both:

- retries
- what happens after retries

so the Retry Policy section is semantically close even though it does not contain the destination.

## Important lesson

Hierarchy can reduce the search space without fixing ranking quality.

These are separate benefits:

```text
efficiency
vs
accuracy
```

EXP-039 improves efficiency at the child-search stage:

```text
12 candidates → 4 candidates
```

but accuracy remains:

```text
0.6667
```

## Next research question

Can child retrieval use hierarchical context or a second-stage scorer to distinguish near-neighbor sections inside the correct parent?

Before using a cross-encoder, the next controlled experiment should test whether changing the query representation at the child stage is enough.