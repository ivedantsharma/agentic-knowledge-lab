# Phase 1 — Separating Answerable and Unanswerable Retrieval Evaluation

Our first end-to-end run produced:

- 3 answerable tasks
- 1 unanswerable task

The three answerable tasks all retrieved the correct document at rank 1.

But aggregate Recall@3 and MRR were 0.75 because the unanswerable task had no relevant documents and therefore contributed zero.

That mixes two different capabilities.

## Capability A — Retrieval on answerable tasks

Question:

> When relevant evidence exists, does the retriever find and rank it well?

Metrics:
- Recall@K
- Precision@K
- MRR

These metrics require a non-empty relevance set.

## Capability B — Behavior on unanswerable tasks

Question:

> When no relevant evidence exists, does the system avoid pretending that some document is relevant?

This requires a different evaluation rule.

For now, we will measure a simple diagnostic:

```text
unanswerable retrieval rate
=
fraction of unanswerable tasks for which the retriever returned at least one document
```

A value of:

```text
1.0
```

means every unanswerable task still produced retrieved documents.

That does not necessarily mean the retriever is "wrong" by itself, because most top-k retrievers always return nearest neighbors.

It tells us that a separate abstention or confidence mechanism is needed.

## Why this separation matters

Do not force different task types into metrics that were not designed for them.

A benchmark should measure each capability with a metric that corresponds to the desired behavior.

## Next implication

To handle unanswerable tasks well, dense retrieval eventually needs something like:

- similarity threshold,
- confidence model,
- verifier,
- answer-stage abstention,
- or agent-level evidence sufficiency checks.

We should not add those yet without measuring the baseline first.
