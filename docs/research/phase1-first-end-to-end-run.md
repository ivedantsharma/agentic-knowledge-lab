# Phase 1 — First End-to-End KnowledgeBench Run

We now have every basic layer required for an end-to-end retrieval benchmark:

```text
tasks.jsonl
+
documents.jsonl
↓
validated loaders
↓
dense retriever
↓
RunResult objects
↓
typed benchmark evaluator
↓
Recall@K / Precision@K / MRR
```

## Why this is a milestone

Earlier experiments printed similarity scores manually.

Now the system:

1. loads versioned benchmark tasks,
2. loads a versioned corpus,
3. embeds the corpus,
4. retrieves documents for every task,
5. stores system outputs as RunResult objects,
6. compares them with task ground truth,
7. produces aggregate benchmark metrics.

This is the first complete KnowledgeBench retrieval pipeline.

## Important limitation

The current dataset is tiny and synthetic.

A high score means only that the pipeline is functioning.

It does not establish research quality or production performance.

## Unanswerable task warning

The current retrieval metrics are not yet sufficient for unanswerable tasks.

If a task has no relevant documents, Recall@K returns 0.

But a system that correctly retrieves nothing may actually be behaving well.

This tells us that unanswerable evaluation needs its own metric/rule rather than forcing every task into ordinary retrieval recall.

That is a future KnowledgeBench design problem.
