# Phase 5 High-Level Design

## Goal

Build a hierarchical retrieval system that can preserve answer-bearing evidence while controlling candidate search and downstream context size.

The central Phase 5 question is:

> Can document → section → chunk retrieval improve evidence discovery and context efficiency compared with flat retrieval?

## Final architecture

```text
User Query
    ↓
Dense Document Router
(MiniLM)
    ↓
Top-2 Parent Documents
    ↓
Cross-Encoder Section Reranker
    ↓
Top-2 Sections
    ↓
Local Overlapping Chunking
(10 words, overlap 3)
    ↓
Cross-Encoder Local Chunk Scoring
    ↓
Best Chunk per Retained Section
    ↓
Radius-1 Expansion
(previous + anchor + next)
    ↓
Source-Range Merge
    ↓
Deduplicated Evidence Windows
```

## Core components

### HierarchicalRetrievalConfig

Reusable configuration for:

- parent beam,
- section beam,
- chunk size,
- chunk overlap,
- chunk radius.

The Phase 5 reference configuration is:

```text
parent_beam = 2
section_beam = 2
chunk_size_words = 10
chunk_overlap_words = 3
chunk_radius = 1
```

These values are benchmark-derived reference settings, not universal optima.

### Dense parent routing

`HierarchicalDenseRetriever` ranks document summaries using MiniLM embeddings.

Document summaries include:

- document title,
- section titles.

This is the coarse stage.

Its objective is inexpensive high-recall routing, not final evidence selection.

### Cross-encoder section reranking

All sections inside the retained parent beam are pooled.

The cross-encoder scores query-section pairs jointly.

This is the fine section stage.

The cross-encoder is applied only after parent routing narrows the candidate set.

### Hierarchical chunking

Each retained section is split independently.

Chunks preserve:

- parent document ID,
- section index,
- section title,
- local chunk index,
- source word offsets.

Retrieval text also includes document and section ancestry.

### Local chunk scoring

Chunk ranking occurs inside each retained section.

This preserves the section-level beam instead of flattening all chunks into one global top-k list.

### Radius-1 expansion

The highest-scoring local chunk becomes the anchor.

The final local evidence region includes:

```text
previous chunk
+ anchor chunk
+ next chunk
```

when those chunks exist.

This protects against answer spans immediately before or after the query-matching chunk.

### Deduplicated source windows

Overlapping chunks are useful for retrieval robustness but should not be concatenated naively.

The system merges selected chunk source ranges and reconstructs one unique source window.

Therefore:

```text
retrieval representation
!=
returned context representation
```

## Reusable implementation

The final reusable component is:

```text
knowledge_engine/retrieval/coarse_to_fine.py
```

Main interface:

```text
CoarseToFineHierarchicalRetriever.search(query)
```

It returns:

- selected parent IDs,
- evidence windows,
- document/section/chunk provenance,
- section and anchor scores,
- source word offsets,
- candidate-count diagnostics.

## Final integrated benchmark

Long-section stress benchmark:

```text
EvidenceRetentionRate=1.0000
AvgReturnedWindowWords=43.33
```

The immediately preceding full-section baseline was:

```text
AvgRetainedSectionWords=95.33
```

The accepted radius-1 policy therefore preserved all benchmark evidence while reducing returned context by approximately 54.55%.

## Why the architecture is hierarchical

Each stage narrows a different search space:

```text
all documents
→ selected documents
→ selected sections
→ local chunks
→ local evidence windows
```

The hierarchy is not simply metadata organization.

It changes where compute is spent and where irreversible decisions are made.

## Key design principle

Avoid collapsing to top-1 too early.

Phase 5 experiments showed top-1 errors at both parent and child levels.

Small beams preserve plausible paths until a stronger local scorer or context-construction stage can resolve them.

## Limitations

The benchmark is synthetic and development-influenced.

The final benchmark has only three answerable tasks.

The final settings should therefore be treated as a validated mechanism, not as proof of generalization or production-scale optimality.
