# Phase 2 High-Level Design

## Goal

Transform source documents into retrieval-ready representations while preserving provenance and enough context for reliable retrieval.

## Current pipeline

```text
SourceDocument
    ↓
ingestion
    ↓
chunking strategy
    ↓
DocumentChunk[]
    ↓
embedding / lexical indexing
    ↓
first-stage retrieval
    ↓
candidate set
    ↓
optional reranking
    ↓
RunResult
    ↓
KnowledgeBench
```

## Chunking strategies implemented

### Fixed word chunks

Parameters:
- chunk_size_words
- overlap_words

Observed tradeoffs:
- very small chunks can fragment evidence,
- overlap can repair boundaries but increase redundancy,
- larger chunks preserve context but reduce granularity.

### Structure-aware chunks

One chunk per semantic section.

Benefits:
- avoids arbitrary boundaries,
- preserves local section meaning.

Observed limitation:
- section text can still lose parent-document context.

### Parent-context chunks

Adds:
- document title,
- section title.

Observed result:
- improved MRR but not Hit@1 on the Cirrus failure.

### Rich chunk-specific context

Adds a short section-role description.

Observed result:
- no improvement beyond parent-title context on the current benchmark.

## Evidence representation

Benchmark relevance is defined using source-level evidence rather than hard-coded chunk IDs.

```text
EvidenceTask
├── question
├── source_document_id
├── evidence_text
└── expected_answer
```

Relevant chunk IDs are derived automatically per chunking configuration.

This allows fair comparison across:
- different chunk sizes,
- overlap,
- structure-aware chunking,
- contextual chunking.

## Metrics

Phase 2 uses:
- Recall@K
- Precision@K
- MRR
- Hit@K
- fragmented task count
- chunk count

Hit@K is important when overlap duplicates the same evidence across several chunks.

## Reranking

Current two-stage retrieval path:

```text
dense bi-encoder
↓
top-k candidates
↓
cross-encoder
↓
final ranking
```

Use reranking only when first-stage recall is sufficient.

## Current architectural findings

1. Chunking is an optimization problem, not a preprocessing default.
2. Smaller chunks are not automatically better.
3. Overlap can both help and hurt.
4. Semantic structure is useful but may lose parent context.
5. More contextual prose is not automatically better.
6. Reranking can fix close ranking errors when recall is already good.
7. Relevance labels should be independent of chunking implementation.

## Phase 2 non-goals

Not yet solved:
- real PDF/HTML/Markdown ingestion,
- page-level provenance,
- tokenizer-aware chunk limits,
- LLM-generated contextual retrieval,
- large-scale vector indexes,
- multi-hop retrieval,
- graph/hierarchical retrieval,
- learned chunking,
- learned retrieval routing.
