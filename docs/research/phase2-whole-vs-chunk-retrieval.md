# Phase 2 — Whole-Document vs Chunk Retrieval

## Research question

Does splitting multi-topic documents into smaller retrieval units improve retrieval quality compared with indexing each whole document as one item?

## Why this matters

A long source document may contain several unrelated sections.

If the entire document is represented as one retrieval unit, the signal for one small relevant section can be diluted by unrelated content.

Chunking can improve granularity.

But chunking also creates risks:

- evidence can be split across boundaries,
- local context can be lost,
- overlapping chunks can create duplicates.

So chunking should be treated as an experimental variable, not an unquestioned default.

## Experiment design

We create a small multi-section corpus.

Each source document contains several topics.

We evaluate two systems:

### Baseline A — Whole-document retrieval

Each source document is one retrieval item.

Relevant IDs refer to source document IDs.

### Baseline B — Fixed chunk retrieval

Each source document is split into deterministic chunks.

Relevant IDs refer to chunk IDs.

We use the same:
- source text,
- dense embedding model,
- cosine similarity,
- questions,
- top-k,
- evaluator.

The main changed variable is retrieval granularity.

## Important caveat

Whole-document relevance and chunk-level relevance are different label spaces.

Therefore we should compare their retrieval behavior and failure cases carefully rather than treating every metric difference as perfectly apples-to-apples.

The goal of this first experiment is to expose whether smaller retrieval units help isolate relevant sections.
