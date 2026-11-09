# EXP-071 Result: Expanded Hard Benchmark and Per-Challenge Slices

## Overall BM25

```text
MeanSupportingRecall@3=0.7778
MRR=0.9167
MeanEvidenceChainCoverage=0.6667
DistractorHitRate=0.5000
ContradictionHitRate=0.0000
StaleHitRate=1.0000
MeanAmbiguityCandidateCoverage=1.0000
UnanswerableRetrievalRate=1.0000
```

## Overall Dense MiniLM

```text
MeanSupportingRecall@3=0.7500
MRR=0.8333
MeanEvidenceChainCoverage=0.6250
DistractorHitRate=0.5000
ContradictionHitRate=1.0000
StaleHitRate=0.6667
MeanAmbiguityCandidateCoverage=1.0000
UnanswerableRetrievalRate=1.0000
```

## Challenge-level findings

### Ambiguity

Both retrievers expose all annotated competing interpretations:

```text
ambiguity coverage=1.0000
```

### Contradiction

BM25:

```text
supporting recall=1.0000
chain coverage=1.0000
contradiction hit rate=0.0000
```

Dense:

```text
supporting recall=0.7500
chain coverage=0.7500
contradiction hit rate=1.0000
```

Dense is much more exposed to pending contradictory policy documents on this slice.

### Stale knowledge

BM25:

```text
supporting recall=0.5556
stale hit rate=1.0000
```

Dense:

```text
supporting recall=0.6667
stale hit rate=0.6667
```

BM25 retrieves more stale evidence on the temporal slice.

### Multi-hop

BM25:

```text
supporting recall=0.6667
chain coverage=0.6667
```

Dense:

```text
supporting recall=0.6250
chain coverage=0.6250
```

Neither retriever reliably reconstructs all multi-hop evidence at top-3.

### Unanswerable

Both:

```text
UnanswerableRetrievalRate=1.0000
```

This remains expected for fixed top-k retrieval without abstention.

## Research conclusion

The expanded benchmark produces meaningfully different failure profiles.

A single aggregate score would hide:

- BM25's stronger contradiction avoidance,
- BM25's higher stale exposure,
- Dense's stronger stale support recall,
- Dense's contradiction exposure,
- shared ambiguity coverage,
- shared inability to abstain.

Therefore the challenge taxonomy is adding useful evaluation information.

## Remaining benchmark question

The results are still tied to top-k=3.

EXP-072 tests whether these conclusions remain visible under different candidate budgets.
