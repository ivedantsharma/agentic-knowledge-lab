# Phase 2 — Similarity Failure Analysis

## Why inspect scores?

A ranking tells us which chunk won.

A score analysis tells us how strongly the embedding model preferred one chunk over another.

For the Cirrus failure:

```text
query:
Where are Cirrus jobs sent after exhausting all retries?
```

we want to compare:

```text
Retry Policy
vs
Dead Letter Handling
```

If the scores are nearly tied, a lightweight reranker may be enough.

If Retry Policy is strongly preferred, the embedding model or representation may be the larger issue.

## What we are testing

We are moving from:

```text
"retrieval failed"
```

to:

```text
"why did this retriever rank the wrong chunk higher?"
```

That is the start of systematic failure analysis.

## Possible outcomes

### Outcome A — tiny score gap

Example:

```text
Retry Policy: 0.611
Dead Letter: 0.607
```

Interpretation:
The retriever is uncertain.

A reranker or lexical signal may resolve it.

### Outcome B — large score gap

Example:

```text
Retry Policy: 0.72
Dead Letter: 0.48
```

Interpretation:
The dense embedding representation strongly favors the wrong concept.

We may need a better embedding model, query transformation, or different retrieval architecture.

## Next decision

Do not add reranking until we inspect this score gap.
