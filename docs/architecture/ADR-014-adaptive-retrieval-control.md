# ADR-014: Adaptive Retrieval Should Control Strategy, Budget, and Query State

## Status

Accepted.

## Context

A single fixed retrieval configuration is simple but cannot optimally handle all query types.

Phase 10 studied:

- retriever selection,
- retrieval budget,
- query transformation.

## Evidence

### Retriever routing

Oracle headroom above fixed Hybrid was only:

```text
+0.0417 MRR
```

with 11/12 paired tasks tied.

### Budget adaptation

Minimal useful k varied from:

```text
1 to 5
```

across hard tasks.

### Query transformation

Decomposition repaired part of a saturated multi-hop failure:

```text
0.3333 → 0.6667 recall
```

but exposed relation and stale-evidence errors.

### Literal qualifier preservation

Did not improve aggregate recall.

## Decision

Represent adaptive retrieval as a multi-axis control problem.

The retrieval policy should eventually choose:

```text
strategy
query
budget
```

while maintaining structured state about:

```text
entities
relations
qualifiers
temporal constraints
retrieval history
```

## Rejected alternatives

### One global retriever

Rejected because per-query winners differ.

### Complex learned retriever router immediately

Rejected because oracle headroom is too small on the current benchmark.

### Always increase top-k

Rejected because some tasks saturate before full evidence is recovered.

### Prompt/query wording tweaks alone

Rejected because EXP-100 showed no gain from literal qualifier preservation.

## Consequence

Phase 11/12 policy learning should optimize action selection over retrieval controls rather than train a narrow BM25-vs-Dense classifier.
