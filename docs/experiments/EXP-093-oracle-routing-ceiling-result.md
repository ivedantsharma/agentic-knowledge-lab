# EXP-093 Result: Fixed Retriever Comparison and Oracle Routing Ceiling

## Validation

```text
241 tests passed
ruff passed
```

## Fixed retrievers

### BM25

```text
mean_supporting_recall=0.7778
mean_reciprocal_rank=0.9167
mean_chain_coverage=0.6667
```

### Dense MiniLM

```text
mean_supporting_recall=0.7500
mean_reciprocal_rank=0.8333
mean_chain_coverage=0.6250
```

### Hybrid RRF

```text
mean_supporting_recall=0.6944
mean_reciprocal_rank=0.8889
mean_chain_coverage=0.5417
```

## Oracle ceiling

```text
mean_oracle_supporting_recall=0.8333
mean_oracle_reciprocal_rank=0.9167
unique_winner_counts={'dense': 1, 'bm25': 2}
tied_tasks=3
```

## Per-task winners

```text
kbv2-hard-001 → dense
kbv2-hard-002 → bm25
kbv2-hard-005 → bm25
kbv2-hard-006 → tie
kbv2-hard-007 → tie
kbv2-hard-010 → dense/hybrid tie
```

## Interpretation

Adaptive routing has measurable but modest headroom.

Compared with the best fixed retriever:

```text
Supporting Recall@3
0.7778 → 0.8333
```

Absolute gain:

```text
+0.0555...
```

The oracle does not improve MRR beyond BM25.

Therefore the benchmark does not justify a complex learned router yet.

However, different strategies do uniquely win different tasks, so query-dependent strategy selection is not vacuous.

## Hybrid finding

Equal-weight RRF was never the unique best strategy.

This repeats the earlier Phase 1 lesson that fusion is not automatically superior.

## Next step

Before introducing a router, inspect observable query features associated with strategy wins.

The router must use only information available from the query at inference time, not benchmark challenge labels or gold evidence.
