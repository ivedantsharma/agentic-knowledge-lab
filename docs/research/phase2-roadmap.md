# Phase 2 — Document Ingestion, Chunking, and Information Architecture Foundations

## Objective

Move from tiny synthetic one-paragraph corpus entries to a real document-processing pipeline.

Phase 2 asks:

> How should a knowledge system transform documents into retrieval units without losing the context needed to answer questions accurately?

## Core research questions

1. How does chunk size affect retrieval quality?
2. How does overlap affect retrieval quality and redundancy?
3. When do fixed chunks lose important document-level context?
4. Can contextualized chunks improve retrieval over naive chunks?
5. How should provenance be preserved so retrieved evidence can always be traced back to the source?
6. When does chunking help, and when does it fragment evidence needed for multi-hop questions?

## Planned baselines

### C0 — Whole-document retrieval
No chunking.

### C1 — Fixed-size non-overlapping chunks
Simple baseline.

### C2 — Fixed-size overlapping chunks
Tests whether overlap helps preserve boundary context.

### C3 — Structure-aware chunks
Split using headings/sections where possible.

### C4 — Contextualized chunks
Add document/section context to chunks before indexing.

Do not jump to C3/C4 before measuring C0-C2.

## Phase 2 evaluation

Reuse KnowledgeBench but extend it with tasks where:

- evidence sits near a chunk boundary,
- one answer needs two chunks,
- many chunks share similar local wording,
- the same phrase means different things in different sections,
- a chunk is ambiguous without its parent document context.

Primary metrics remain:

- Recall@1
- Recall@K
- MRR
- category slices

Additional Phase 2 diagnostics:

- chunks retrieved per source document,
- duplicate/overlapping context,
- chunk token/word count,
- provenance correctness,
- evidence fragmentation.

## Exit criteria

Phase 2 is complete when we can:

- ingest source documents,
- deterministically chunk them,
- preserve provenance,
- index/retrieve chunks using BM25 and dense retrieval,
- run chunking experiments,
- compare whole-document vs chunk retrieval,
- document at least one chunk-boundary failure,
- test overlap,
- test one structure/context-aware improvement,
- record findings and architecture decisions.
