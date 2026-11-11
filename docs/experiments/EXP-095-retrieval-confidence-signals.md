# EXP-095: Retrieval Confidence Signal Diagnostic

## Research question

Do ranking-confidence and cross-retriever agreement signals correlate with which retriever performs best?

## Trigger from EXP-094

Simple query-surface features were insufficient.

In particular:

```text
hard-001 → Dense wins
hard-005 → BM25 wins
```

despite very similar query length, temporal cues, and relational structure.

## New signal family

Instead of only inspecting the query text, inspect the rankings produced by the candidate retrievers.

These signals are available at inference time.

### BM25 signals

- top-1 score,
- top-1 minus top-2 margin,
- number of nonzero-scoring documents.

### Dense signals

- top-1 cosine score,
- top-1 minus top-2 margin.

### Agreement signals

- whether BM25 and Dense agree on top-1,
- overlap count in top-3,
- top-3 Jaccard similarity.

## Why margins matter

A large within-retriever margin can indicate that one candidate is clearly separated from alternatives.

Important:

```text
BM25 scores and cosine scores are not directly calibrated.
```

Therefore EXP-095 does not compare raw BM25 and Dense score magnitudes as if they shared a scale.

It only diagnoses their within-retriever ranking shapes.

## Why agreement matters

If BM25 and Dense agree strongly, routing may not matter.

If they disagree sharply, the query may be one where strategy selection has higher value.

## No router yet

This experiment is diagnostic.

We do not construct a confidence router until the observed signals support a defensible rule.
