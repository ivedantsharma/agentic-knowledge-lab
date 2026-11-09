# EXP-066 Result: KnowledgeBench v2 BM25 vs Dense Baseline

## BM25

```text
MeanSupportingRecall@3=0.6667
MRR=1.0000
MeanEvidenceChainCoverage=0.6667
DistractorHitRate=1.0000
ContradictionHitRate=0.0000
StaleHitRate=0.0000
UnanswerableRetrievalRate=1.0000
```

## Dense MiniLM

```text
MeanSupportingRecall@3=0.5833
MRR=0.7500
MeanEvidenceChainCoverage=0.5833
DistractorHitRate=1.0000
ContradictionHitRate=0.0000
StaleHitRate=0.0000
UnanswerableRetrievalRate=1.0000
```

## Task-level observations

### Atlas / Borealis

BM25 retrieved:

```text
Atlas ownership
Cirrus contradiction
Aurora distractor
```

Only one of three required supporting documents was present.

Dense retrieved:

```text
Aurora distractor
current Borealis policy
Atlas ownership
```

Dense recovered two of three supporting documents but ranked the Aurora distractor first.

### Cirrus

BM25 recovered both supporting documents and therefore the full evidence chain.

Dense retrieved the Cirrus manual but missed the Developer Productivity bridge document in top-3.

## Main comparison

On this seed:

```text
BM25 > Dense
```

for aggregate supporting recall, MRR, and evidence-chain coverage.

However, this is a three-task seed and should not be interpreted as a general conclusion that lexical retrieval is superior.

## Important negative findings

Both retrievers returned documents for the unanswerable task:

```text
UnanswerableRetrievalRate=1.0000
```

This is expected for fixed-top-k ranking without an abstention policy.

Neither stale nor contradictory evidence entered top-3.

EXP-067 therefore checks their full-corpus rank before deciding whether the retrievers handled those challenges well or whether the adversarial examples are simply too weak.
