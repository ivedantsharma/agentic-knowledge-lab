# Phase 2 Final Closeout

## Status

Phase 2 complete.

## Final capability

The project can now:

1. ingest a real Markdown file,
2. preserve heading structure,
3. represent sections as typed data,
4. chunk documents using multiple strategies,
5. preserve source provenance,
6. derive chunk relevance from source evidence,
7. run dense retrieval,
8. inspect retrieval-score failures,
9. rerank candidates with a cross-encoder,
10. evaluate chunking strategies with KnowledgeBench.

## Key experimental conclusions

### Fixed chunk size matters

Very small chunks can fragment evidence.

### Overlap is not free

Overlap can repair boundaries but increase redundancy and hurt top-k diversity.

### Larger chunks can preserve useful context

30-word chunks outperformed smaller fixed chunks on the current corpus.

### Native structure is useful

Section-aware chunks improved over small arbitrary chunks.

### Parent context can help

Document/section context improved ranking for the Cirrus failure.

### More contextual prose is not automatically better

Rich manually authored context did not outperform the simpler parent prefix.

### Reranking is valuable when recall is already good

The cross-encoder fixed a rank-order error when the relevant chunk was already in dense top-3.

## Architecture at Phase 2 exit

```text
real source file
↓
format parser
↓
StructuredDocument
↓
chunking strategy
↓
DocumentChunk[]
↓
first-stage retrieval
↓
candidate set
↓
optional cross-encoder reranking
↓
RunResult
↓
KnowledgeBench
```

## Phase 3 handoff

Phase 3 should move beyond single-chunk, single-hop retrieval.

Recommended focus:

- multi-document tasks,
- multi-hop evidence chains,
- hierarchical retrieval,
- graph/claim-evidence representations,
- retrieval planning,
- evidence aggregation,
- verification,
- agent traces and tool-use metrics.

The central Phase 3 question becomes:

> When one retrieval step is not enough, how should an agent plan and execute a sequence of searches over richer information structures?
