# Phase 10 Foundations: Adaptive Retrieval and Query Understanding

## Central question

> Can a knowledge system choose a better retrieval strategy from the structure of the query instead of using one retriever for every task?

## Why adaptive retrieval?

Different retrieval methods have different inductive biases.

### BM25

Strong when exact lexical overlap matters.

### Dense retrieval

Strong when semantic similarity matters despite wording differences.

### Hybrid retrieval

Can combine lexical and semantic evidence, but fusion is not automatically better.

### Hierarchical retrieval

Useful when the search space has document/section/chunk structure.

### Graph retrieval

Useful when the question requires explicit entity-relation traversal.

The Phase 10 goal is not to declare one architecture globally best.

It is to learn:

```text
query properties
→ retrieval strategy
→ search budget
```

## Research sequence

1. fixed retriever comparison,
2. oracle routing ceiling,
3. query-feature taxonomy,
4. rule-based router,
5. routing evaluation,
6. adaptive top-k,
7. query transformation,
8. learned/semantic routing if justified.

## Scientific rule

Do not build a router until there is measurable routing headroom.

If one fixed retriever dominates all tasks, routing adds complexity without evidence of benefit.

## EXP-093 scope

Start with retrieval strategies that operate directly on the same KnowledgeBench v2 hard corpus:

- BM25,
- Dense MiniLM,
- equal-weight BM25 + Dense RRF.

Hierarchical and graph routing use different representations and will be integrated later after the routing evaluation contract is established.

## Oracle definition

For each answerable task, the oracle compares strategies by:

1. Supporting Recall@3,
2. Reciprocal Rank as tie-break.

The oracle is not a deployable system.

It is an upper-bound diagnostic answering:

> If we knew which fixed retriever would perform best for each query, how much could routing improve retrieval?

## Unanswerable tasks

EXP-093 deliberately excludes unanswerable tasks from retriever-selection scoring.

For them, the important routing decision is not merely:

```text
BM25 vs Dense
```

but potentially:

```text
search vs clarify vs abstain
```

That becomes a later Phase 10 routing action.
