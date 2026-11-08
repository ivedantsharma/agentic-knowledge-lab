# Phase 5 — Three-Level Hierarchy: Document → Section → Chunk

## Why add a chunk level?

Sections preserve semantic structure, but real sections can be long.

If an entire section is passed downstream:

- context cost grows,
- unrelated facts inside the same section remain,
- answer generation receives more noise.

A chunk level provides finer evidence localization.

## Three-level retrieval

```text
query
→ parent document beam
→ section beam
→ chunk candidates
→ final chunk ranking
```

## Ancestry matters

A chunk should preserve:

```text
document_id
section title
local chunk position
```

and its retrieval representation should include parent context.

Without ancestry, a short chunk can become semantically ambiguous.

## New failure modes

Adding chunks introduces new risks:

1. evidence fragmentation across chunk boundaries,
2. loss of section context,
3. wrong chunk ranking inside the right section,
4. increased candidate count if beams are too wide.

## First experiment

Keep the successful parent/section beams fixed:

```text
parent beam = 2
section beam = 2
```

Then split only retained sections into deterministic word chunks.

Use a cross-encoder to rank the chunk candidates.

This isolates the effect of adding the third hierarchy level.