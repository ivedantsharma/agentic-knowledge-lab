# Phase 5 Failure Taxonomy

## Purpose

Hierarchical retrieval introduces failure modes that flat retrieval does not expose clearly.

A final retrieval miss should be assigned to the stage that caused it before changing architecture.

## 1. Parent-routing failure

The correct document falls outside the parent beam.

Observed in EXP-042 with strict top-1 parent routing.

```text
correct parent rank = 2
parent beam = 1
→ evidence unreachable
```

Repair:

```text
parent beam 1 → 2
```

## 2. Within-parent section-ranking failure

The correct document is selected, but the wrong section ranks first.

Observed with Cirrus in the early hierarchical baseline.

Dense retrieval preferred:

```text
Retry Policy
```

over:

```text
Dead Letter Handling
```

Repair:

Use a local cross-encoder for section reranking.

## 3. Pooled-section distractor failure

The correct parent is present, but a semantically similar section from another retained parent outranks the correct section.

This showed that parent recall alone does not imply end-to-end success.

## 4. Premature child collapse

The relevant section ranks second and is discarded by child top-1.

Observed in the Cirrus parent-stress benchmark.

Repair:

Retain a small section beam.

## 5. Evidence fragmentation

An answer span crosses a chunk boundary and no individual chunk contains the complete labeled evidence.

Observed with Borealis:

```text
"... incremental backups run every"
"backups run every six hours."
```

Repair:

Chunk overlap.

## 6. Candidate concentration

Multiple chunks from one distractor section occupy the global chunk beam.

Observed with Cirrus after overlap repair.

Symptom:

```text
top chunk 1 → distractor section
top chunk 2 → same distractor section
relevant chunk → global rank 4
```

Repair:

Rank chunks locally inside each retained section instead of using one global chunk top-k.

## 7. Directional neighbor failure

The anchor chunk is near the answer, but selecting only the higher-scoring adjacent neighbor chooses the wrong direction.

Observed on the long-section Cirrus task.

The returned window ended immediately before:

```text
CIRRUS-DLQ
```

Repair:

Bidirectional radius-1 expansion.

## 8. Overlap duplication

Returning overlapping chunks directly repeats text and can make chunk-level context larger than the original section.

Repair:

Merge source word ranges and reconstruct a deduplicated source window.

## 9. Benchmark-scale failure

The method is intended to reduce context, but the benchmark sections are so short that local windows reconstruct the entire section.

Observed in EXP-049:

```text
AvgDeduplicatedWindowWords=23.33
AvgRetainedSectionWords=23.33
```

This was not an architecture failure.

It was a benchmark incapable of measuring the intended benefit.

Repair:

Introduce longer sections while keeping the retrieval policy fixed.

## 10. Context-recall tradeoff failure

Aggressive context reduction preserves less evidence.

Observed in EXP-050:

```text
EvidenceRetentionRate=0.6667
ReductionVsSections=0.6434
```

The correct response is not to optimize one metric in isolation.

Evaluate the recall/context Pareto frontier.

## Diagnostic order

When a hierarchical retrieval task fails, inspect in this order:

```text
1. Was the correct parent inside the beam?
2. Was the correct section inside the section beam?
3. Does any chunk contain the evidence?
4. Where does the evidence chunk rank locally?
5. Is another section monopolizing the global candidates?
6. Does the local context window cover the answer boundary?
7. Is overlap duplicating unnecessary returned context?
```

## Research lesson

Hierarchical retrieval failures are often routing or representation failures rather than simple semantic-search failures.

Changing the model before locating the failing stage can hide the actual cause.
