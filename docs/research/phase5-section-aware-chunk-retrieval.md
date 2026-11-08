# Phase 5 — Section-Aware Chunk Retrieval

## Problem with a global chunk beam

After section selection, flattening all chunks into one global list discards hierarchy.

A single section can occupy multiple top positions:

```text
section A chunk 0
section A chunk 1
section B chunk 0
section B chunk 1
↓
global top-2
↓
both slots may come from section A
```

This can eliminate section B even though the section stage intentionally preserved it.

## Section-aware alternative

Treat each retained section as a local search region.

For each retained section:

1. score its chunks,
2. select the strongest local chunk,
3. optionally expand to neighboring chunks.

This preserves the section-level beam while still using fine-grained chunk ranking.

## Small-to-big retrieval

The ranker operates on small chunks because they are precise.

The system can return a slightly larger local window:

```text
best small chunk
+ adjacent chunk
```

This is useful when:

- the query-matching clue is in one chunk,
- the exact answer is in the next chunk,
- the evidence crosses or sits near a boundary.

## Phase 5 evidence

Borealis:

```text
local rank 1: ... incremental backups run every
local rank 2: backups run every six hours.
```

Cirrus:

```text
local rank 1: ... fails all retry attempts is moved to
local rank 2: ... dead-letter queue named CIRRUS-DLQ.
```

In both cases, local neighbor expansion can preserve the answer-bearing text without relying on a global chunk top-k.
