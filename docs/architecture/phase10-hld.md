# Phase 10 High-Level Design

## Goal

Move from fixed retrieval toward a system that adapts search behavior to the query.

The phase studied three adaptation axes:

```text
which retriever?
how many candidates?
how should the query be transformed?
```

## Architecture

```text
query
  ↓
query understanding
  ↓
retrieval policy
  ├─ strategy selection
  ├─ budget selection
  └─ query transformation
  ↓
retriever
  ↓
evidence
```

## Findings

### Retriever selection

BM25, Dense, and Hybrid have different per-query behavior.

However, oracle routing headroom was modest.

On the paired benchmark:

```text
best fixed Hybrid MRR=0.8333
oracle MRR=0.8750
headroom=0.0417
```

with 11/12 tasks tied.

Conclusion:

```text
retriever identity is not the strongest adaptation axis here
```

### Retrieval budget

Budget requirements varied strongly:

```text
k=1,2,3,5 depending on task
```

Fixed-k recall ranged from:

```text
0.5556 at k=1
to
0.8889 at k=5
```

Conclusion:

```text
adaptive top-k has real value
```

### Query transformation

Oracle decomposition improved a saturated multi-hop case:

```text
0.3333 → 0.6667
```

but did not improve aggregate recall.

Conclusion:

```text
decomposition can expose missing evidence
but does not guarantee correct relation/temporal retrieval
```

### Qualifier preservation

Adding literal words such as current/production did not repair the remaining failures.

Conclusion:

```text
query rewriting needs structured state,
not merely additional wording
```

## Proposed adaptive retrieval policy abstraction

Future policy-learning phases should reason over:

```text
query features
retrieval signals
retrieval history
entity/relation state
temporal constraints
candidate budget
```

and choose actions such as:

```text
SEARCH(strategy, query, k)
REFORMULATE(query)
EXPAND_BUDGET(k)
STOP
```

## Limitations

- very small synthetic benchmark,
- only BM25, MiniLM, and RRF in direct routing comparison,
- no learned router,
- oracle transformations use benchmark knowledge,
- no calibrated latency model,
- no end-to-end answer metric for every Phase 10 experiment.

Phase 10 establishes the control problem, not the final learned policy.
