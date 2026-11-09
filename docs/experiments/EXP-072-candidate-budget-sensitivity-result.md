# EXP-072 Result: Candidate-Budget Sensitivity

## BM25

```text
k=1
supporting recall=0.4444
chain coverage=0.4167
distractor=0.0000
contradiction=0.0000
stale=0.3333
ambiguity=0.5000

k=3
supporting recall=0.7778
chain coverage=0.6667
distractor=0.5000
contradiction=0.0000
stale=1.0000
ambiguity=1.0000

k=5
supporting recall=0.7778
chain coverage=0.6667
distractor=1.0000
contradiction=0.5000
stale=1.0000
ambiguity=1.0000
```

BM25 support gains saturate at k=3 while adversarial exposure continues to rise at k=5.

## Dense MiniLM

```text
k=1
supporting recall=0.5000
chain coverage=0.2500
distractor=0.5000
contradiction=0.0000
stale=0.3333
ambiguity=0.5000

k=3
supporting recall=0.7500
chain coverage=0.6250
distractor=0.5000
contradiction=1.0000
stale=0.6667
ambiguity=1.0000

k=5
supporting recall=0.8611
chain coverage=0.7917
distractor=1.0000
contradiction=1.0000
stale=1.0000
ambiguity=1.0000
```

Dense continues gaining support and chain coverage at k=5, but reaches full exposure to the annotated stale, contradictory, and distractor cases.

## Main conclusion

Candidate budget creates a Pareto frontier:

```text
more candidates
→ more useful evidence
→ more adversarial evidence
```

There is no universally best k.

For BM25, k=3 is a natural benchmark reference point because support gains saturate there.

For Dense, k=5 improves evidence coverage further, but only by accepting substantially more adversarial exposure.

## Benchmark implication

KnowledgeBench v2 should report candidate budget with every retrieval result.

Comparing systems at different k values would confound retrieval quality with candidate-set size.

## Unanswerable behavior

For both retrievers and every tested k:

```text
UnanswerableRetrievalRate=1.0000
```

Fixed top-k retrieval still has no abstention mechanism.
