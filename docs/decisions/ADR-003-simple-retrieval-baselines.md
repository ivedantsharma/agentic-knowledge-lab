# ADR-003: Keep Simple Retrieval Baselines Before Learned Fusion

## Status

Accepted

## Context

Phase 1 established:
- BM25 baseline,
- dense baseline,
- equal-weight RRF hybrid baseline.

RRF failed to improve KnowledgeBench v2.

The current benchmark is too small to safely tune fusion weights.

## Decision

Keep BM25, dense, and equal-weight RRF as transparent baselines.

Do not tune weighted fusion, thresholds, or learned routing on Phase 1 evaluation examples.

Revisit hybrid optimization only after a larger train/dev/test structure exists.

## Consequences

Benefits:
- avoids benchmark overfitting,
- preserves interpretable baselines,
- makes future improvements measurable.

Cost:
- Phase 1 knowingly leaves retrieval performance on the table.
