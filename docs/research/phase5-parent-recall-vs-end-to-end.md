# Phase 5 — Parent Recall Is Not End-to-End Recall

## Three increasingly strict questions

A hierarchical system should be evaluated at multiple levels.

### 1. Parent recall

Did the selected parent beam contain the correct document?

### 2. Child recall

Once candidate children were pooled, did the relevant section appear near the top?

### 3. End-to-end Hit@1

Did the system finally select the answer-bearing section first?

These metrics answer different questions.

## EXP-042 example

At beam 2:

```text
ParentRecall@2 = 1.0
EndToEndHit@1  = 0.6667
```

So the hierarchy successfully keeps the correct document alive, but the final scorer still makes one wrong decision.

## Why beam width has diminishing returns

Increasing beam width has two effects:

```text
+ increases chance correct parent survives
- increases number of children the expensive scorer must compare
```

Once parent recall has saturated, wider beams may add only cost and distractors.

EXP-042 shows exactly that:

```text
beam 2: parent recall 1.0, 8 children
beam 3: parent recall 1.0, 12 children
```

with identical end-to-end accuracy.

## Research lesson

The correct operating point is not necessarily the widest beam.

We want the smallest beam that preserves enough parent recall for the downstream scorer.