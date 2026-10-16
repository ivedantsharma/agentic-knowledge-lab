# Phase 1 — Retrieval Metrics in Code

This module turns Recall@K, Precision@K, and Reciprocal Rank into executable evaluation code.

## 1. Recall@K

Recall@K asks:

> Of all relevant documents, how many did we retrieve in the top K?

Formula:

```text
Recall@K =
number of relevant documents in top K
/
total number of relevant documents
```

Example:

Relevant documents:

```text
{A, B, C, D}
```

Top-5 retrieval:

```text
[A, X, B, Y, C]
```

Three of four relevant documents were found:

```text
Recall@5 = 3 / 4 = 0.75
```

## 2. Precision@K

Precision@K asks:

> Of the K documents we retrieved, how many were relevant?

Same example:

```text
[A, X, B, Y, C]
```

Three of five retrieved documents are relevant:

```text
Precision@5 = 3 / 5 = 0.60
```

## 3. Reciprocal Rank

Reciprocal Rank asks:

> How early did the first relevant result appear?

Formula:

```text
RR = 1 / rank_of_first_relevant_document
```

If the first relevant result appears at rank 4:

```text
RR = 1 / 4 = 0.25
```

If there is no relevant result, RR is usually 0.

## 4. Why Recall and Precision can disagree

Suppose there are 100 relevant documents.

You retrieve only 2 documents, and both are relevant.

Then:

```text
Precision@2 = 2 / 2 = 1.0
Recall@2 = 2 / 100 = 0.02
```

So precision is perfect, but recall is terrible.

Now suppose you retrieve 100 documents and 90 are relevant.

Then:

```text
Precision@100 = 90 / 100 = 0.90
Recall@100 = 90 / 100 = 0.90
```

Increasing K often increases recall, but can reduce precision because more irrelevant documents may enter the result set.

## 5. Retrieval-evaluation mental model

```text
Query
↓
Retriever
↓
Ranked results
↓
Compare against ground-truth relevant document IDs
↓
Recall@K / Precision@K / RR
```

## 6. Exercise

Implement these functions in:

`knowledgebench/metrics/retrieval.py`

- `recall_at_k(...)`
- `precision_at_k(...)`
- `reciprocal_rank(...)`

The functions should work using document IDs only.

Example:

```python
retrieved = ["doc_a", "doc_x", "doc_b", "doc_y", "doc_c"]
relevant = {"doc_a", "doc_b", "doc_c", "doc_d"}
```

Expected:

```text
Recall@5 = 0.75
Precision@5 = 0.60
RR = 1.0
```

Why is RR 1.0 here?

Because the first relevant document appears at rank 1.
