# EXP-043: Pooled Child Rank Diagnostic

## Research question

When beam=2 recovers the correct parent but Cirrus still fails, where does the answer-bearing section rank in the pooled child list?

## Why diagnose before changing architecture

If the relevant child is rank 2, the system has a precision-at-1 problem.

If it is rank 6 or 7, the scorer has a more fundamental relevance problem.

Those cases justify different fixes.

## Experiment

For parent beams 1, 2, and 3:

- pool all child sections from selected parents,
- cross-encode all query-section pairs,
- record the rank of the section containing benchmark evidence,
- compute ChildRecall@1, ChildRecall@2, ChildRecall@3, and MRR.

## Controlled variables

No retrieval component changes.

This is a diagnostic experiment only.

## Expected value

The experiment separates:

```text
parent-routing failure
from
pooled-child ranking failure
```

and tells us whether top-k child retention could be useful before adding another scoring mechanism.