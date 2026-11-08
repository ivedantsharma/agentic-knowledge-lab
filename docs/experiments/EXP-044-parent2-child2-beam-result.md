# EXP-044 Result: Parent Beam 2 + Child Beam 2

## Aggregate

```text
ParentRecall@2=1.0000
ChildRecall@1=0.6667
ChildRecall@2=1.0000
EvidenceRetentionRate=1.0000
RetainedChildrenPerQuery=2.00
ScoredChildrenPerQuery=8.00
```

## Interpretation

A two-level beam preserves all answer-bearing sections on the parent-stress benchmark.

Atlas and Borealis rank their relevant child first.

Cirrus ranks the relevant child second:

```text
1. distractor_cirrus_failures::Exhausted Retry Monitoring
2. manual_gamma::Dead Letter Handling
```

Keeping a child beam of two prevents the answer-bearing section from being discarded.

## Cost

The system scores eight pooled child sections and retains two.

This separates:

- scoring budget,
- downstream context budget.

## Conclusion

Hierarchical retrieval should preserve a small candidate frontier rather than force a top-1 decision at every level.

The next step is to descend retained sections into chunks.