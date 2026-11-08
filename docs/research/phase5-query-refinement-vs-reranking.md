# Phase 5 — When Query Refinement Is Not Enough

## What EXP-040 tested

We kept the hierarchical topology fixed and changed only the child-stage query representation.

The goal was to test whether the Cirrus miss was mainly caused by a noisy original query.

## Result

It was not.

Even the focused query:

```text
destination after all retry attempts
```

still ranked:

```text
Retry Policy
```

above:

```text
Dead Letter Handling
```

## Why this can happen

A bi-encoder embeds the query and section independently.

It is optimized for broad semantic similarity, not exact pairwise relation matching.

The Retry Policy section contains strong lexical/semantic signals around:

- retries
- failed jobs
- attempts

so it can remain close to the query even though it does not answer the requested destination relation.

## Why a cross-encoder is different

A cross-encoder reads the query and candidate section together:

```text
[query + section]
```

and outputs one relevance score for that pair.

This allows richer interaction between tokens from the query and the section.

Conceptually:

```text
bi-encoder
query → vector
section → vector
cosine similarity

cross-encoder
query + section → joint transformer → relevance score
```

## Tradeoff

Cross-encoders are more expensive because each query-candidate pair must be scored separately.

Hierarchy makes them more practical:

```text
flat corpus: score many sections
hierarchical: score only children of selected parent
```

This is one of the strongest reasons to combine hierarchy with reranking.