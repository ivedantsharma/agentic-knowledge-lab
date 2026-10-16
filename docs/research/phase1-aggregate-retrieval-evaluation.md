# Phase 1 — Aggregate Retrieval Evaluation

We already know how to score one query.

Now we want to evaluate an entire benchmark.

## 1. Per-query vs benchmark-level metrics

For one query we can compute:

- Recall@K
- Precision@K
- Reciprocal Rank

For a benchmark with many queries, we compute those values for every query and then aggregate them.

Example:

```text
Query 1 Recall@5 = 1.00
Query 2 Recall@5 = 0.50
Query 3 Recall@5 = 0.75
```

Mean Recall@5:

```text
(1.00 + 0.50 + 0.75) / 3
= 0.75
```

---

## 2. Mean Precision@K

Same idea:

```text
mean_precision_at_k =
average of Precision@K across all benchmark queries
```

---

## 3. MRR

MRR means Mean Reciprocal Rank.

For each query:

```text
RR = 1 / rank of first relevant result
```

Then average across queries.

Example:

```text
Query 1 first relevant rank = 1
RR = 1.0

Query 2 first relevant rank = 2
RR = 0.5

Query 3 first relevant rank = 4
RR = 0.25
```

MRR:

```text
(1.0 + 0.5 + 0.25) / 3
= 0.5833
```

MRR rewards systems that put a relevant result near the top.

---

## 4. Benchmark task shape

For now, a retrieval task can be represented minimally as:

```python
{
    "query": "How do virtual environments help?",
    "relevant_ids": {"doc_python"},
}
```

And a retrieval run can produce:

```python
{
    "query": "How do virtual environments help?",
    "retrieved_ids": ["doc_python", "doc_rl", "doc_http"],
}
```

Later we will replace loose dictionaries with typed schemas.

---

## 5. Evaluation flow

```text
Benchmark tasks
    ↓
Retriever outputs
    ↓
Pair each query with ground truth
    ↓
Per-query metrics
    ↓
Aggregate
    ↓
Benchmark report
```

---

## 6. Why averages are useful

A single query can be unusually easy or unusually hard.

Averages reduce the chance that one example dominates our judgment.

But averages can still hide important failures.

Later we will also report:
- per-category results,
- failure counts,
- distributions,
- confidence intervals,
- repeated-run variance for stochastic agents.

---

## 7. Exercise

Implement:

`knowledgebench/evaluation/retrieval_evaluator.py`

with:

- `mean_recall_at_k(...)`
- `mean_precision_at_k(...)`
- `mean_reciprocal_rank(...)`

Each function should receive:

```python
retrieved_by_query: dict[str, list[str]]
relevant_by_query: dict[str, set[str]]
```

The query keys should identify the same benchmark tasks.

For now, if a query exists in the relevance ground truth but is missing from retrieval output, treat its retrieved list as empty.

This makes missing system output count as failure rather than silently disappearing from evaluation.

---

## 8. Important design rule

The denominator for benchmark averages should be the number of benchmark queries in the ground-truth relevance mapping.

Why?

Because the benchmark defines what must be evaluated.

A system should not improve its score simply by omitting difficult queries.
