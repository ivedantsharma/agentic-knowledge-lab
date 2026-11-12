# EXP-106 Result: Action-Class Source-Support Audit

## Validation

```text
264 tests passed
ruff passed
```

## Results

### SEARCH_HYBRID_K1

```text
source_count=2
sources=[
  kbv2-hard-007,
  kbv2-hard-010
]
train source=kbv2-hard-007
heldout source=kbv2-hard-010
source_disjoint_evaluable=True
```

### SEARCH_HYBRID_K2

```text
source_count=1
sources=[kbv2-hard-006]
source_disjoint_evaluable=False
```

### SEARCH_HYBRID_K3

```text
source_count=0
source_disjoint_evaluable=False
```

### SEARCH_HYBRID_K5

```text
source_count=2
sources=[
  kbv2-hard-001,
  kbv2-hard-002
]
train source=kbv2-hard-001
dev source=kbv2-hard-002
source_disjoint_evaluable=True
```

### REFORMULATE

```text
source_count=1
sources=[kbv2-hard-005]
source_disjoint_evaluable=False
```

## Summary

```text
action_classes=5
source_disjoint_evaluable_classes=2
insufficient_classes=3
```

## Interpretation

Only K1 and K5 currently support source-disjoint class evaluation.

K2 and REFORMULATE are confounded with one source task each.

K3 has no positive source at all.

Therefore further SFT hyperparameter tuning would be premature.

## Decision

Search the existing benchmark for additional independently oracle-labelable policy examples before creating new synthetic source tasks.
