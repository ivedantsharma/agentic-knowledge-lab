# Phase 2 — Testing Chunk Overlap

## Motivation

The first fixed-chunk experiment exposed a boundary failure.

The Atlas question needs concepts that landed on opposite sides of an 18-word boundary:

```text
chunk 0:
... Atlas ... Token Rotation. Access-token signing

chunk 1:
keys rotate ... current key identifier is ATLAS-KV-104
```

The answer-bearing chunk lost some of the query context.

## Hypothesis

Adding overlap will copy some words from the previous chunk into the next chunk.

That may allow the answer-bearing chunk to contain both:

- the contextual terms that make it retrievable,
- the answer text itself.

## Configuration

Baseline:

```text
chunk_size = 18
overlap = 0
stride = 18
```

Experiment:

```text
chunk_size = 18
overlap = 6
stride = 12
```

The chunk size stays fixed.

Only overlap changes.

That makes this a controlled comparison.

## Tradeoff

Overlap can improve boundary preservation, but it also:

- increases number of chunks,
- duplicates text,
- increases indexing cost,
- can fill top-k with near-duplicate chunks.

So the goal is not "more overlap is always better."

The goal is to measure whether modest overlap fixes identifiable failures at acceptable redundancy cost.
