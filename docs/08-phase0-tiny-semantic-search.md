# Phase 0 — Stage C: Build a Tiny Semantic Search Engine

Now we will use embeddings for an actual retrieval task.

## Goal

Given a small set of documents and a user query:

1. embed every document,
2. embed the query,
3. compare the query embedding with every document embedding,
4. sort by cosine similarity,
5. return the most relevant documents.

## Why this matters

This is the simplest possible dense retriever.

Later, FAISS or Qdrant will make the search much faster across large collections, but the basic logic remains:

```text
query
↓
query embedding
↓
compare with document embeddings
↓
rank
↓
top-k documents
```

## Documents

We will use a tiny corpus containing topics such as:
- Python virtual environments,
- dog sleeping,
- stock markets,
- reinforcement learning,
- HTTP errors.

## Query examples

Try queries like:

```text
How do I prevent Python packages from conflicting?
```

and:

```text
How can a model learn from rewards?
```

The query does not need to exactly match document wording.

## New concept: top-k

If `k = 3`, return the three highest-ranked documents.

The ranked list might look like:

```text
1. document_4  score=0.81
2. document_2  score=0.63
3. document_5  score=0.20
```

## Important limitation

This implementation compares the query with every document one by one.

That is fine for five documents.

It is inefficient for millions.

Later we will learn approximate nearest-neighbor indexes.
