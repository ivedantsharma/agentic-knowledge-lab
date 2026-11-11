# EXP-100 Result: Qualifier-Preserving Query Transformation

## Validation

```text
255 tests passed
ruff passed
```

## Per-task results

### kbv2-hard-001

```text
baseline recall=0.6667
qualifier-preserved recall=0.6667
```

The intermediate query still retrieved Atlas ownership instead of the Platform Reliability production-storage bridge.

### kbv2-hard-005

```text
baseline recall=0.6667
qualifier-preserved recall=0.6667
```

The final query still retrieved the stale Solstice policy instead of the current policy.

### kbv2-hard-006

```text
baseline recall=1.0000
qualifier-preserved recall=1.0000
```

No change.

## Aggregate

```text
baseline_mean_recall=0.7778
qualifier_preserved_mean_recall=0.7778
```

## Interpretation

Literal qualifier preservation did not improve retrieval.

Therefore the failure cannot be reduced to simply dropping words like:

- current,
- production.

The remaining errors are structural:

- relation-selection failure on the intermediate bridge,
- temporal-version ranking failure on stale vs current evidence.

## Decision

Do not continue a wording-tweak treadmill.

Phase 10 should close with the conclusion that adaptive retrieval requires multiple control axes:

1. retriever selection,
2. retrieval budget,
3. query transformation,
4. structured relation/temporal state.

The first three were directly studied here; the fourth is supported by the observed failure modes and earlier Phase 3/6 mechanisms.

Automatic learning of these decisions belongs in later policy-learning phases.
