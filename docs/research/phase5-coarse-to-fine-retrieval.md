# Phase 5 — Coarse-to-Fine Retrieval

## What EXP-041 demonstrated

A hierarchical retriever can assign different models to different levels.

Example architecture:

```text
Document level
MiniLM bi-encoder
cheap, broad routing
        ↓
Section level
cross-encoder
expensive, precise reranking
```

## Why not use the cross-encoder over the entire corpus?

A cross-encoder scores query-candidate pairs jointly.

If there are N candidates, it requires approximately N model evaluations per query.

Hierarchy first reduces N.

In the current toy corpus:

```text
flat sections = 12
selected parent's sections = 4
```

So the expensive scorer only evaluates one-third as many section candidates.

At larger scale this difference can become much larger.

## Coarse vs fine retrieval

### Coarse stage

Goal:

- high recall,
- cheap execution,
- identify promising regions of the corpus.

### Fine stage

Goal:

- discriminate near-neighbor evidence,
- spend more compute on fewer candidates.

## New failure mode

This architecture introduces an important bottleneck:

```text
if the coarse parent stage misses the right document,
the fine child stage never sees the right section.
```

So the next concept is parent recall and hierarchical beam width.