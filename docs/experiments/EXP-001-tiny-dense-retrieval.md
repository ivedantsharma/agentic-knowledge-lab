# EXP-001: Tiny Dense Retrieval Search

## Question

Can a small sentence-embedding model retrieve the correct document when the query uses wording that differs from the document?

## Model

`sentence-transformers/all-MiniLM-L6-v2`

## Corpus

Five tiny documents covering:
- Python virtual environments
- dog sleeping
- stock markets
- reinforcement learning
- HTTP connection errors

## Queries and Results

### Query 1

```text
How do I stop Python package versions from conflicting between projects?
```

Top result:

```text
doc_python — 0.7608
```

Relevant document:

```text
Python virtual environments isolate project dependencies so different projects can use different package versions.
```

### Query 2

```text
How can a model learn from rewards?
```

Top result:

```text
doc_rl — 0.6515
```

Relevant document:

```text
Reinforcement learning trains an agent using rewards that encourage useful behavior.
```

### Query 3

```text
Why is my server refusing the connection?
```

Top result:

```text
doc_http — 0.6251
```

Relevant document:

```text
ERR_CONNECTION_REFUSED usually means the target server rejected or did not accept the network connection.
```

## Interpretation

All three queries ranked the semantically correct document first.

This is especially important for Query 3:

```text
Why is my server refusing the connection?
```

The document contains the technical token:

```text
ERR_CONNECTION_REFUSED
```

but the query does not.

Dense retrieval still retrieved the correct document because the embedding model captured semantic similarity rather than relying only on exact word overlap.

## What this demonstrates

The experiment validates the basic dense-retrieval pipeline:

```text
documents
↓
document embeddings

query
↓
query embedding
↓
cosine similarity
↓
rank documents
↓
top-k results
```

## Important limitations

This does **not** prove dense retrieval is always better than lexical retrieval.

The corpus has only five simple documents.

Dense retrieval can struggle with:
- exact IDs
- rare identifiers
- error codes
- product numbers
- exact quotations
- unusual proper nouns

Those cases motivate later lexical/BM25 and hybrid-retrieval experiments.

## Next research step

Do not immediately add more retrieval algorithms.

First define:
- research questions,
- hypotheses,
- baselines,
- datasets,
- metrics,
- experiment rules.

That is Phase 1.
