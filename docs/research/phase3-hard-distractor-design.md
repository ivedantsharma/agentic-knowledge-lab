# Phase 3 — Designing Hard Multi-Hop Distractors

## Why v1 was still too easy

A distractor is only useful if it competes with the correct document for the same query.

For example:

```text
Query:
Which storage system is maintained by Platform Reliability?
```

Weak distractor:

```text
Developer Productivity maintains Cirrus.
```

This is not very competitive because the queried team is different.

Harder distractor:

```text
Platform Reliability previously maintained Aurora storage.
```

Even harder:

```text
Platform Reliability maintains Aurora for legacy reporting.
```

Now both documents contain:
- Platform Reliability,
- maintains,
- storage-related wording.

The retriever must distinguish the intended relation, not just match keywords.

## Hard distractor principles

A strong distractor should overlap with the gold document on some combination of:

- same entity,
- same relation verb,
- same document type,
- same answer type,
- similar sentence structure,
- similar lexical cues.

## Next benchmark

Create a v2 corpus with:

### Hop 1 competition
Two Atlas-like entities and nearly identical "operated by" statements.

### Hop 2 competition
Multiple storage systems maintained by Platform Reliability.

### Hop 3 competition
Multiple Borealis backup cadences for different environments or backup types.

## Why this matters

If retrieval fails under these conditions, we will have a useful failure to analyze.

Then we can test:
- reranking,
- query refinement,
- metadata filters,
- relation-aware retrieval,
- or structured retrieval.

That is much more informative than repeatedly getting 1.0 on an easy benchmark.
