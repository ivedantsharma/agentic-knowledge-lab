# Phase 1 — Typed Benchmark Evaluation

We now have two schemas:

```text
KnowledgeTask
= ground truth

RunResult
= observed system output
```

The evaluator connects them.

## Why this layer exists

Metrics such as Recall@K and MRR operate on simple structures:

```text
retrieved document IDs
relevant document IDs
```

But our benchmark should operate on typed objects.

So we add an adapter layer:

```text
list[KnowledgeTask]
+
list[RunResult]
↓
match using task_id
↓
extract retrieval IDs
↓
reuse metric functions
↓
BenchmarkRetrievalReport
```

This is preferable to duplicating metric logic.

## Important rule

The task set defines what must be evaluated.

If a task exists but no matching `RunResult` exists, the evaluator treats that task as having no retrieved documents.

Missing output therefore counts as failure rather than disappearing from the score.

## Report

For now the report contains:

- mean_recall_at_k
- mean_precision_at_k
- mean_reciprocal_rank
- evaluated_tasks
- missing_results

Later this report can grow to include:
- answer accuracy
- category slices
- tool-call statistics
- latency
- robustness scores
- confidence intervals
