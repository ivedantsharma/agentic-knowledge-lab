# EXP-053: Deterministic Claim-Graph Traversal Baseline

## Research question

Given the correct start entity and relation path, can a typed claim/evidence graph reproduce the Phase 3 multi-hop answers while preserving claim-level provenance?

## Source facts

The graph is derived from the existing Phase 3 v3 multi-hop corpus.

This avoids inventing a separate fact set for Phase 6.

## Input

Each task provides:

- natural-language question,
- start entity ID,
- gold relation path,
- expected answer,
- expected claim path.

## Traversal

Example:

```text
Atlas
--operated_by-->
Platform Reliability
--maintains_storage_system-->
Borealis
--incremental_backup_cadence-->
"every six hours"
```

Each edge also contains an evidence reference to the source document.

## Metrics

- AnswerAccuracy
- PathAccuracy
- ProvenanceCoverage

## What this experiment does not test

It does not test:

- entity linking from natural language,
- relation extraction,
- autonomous graph planning,
- fuzzy graph search,
- graph/text hybrid retrieval.

Those are intentionally deferred.

## Hypothesis

All four Phase 3-derived tasks should traverse exactly when supplied with their gold relation paths.

If they do not, the graph representation or traversal code is wrong.
