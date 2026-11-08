# Phase 5 Final Review

## Status

Research and implementation complete.

Repository-wide final validation remains the last closeout gate before the roadmap is marked complete.

## Central question

> Can hierarchical retrieval improve evidence discovery while controlling context size and search cost?

For the controlled synthetic benchmarks used in Phase 5:

> Yes. A coarse-to-fine document → section → chunk pipeline preserved all final benchmark evidence while returning substantially less context than full retained sections.

## What was built

### Hierarchical retrieval foundations

- document summaries
- document-first dense routing
- section-level retrieval
- parent/child metrics
- hierarchical stress corpus

### Strong local ranking

- cross-encoder section reranking
- parent beam search
- section beam retention

### Three-level hierarchy

- hierarchy-aware section chunking
- document and section ancestry
- chunk overlap
- local chunk scoring
- neighbor expansion
- deduplicated source windows

### Reusable system

- HierarchicalRetrievalConfig
- HierarchicalEvidenceWindow
- HierarchicalRetrievalResult
- CoarseToFineHierarchicalRetriever
- final integration benchmark

## Experiment progression

### EXP-039

Hierarchy reduced the child candidate set but did not improve accuracy by itself.

### EXP-040

Query refinement did not fix the Cirrus child-ranking failure.

Negative result: stop tuning query wording.

### EXP-041

Cross-encoder child reranking repaired the within-document Cirrus ambiguity.

### EXP-042

Hard parent distractors broke strict top-1 routing.

Parent beam 2 restored parent recall.

### EXP-043

The Cirrus relevant section was rank 2, not deeply buried.

### EXP-044

Parent beam 2 + section beam 2 preserved all answer-bearing sections.

### EXP-045 / EXP-046

Chunking introduced evidence fragmentation.

Overlap repaired the missing span.

### EXP-047

The Cirrus answer chunk was rank 2 locally but rank 4 globally.

This diagnosed candidate concentration.

### EXP-048

Section-aware neighbor expansion restored evidence retention to 1.0.

### EXP-049

Deduplicating overlapping chunk windows reduced redundant context, but short sections prevented improvement versus full sections.

### EXP-050

Long sections demonstrated the intended context benefit:

```text
ReductionVsSections=0.6434
```

but evidence retention fell to 0.6667.

### EXP-051

Bidirectional radius-1 expansion restored:

```text
EvidenceRetentionRate=1.0000
ReductionVsSections=0.5455
```

### Final reusable benchmark

```text
EvidenceRetentionRate=1.0000
AvgReturnedWindowWords=43.33
```

The reusable retriever reproduced the accepted experimental behavior.

## Main research lessons

### 1. Hierarchy introduces routing bottlenecks

A correct child is useless if its parent is pruned.

### 2. Parent recall and end-to-end success are different metrics

A correct parent inside the beam does not guarantee correct section ranking.

### 3. Strong models are most useful after narrowing

The cross-encoder is more expensive than the dense retriever, so applying it locally gives a natural cost-quality allocation.

### 4. Avoid premature top-1 decisions

Small beams protected evidence at both parent and section levels.

### 5. Chunk overlap solves fragmentation, not ranking

Overlap made missing evidence spans available but did not automatically rank them correctly.

### 6. Preserve hierarchy at the chunk stage

Global chunk top-k can destroy section diversity.

### 7. Retrieval representation and returned context can differ

Overlapping chunks are useful for ranking.

Deduplicated source windows are better for downstream context.

### 8. Optimize a Pareto frontier

The smallest context window is not necessarily the best retrieval policy.

Phase 5 selected the higher-recall radius-1 operating point.

### 9. Benchmark design matters

Short sections could not demonstrate context localization.

A longer-section stress corpus was required to test the intended benefit.

### 10. Stop tuning once the mechanism is understood

The Phase 5 benchmark is synthetic and development-influenced.

The accepted constants should not be repeatedly optimized on the same three tasks.

## Final reference policy

```text
MiniLM document routing
→ parent beam 2
→ cross-encoder section reranking
→ section beam 2
→ 10-word local chunks
→ 3-word overlap
→ cross-encoder local chunk ranking
→ best local chunk
→ radius-1 expansion
→ deduplicated source window
```

## Limitations

- synthetic corpus,
- three final answerable tasks,
- development-influenced stress cases,
- no latency benchmark,
- no production-scale index,
- fixed rather than adaptive beam widths,
- fixed chunk parameters.

These limitations are documented rather than hidden.

## Why Phase 5 stops here

The research objective was to understand hierarchical retrieval mechanics and failure modes, not to optimize a production search engine.

The phase now has:

- controlled baselines,
- negative results,
- ablations,
- hard distractors,
- recall/context tradeoff analysis,
- reusable implementation,
- final integration benchmark,
- explicit failure taxonomy,
- architecture decision record.

Further tuning on the same benchmark would risk overfitting.

## Next phase

Phase 6:

# Knowledge Graph & Claim/Evidence Retrieval

The next research question is:

> When relationships between entities and claims matter, can explicit graph structure improve retrieval beyond hierarchical text navigation?
