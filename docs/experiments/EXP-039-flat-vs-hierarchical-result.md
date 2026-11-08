# EXP-039 Result: Flat vs Hierarchical Retrieval Baseline

## Aggregate result

```text
DocumentHit@1=1.0000
FlatSectionHit@1=0.6667
HierarchicalSectionHit@1=0.6667
FlatCandidateCountPerQuery=12.00
HierarchicalChildCandidatesPerQuery=4.00
```

## Interpretation

The hierarchical retriever routes every query to the correct parent document.

However, hierarchical retrieval does not improve section Hit@1 on this benchmark.

Both flat and hierarchical retrieval fail on the Cirrus dead-letter task.

## Cirrus failure

Question:

```text
Where are Cirrus jobs sent after exhausting all retries?
```

Top section:

```text
Retry Policy
score=0.620166
```

Relevant section:

```text
Dead Letter Handling
```

The parent document is correct:

```text
manual_gamma
```

Therefore this is not a parent-routing failure.

It is a within-document child-ranking failure.

## Efficiency result

Flat retrieval compares against:

```text
12 sections per query
```

Hierarchical child retrieval compares against:

```text
4 sections per query
```

This is a 3x reduction in section candidates in this toy corpus.

However, candidate reduction alone does not improve correctness.

## Main conclusion

Hierarchy successfully narrows the search space, but the current child scorer still confuses semantically adjacent sections.

The next experiment should isolate the child-ranking problem rather than changing parent routing.