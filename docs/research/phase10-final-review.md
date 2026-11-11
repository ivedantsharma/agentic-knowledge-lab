# Phase 10 Final Review

## Status

Complete.

## Central research question

> Can retrieval behavior adapt to the structure and failure mode of a query?

The answer is yes, but adaptation is not a single routing decision.

## EXP-093

Fixed retriever comparison and oracle routing ceiling.

```text
best fixed Supporting Recall@3=0.7778
oracle Supporting Recall@3=0.8333
```

Modest routing headroom.

## EXP-094

Simple query-surface features did not explain winner differences.

## EXP-095

Retriever confidence and disagreement signals also failed to cleanly separate winners.

## EXP-096

Paired lexical/semantic queries showed:

```text
winner shifts in 4 / 6 pairs
```

So wording matters.

## EXP-097

Expanded oracle routing ceiling:

```text
Hybrid MRR=0.8333
oracle MRR=0.8750
11/12 tied tasks
```

Conclusion: retriever routing alone is not worth complex policy learning yet.

## EXP-098

Adaptive top-k showed much stronger variation:

```text
minimal k ranged from 1 to 5
```

and fixed recall increased from:

```text
0.5556 at k=1
to
0.8889 at k=5
```

Budget is a meaningful control variable.

## EXP-099

Oracle query decomposition improved the saturated Helios case:

```text
0.3333 → 0.6667
```

but did not improve mean recall.

## EXP-100

Literal qualifier preservation produced:

```text
0.7778 → 0.7778
```

No gain.

## Final Phase 10 conclusion

Adaptive retrieval should not be modeled as:

```text
query → choose BM25 or Dense
```

A better abstraction is:

```text
state
→ choose query
→ choose retriever
→ choose budget
→ observe evidence
→ update state
```

The strongest empirical signal in this phase was adaptive budget.

The most important failure signal was that query transformation without structured relation/temporal state remains brittle.

## Why this matters for the project

This turns retrieval into a policy problem suitable for the next stages:

- supervised behavior learning,
- policy imitation,
- reinforcement learning.

## Next phase

# Phase 11 — Fine-Tuning Retrieval/Search Behavior

The next question is:

> Can a model learn better retrieval actions from trajectories and oracle decisions instead of relying on hand-written rules?
