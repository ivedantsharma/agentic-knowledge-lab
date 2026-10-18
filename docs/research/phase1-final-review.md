# Phase 1 Final Review

## Status

Phase 1 complete.

## Objective

Build the research-engineering foundation required to study agent-native knowledge systems and evaluate them rigorously.

## What was built

### Foundations

- Python 3.12 environment
- uv dependency management
- pytest
- Ruff
- CI-ready repository structure

### Retrieval foundations

- manual cosine similarity
- real sentence embeddings
- tiny semantic search
- BM25 implementation
- dense retrieval baseline
- Reciprocal Rank Fusion baseline

### KnowledgeBench foundations

- KnowledgeTask schema
- KnowledgeDocument schema
- RunResult schema
- JSONL dataset loaders
- duplicate-ID and validation protections
- retrieval metrics
- aggregate evaluator
- category evaluator
- answerable/unanswerable separation

### Metrics

- Recall@K
- Precision@K
- Reciprocal Rank
- Mean Reciprocal Rank
- category-level retrieval metrics
- unanswerable retrieval diagnostic

### Research datasets

- v0: pipeline-validation benchmark
- v1: initial discriminative benchmark
- v2: lexical/semantic/distractor stress benchmark

## Major experimental findings

### Finding 1

The first benchmark was too easy.

BM25 and dense both achieved perfect answerable rank behavior.

Lesson:

A benchmark that every system saturates cannot distinguish system quality.

### Finding 2

KnowledgeBench v1 exposed a semantic weakness in BM25.

Dense ranked a semantic paraphrase correctly at rank 1 while BM25 ranked it second.

### Finding 3

KnowledgeBench v2 exposed an opaque-identifier weakness in dense retrieval.

For:

```text
ERR-KV-4097
```

dense retrieval ranked the semantically near but lexically wrong `ERR-KV-4098` document first.

BM25 ranked the exact identifier first.

### Finding 4

Equal-weight RRF did not improve v2.

A symmetric rank swap caused equal RRF scores.

Therefore simple rank fusion is not automatically better than either component.

### Finding 5

Both fixed top-k retrievers fail the current unanswerable diagnostic.

They always return some nearest documents even when no relevant evidence exists.

Future systems need evidence sufficiency or abstention behavior.

## Phase 1 research questions answered

### Do lexical and dense retrieval have different failure modes?

Yes, on the current synthetic diagnostic benchmarks.

### Is hybrid retrieval automatically superior?

No.

Equal-weight RRF did not improve v2.

### Can one aggregate metric describe retrieval quality?

No.

Recall@3 saturated while Recall@1, MRR, and category slices exposed meaningful differences.

### Is the current benchmark sufficient for final claims?

No.

It is a small synthetic diagnostic benchmark intended for architecture and methodology development.

## Exit criteria

Phase 1 exit criteria are satisfied:

- [x] explain lexical vs dense retrieval
- [x] implement/test retrieval metrics
- [x] separate ground truth from outputs
- [x] define versioned task/corpus formats
- [x] run controlled BM25 vs dense comparisons
- [x] perform failure analysis
- [x] record a negative hybrid result
- [x] define experiment/leakage protocol
- [x] document high-level architecture
- [x] connect design to relevant literature
- [x] preserve reproducible experiment records

## What Phase 1 intentionally did not solve

- document ingestion from real sources
- chunking
- contextual chunks
- reranking
- large-scale indexing
- graph/hierarchical representations
- multi-hop search agents
- answer generation and citation grading
- abstention
- learned routing
- SFT
- RL

## Phase 2 starting point

Phase 2 should build the first real retrieval/data pipeline around documents rather than synthetic one-paragraph corpus entries.

Recommended sequence:

1. ingestion interface,
2. document -> chunk transformation,
3. chunk metadata and provenance,
4. lexical/dense indexing over chunks,
5. benchmark tasks requiring evidence across chunks,
6. chunking experiments,
7. contextual retrieval baseline,
8. reranking only after measuring retrieval failures.

The key principle remains:

```text
hypothesis
→ baseline
→ measurement
→ failure analysis
→ improvement
→ rerun
```
