# EXP-042 Result: Parent Routing Stress Test

## Aggregate

```text
ParentRecall@1=0.0000
EndToEndHit@1_beam1=0.0000
AvgChildCandidates_beam1=4.00

ParentRecall@2=1.0000
EndToEndHit@1_beam2=0.6667
AvgChildCandidates_beam2=8.00

ParentRecall@3=1.0000
EndToEndHit@1_beam3=0.6667
AvgChildCandidates_beam3=12.00
```

## Main finding

Beam width solves parent recall but does not guarantee final child correctness.

At beam=1, all correct parents are ranked second, so the answer-bearing child sections are unreachable.

At beam=2, every correct parent enters the candidate pool.

Atlas and Borealis recover fully.

Cirrus still fails even though the correct parent is now available.

## Cirrus failure

The pooled cross-encoder ranks:

```text
distractor_cirrus_failures::Exhausted Retry Monitoring
```

above the answer-bearing section in:

```text
manual_gamma::Dead Letter Handling
```

Therefore the remaining failure is not parent recall.

It is pooled child discrimination under a hard cross-document distractor.

## Cost tradeoff

```text
beam 1 → 4 child candidates
beam 2 → 8 child candidates
beam 3 → 12 child candidates
```

Beam 2 improves parent recall from 0 to 1.

Beam 3 adds 50% more child candidates than beam 2 but gives no accuracy gain.

On this benchmark, beam 2 is therefore the better recall/cost operating point.

## Next step

Before changing the scorer, inspect the full pooled child ranking and the rank of the answer-bearing child.

This will tell us whether the Cirrus evidence is nearly recovered at rank 2/3 or deeply buried.