# EXP-108 Result: Measured Policy Dataset v1 Audit

## Validation

```text
269 tests passed
ruff passed
```

## Dataset

```text
examples=17
split_counts={
  dev: 3,
  train: 11,
  heldout: 3
}
action_counts={
  SEARCH_HYBRID_K5: 2,
  SEARCH_HYBRID_K1: 9,
  SEARCH_HYBRID_K2: 5,
  REFORMULATE: 1
}
evidence_families=6
family_leakage={}
```

## Evidence-family split

```text
dev:
  atlas_borealis

train:
  cirrus
  helios_solstice
  nimbus
  orion

heldout:
  security_meridian
```

## Interpretation

Dataset v1 passes the stricter leakage audit.

Unlike v0:

- every example has an individually measured oracle label,
- shared-evidence families do not cross splits.

## Remaining limitations

The class distribution remains imbalanced:

```text
K1=9
K2=5
K5=2
REFORMULATE=1
K3=0
```

Therefore this dataset supports a cleaner SFT comparison but still does not support broad claims for all five policy actions.

## Decision

Retrain LoRA using the same optimization configuration as EXP-105.

Only the dataset/split changes.

This isolates the effect of improved label validity and leakage control.
