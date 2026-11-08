# EXP-043 Result: Pooled Child Rank Diagnostic

## Aggregate

```text
beam 1
ChildRecall@1=0.0000
ChildRecall@2=0.0000
ChildRecall@3=0.0000
ChildMRR=0.0000

beam 2
ChildRecall@1=0.6667
ChildRecall@2=1.0000
ChildRecall@3=1.0000
ChildMRR=0.8333

beam 3
ChildRecall@1=0.6667
ChildRecall@2=1.0000
ChildRecall@3=1.0000
ChildMRR=0.8333
```

## Interpretation

Beam 1 fails because the correct parent is absent.

At beam 2, all answer-bearing sections are present in the pooled child ranking.

For Atlas and Borealis, the relevant child ranks first.

For Cirrus, the relevant child ranks second:

```text
1. distractor_cirrus_failures::Exhausted Retry Monitoring
2. manual_gamma::Dead Letter Handling
```

This is a near-miss, not a deeply buried relevance failure.

## Main conclusion

The hierarchy should not collapse to top-1 child immediately.

A child beam of 2 preserves all answer-bearing sections on this stress benchmark while keeping the candidate set small.

Beam 3 gives no recall improvement over beam 2.

## Next experiment

Evaluate parent beam 2 + child beam 2 as a retrieval policy and compare retained evidence versus context cost.