# Phase 2 — Cross-Encoder Reranking

## Why rerank?

Our Cirrus failure produced:

```text
Retry Policy        0.665840
Dead Letter         0.633207
```

The gap is only about:

```text
0.0326
```

That suggests the dense retriever has already found the correct neighborhood but is uncertain about the final ordering.

## Bi-encoder vs cross-encoder

Our current dense retriever is a bi-encoder.

It works like:

```text
query -> embedding
chunk -> embedding
cosine(query, chunk)
```

The query and chunk are encoded separately.

That makes retrieval fast because document embeddings can be precomputed.

But it limits interaction between query words and passage words.

## Cross-encoder

A cross-encoder reads the query and candidate passage together.

Conceptually:

```text
[query + passage]
        ↓
 transformer
        ↓
 relevance score
```

Because both texts are processed jointly, the model can reason more precisely about relationships such as:

```text
question:
where are jobs sent AFTER retries are exhausted?

candidate A:
how jobs are retried

candidate B:
what happens AFTER all retries fail
```

## Why not use a cross-encoder over the whole corpus?

It is much slower.

For every query-document pair, the model must run again.

So the standard pattern is:

```text
fast retriever
    ↓ top-k candidates
cross-encoder
    ↓ reranked candidates
final top-k
```

This is called retrieve-then-rerank.

## Our experiment

Stage 1:
- dense retrieval
- retrieve top 3 chunks

Stage 2:
- cross-encoder reranks only those 3

Model:
`cross-encoder/ms-marco-MiniLM-L6-v2`

We are not changing:
- corpus,
- chunking strategy,
- evidence labels,
- questions.

The changed variable is the second-stage reranker.

## Hypothesis

The reranker should distinguish:
- "Retry Policy" = retry process
- "Dead Letter Handling" = outcome after retries fail

and move the answer-bearing Cirrus chunk to rank 1.
