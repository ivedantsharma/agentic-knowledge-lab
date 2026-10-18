# Phase 2 Final Review

## Status

Phase 2 is nearing completion.

## Objective

Study how document transformation and retrieval-unit design affect retrieval quality.

## What was built

### Data model

- SourceDocument
- DocumentChunk
- DocumentSection
- StructuredDocument
- EvidenceTask

### Ingestion and loading

- source-document loader
- chunk loader
- structured-document loader

### Chunking

- fixed-size word chunking
- overlap
- section-aware chunking
- deterministic parent context
- rich chunk-specific context

### Evaluation

- evidence-derived chunk relevance
- Hit@K
- fragmentation detection
- dense retrieval comparisons
- candidate-score failure analysis
- cross-encoder reranking

## Major findings

### Finding 1 — very small chunks can destroy evidence

12-word chunks split the Borealis evidence so no single chunk contained the full labeled phrase.

### Finding 2 — overlap is a tradeoff

Overlap fixed the Atlas boundary failure but increased redundancy and hurt Cirrus top-k behavior.

### Finding 3 — larger fixed chunks performed better on this corpus

30-word fixed chunks outperformed 18-word chunks.

### Finding 4 — semantic boundaries helped, but not enough

Section-aware chunks improved over small fixed chunks but did not outperform the 30-word baseline overall.

### Finding 5 — parent context helped ranking

Adding document/section identity improved Cirrus from rank 3 to rank 2.

### Finding 6 — more context was not automatically better

Rich chunk-specific context did not improve beyond the simpler parent prefix.

### Finding 7 — dense retrieval had enough recall

For the Cirrus failure, the answer-bearing chunk was already rank 2 with a small score gap.

### Finding 8 — reranking fixed candidate ordering

The cross-encoder moved the relevant Cirrus chunk to rank 1.

Dense:
- Hit@1 = 0.6667
- MRR = 0.8333

Dense + reranker:
- Hit@1 = 1.0000
- MRR = 1.0000

## Phase 2 exit status

Completed:

- [x] ingest versioned source documents
- [x] deterministic chunking
- [x] preserve provenance
- [x] compare whole-document vs chunk retrieval
- [x] demonstrate a chunk-boundary failure
- [x] test overlap
- [x] compare chunk sizes
- [x] test structure-aware chunking
- [x] test contextualized chunks
- [x] add chunking-independent evidence labels
- [x] diagnose a retrieval ranking failure
- [x] test reranking

Remaining before final close:

- [ ] add one ingestion path for a real file format
- [ ] update ADR/documentation with final Phase 2 decisions
- [ ] run final tests and produce Phase 3 handoff

## Recommended Phase 3 direction

Phase 3 should move from single-hop retrieval units into richer information architecture.

Suggested focus:

1. multi-document evidence,
2. multi-hop tasks,
3. hierarchical retrieval,
4. graph/claim-evidence representations,
5. agent-driven retrieval planning,
6. evidence aggregation and verification.

The research loop remains:

```text
hypothesis
→ baseline
→ evaluation
→ failure analysis
→ improvement
→ rerun
```
