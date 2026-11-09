# EXP-070 Result: Ambiguity as a First-Class Retrieval Challenge

## BM25 ambiguity task

```text
retrieved:
Nimbus Analytics Cache
Nimbus Session Cache
another document

AmbiguityCandidateCoverage@3=1.0000
```

## Dense MiniLM ambiguity task

```text
retrieved:
Nimbus Session Cache
Nimbus Analytics Cache
another document

AmbiguityCandidateCoverage@3=1.0000
```

## Aggregate

Both retrievers produced:

```text
MeanAmbiguityCandidateCoverage=1.0000
```

## Interpretation

Both retrieval methods exposed both plausible interpretations of the under-specified Nimbus query.

That is desirable at the retrieval stage.

The benchmark does not reward either system for choosing one answer because the task is explicitly ambiguous and unanswerable without clarification.

## Limitation

This is only one ambiguity example.

A single task cannot establish robust ambiguity handling.

EXP-071 expands the benchmark so challenge-level results are not defined by one example.
