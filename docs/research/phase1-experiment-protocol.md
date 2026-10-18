# Phase 1 Experiment Protocol and Dataset Versioning

## Purpose

This document defines how retrieval experiments should be run so results remain interpretable and reproducible.

## 1. Dataset roles

Use three conceptual partitions once datasets become large enough:

- train: for learned components
- dev: for design choices, thresholds, fusion weights, prompts, and hyperparameters
- test: for final evaluation only

The current Phase 1 datasets are synthetic diagnostic datasets, not final held-out test sets.

They must not be treated as evidence of production-level performance.

## 2. Versioning

Never silently modify an existing benchmark version after reporting results.

Create a new version instead.

Examples:

```text
knowledgebench_phase1_v0
knowledgebench_phase1_v1
knowledgebench_phase1_v2
```

Each reported experiment must name the exact dataset version.

## 3. Controlled comparisons

When comparing two retrieval methods, keep fixed where possible:

- task set
- corpus
- relevance judgments
- top-k
- evaluator
- metrics
- embedding model when dense retrieval is not the variable
- preprocessing/tokenization unless explicitly under study

Change one meaningful variable at a time.

## 4. Primary retrieval metrics

Use:

- Recall@1 for rank-1 retrieval quality
- Recall@K for coverage
- Precision@K for retrieved-set purity
- MRR for first-relevant rank sensitivity
- category-level slices

Do not rely only on one aggregate metric.

## 5. Unanswerable tasks

Do not mix tasks with empty relevance sets into ordinary Recall/MRR averages.

Track them separately.

Current diagnostic:

```text
unanswerable retrieval rate
```

Later phases should add abstention/evidence-sufficiency metrics.

## 6. Missing outputs

If a benchmark task has no system result, treat it as a failure rather than silently removing it from evaluation.

## 7. Negative results

Record negative results.

Do not keep changing parameters until the system wins.

Example:

Equal-weight RRF failed to improve over dense retrieval on v2.

That is a valid result.

## 8. Hyperparameter tuning

Do not tune on the final test set.

Thresholds, weights, prompts, and learned policies must be selected using train/dev data.

## 9. Experiment record

Each meaningful experiment should record:

- question/hypothesis
- dataset version
- corpus version
- system configuration
- metrics
- category slices
- qualitative failures
- interpretation
- next decision

## 10. Reproducibility

Where stochastic behavior exists later, record:

- random seed
- model/version
- prompt version
- tool configuration
- number of trials

Phase 1 retrieval baselines are mostly deterministic, so repeated trials are not yet necessary.
