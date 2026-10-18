# ADR-004: Use Retrieve-Then-Rerank for Close Candidate Disagreements

## Status

Accepted

## Context

Phase 2 showed a dense retrieval failure where:
- the correct chunk was present at rank 2,
- the score gap to rank 1 was small,
- contextualization improved but did not fully fix ranking.

A cross-encoder reranker corrected the ordering.

## Decision

Adopt retrieve-then-rerank as the preferred pattern when:
- first-stage retrieval recall is already adequate,
- the problem is candidate ordering.

Do not apply reranking as a blanket fix for missing candidates.

## Consequences

Benefits:
- improves precision without replacing fast retrieval,
- preserves precomputed dense indexes,
- gives a clean separation between candidate generation and candidate scoring.

Costs:
- adds latency,
- adds a second model,
- requires careful top-k candidate selection,
- still depends on first-stage recall.
