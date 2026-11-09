# EXP-069 Result: Challenge-Aware Baselines on Strengthened v1 Corpus

## BM25

```text
MeanSupportingRecall@3=0.6667
MRR=1.0000
MeanEvidenceChainCoverage=0.6667
DistractorHitRate=1.0000
ContradictionHitRate=1.0000
StaleHitRate=1.0000
UnanswerableRetrievalRate=1.0000
```

## Dense MiniLM

```text
MeanSupportingRecall@3=0.5833
MRR=0.7500
MeanEvidenceChainCoverage=0.5833
DistractorHitRate=1.0000
ContradictionHitRate=1.0000
StaleHitRate=0.0000
UnanswerableRetrievalRate=1.0000
```

## Interpretation

BM25 retains stronger supporting recall and evidence-chain coverage on the seed, but the strengthened corpus exposes it to both stale and contradictory evidence at top-3.

Dense MiniLM also retrieves the contradiction, but the stale Borealis policy remains outside top-3.

This demonstrates a challenge-specific tradeoff:

```text
BM25:
higher support coverage
+ higher stale exposure

Dense:
lower support coverage
+ lower stale exposure
```

Both fixed-top-k retrievers continue to return documents for unanswerable tasks.

## Scientific conclusion

The strengthened v1 corpus succeeds as a harder retrieval benchmark.

Challenge-aware metrics reveal behavior that a single aggregate retrieval score would hide.
