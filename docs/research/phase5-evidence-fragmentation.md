# Phase 5 — Evidence Fragmentation at the Chunk Level

## A new failure class

At the document level, failure means choosing the wrong document.

At the section level, failure means choosing the wrong semantic region.

At the chunk level, there is an additional possibility:

```text
the correct section is selected
but the evidence is split across chunk boundaries
```

This is fragmentation.

## Why ranking cannot fix fragmentation

If no individual chunk contains the full evidence span, even a perfect ranker cannot return a chunk containing that span.

That means fragmentation is an ingestion/chunking problem, not a retrieval-model problem.

## Typical fixes

- add overlap,
- increase chunk size,
- use sentence-aware boundaries,
- preserve adjacent chunks.

## Scientific next step

Change only overlap first.

Keep chunk size fixed at 10 words and compare:

```text
overlap = 0
vs
overlap = 3
```

If Borealis is repaired, we have direct evidence that overlap solves this boundary failure.