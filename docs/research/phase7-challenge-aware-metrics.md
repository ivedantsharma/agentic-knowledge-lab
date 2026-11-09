# Phase 7: Challenge-Aware Retrieval Metrics

KnowledgeBench v2 separates two questions that ordinary retrieval metrics often merge:

```text
Did we retrieve useful evidence?
What harmful or misleading evidence also entered the candidate set?
```

## Supporting recall

Supporting recall measures positive evidence availability.

For a three-document evidence chain:

```text
2 supporting documents retrieved
→ supporting recall = 2/3
```

## Evidence-chain coverage

Evidence-chain coverage uses the explicit chain annotation.

At this stage it measures membership coverage, not whether a planner followed the chain in the correct order.

Order-aware path evaluation will become more important for agent evaluation.

## Adversarial evidence rates

### Distractors

A distractor is plausible but irrelevant.

### Contradictions

A contradiction directly disagrees or appears to disagree with the intended answer.

Retrieving one is not necessarily an error.

The error may happen later if the system trusts it without resolving provenance or status.

### Stale evidence

Stale evidence was previously valid but should not determine the current answer.

A good benchmark should expose whether a retriever places stale and current evidence together.

## Why unanswerable retrieval remains useful

BM25 and dense nearest-neighbor retrieval normally return something whenever top-k is requested.

Therefore:

```text
UnanswerableRetrievalRate ≈ 1
```

is expected for a plain retriever.

That is not a broken metric.

It demonstrates that retrieval ranking and answerability detection are separate capabilities.

Later systems must add confidence, verification, or abstention rather than pretending nearest-neighbor ranking solves unanswerability.
