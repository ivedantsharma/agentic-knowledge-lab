# Phase 1 — Designing a Discriminative Retrieval Benchmark

Our first BM25 vs dense experiment produced identical aggregate metrics.

That does **not** mean the two retrievers are equivalent.

It means the benchmark is not yet discriminative enough.

## 1. What is a discriminative benchmark?

A discriminative benchmark contains tasks that expose meaningful differences between systems.

If every system gets 100%, the benchmark cannot help us decide which system is better.

## 2. Retrieval failure modes we want to isolate

### Lexical-favored tasks

These should reward exact matching.

Examples:
- error codes
- RFC identifiers
- function names
- product IDs
- exact technical strings

Expected:
BM25 may outperform dense retrieval.

### Dense-favored tasks

These should use paraphrases with little exact word overlap.

Example:

Document:
```text
Virtual environments isolate package dependencies.
```

Query:
```text
How do I stop one Python project's libraries from interfering with another?
```

Expected:
Dense retrieval may outperform BM25.

### Distractor-heavy tasks

Several documents should contain overlapping words, but only one should contain the correct meaning.

This tests whether retrieval uses the right signal instead of superficial overlap.

## 3. Controlled benchmark design

We will create a new dataset while keeping:

- same evaluator
- same metrics
- same top_k
- same BM25 implementation
- same dense embedding model

The changed variable is the benchmark difficulty/composition.

## 4. Why category labels matter

Each task will be labeled:

- lexical
- semantic
- distractor
- unanswerable

This will later let us compare:

```text
BM25 lexical performance
vs
dense lexical performance

BM25 semantic performance
vs
dense semantic performance
```

Overall averages alone can hide those differences.

## 5. Research interpretation

If BM25 wins lexical tasks and dense wins semantic tasks, that is evidence supporting a future hybrid retriever.

But we should measure that before building hybrid retrieval.
