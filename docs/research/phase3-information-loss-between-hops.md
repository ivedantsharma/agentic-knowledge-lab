# Phase 3 — Information Loss Between Hops

## The new failure

Until now our state between hops was:

```text
previous_fact: str
```

Example:

```text
Platform Reliability
Borealis
```

That was sufficient on the easy corpus.

It is not sufficient once the same entity exists in multiple contexts.

## What was lost?

Hop 2 contains:

```text
Borealis storage system for production customer profile data
```

but we reduce this to:

```text
Borealis
```

The next query therefore cannot distinguish:

- production Borealis,
- staging Borealis.

## New concept: retrieval state

A multi-hop system should carry more than one string.

Conceptually:

```text
RetrievalState
├── entity
├── qualifiers
├── source_document
├── relation
└── previous evidence
```

We will introduce this gradually.

For the next controlled experiment, we keep the same entity extractor but explicitly preserve the known environment qualifier in the next query.

This asks:

> Is the failure caused by the dense retriever, or by an under-specified query?

## Why not rerank first?

The dense score gap is small:

```text
0.665681 - 0.650305 = 0.015376
```

That makes reranking tempting.

But both candidate documents genuinely match the ambiguous query.

A reranker cannot recover information that the query does not express.

First repair the query.

Then, if ranking still fails, reranking becomes justified.
