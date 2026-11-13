# EXP-110 Result: Class-Balanced Measured v1 LoRA SFT

## Configuration

```text
model=Qwen/Qwen2.5-0.5B-Instruct
epochs=2
learning_rate=2e-4
original_train_examples=11
balanced_train_examples=28
dev_examples=3
heldout_examples=3
```

Training distribution:

```text
original:
  SEARCH_HYBRID_K1=7
  SEARCH_HYBRID_K2=2
  SEARCH_HYBRID_K5=1
  REFORMULATE=1

balanced:
  SEARCH_HYBRID_K1=7
  SEARCH_HYBRID_K2=7
  SEARCH_HYBRID_K5=7
  REFORMULATE=7
```

## Before training

```text
train accuracy=0.1818
dev accuracy=0.0000
heldout accuracy=0.3333
```

## Training loss

```text
epoch 1 mean loss=0.194812
epoch 2 mean loss=0.087429
```

## After training

```text
train accuracy=0.9091
dev accuracy=1.0000
heldout accuracy=0.6667
```

Prediction distribution no longer collapsed to one class.

Train predictions:

```text
SEARCH_HYBRID_K1=6
SEARCH_HYBRID_K2=3
SEARCH_HYBRID_K5=1
REFORMULATE=1
```

Heldout:

```text
SEARCH_HYBRID_K2=2
SEARCH_HYBRID_K1=1
```

## Accuracy deltas

```text
train   +0.7273
dev     +1.0000
heldout +0.3333
```

## Interpretation

Class balancing resolved the all-K1 collapse observed in EXP-109.

This establishes that class frequency was a major optimization shortcut in the tiny Phase 11 dataset.

The adapter also transferred partially to the evidence-family-disjoint heldout Meridian family:

```text
0.3333 → 0.6667
```

This is stronger evidence of learned retrieval-policy behavior than EXP-105 or EXP-109.

## What this proves

Within this controlled synthetic setting:

- LoRA SFT can learn retrieval-action mappings,
- target-only causal-LM training works,
- measured oracle labels are preferable to inherited labels,
- evidence-family leakage control matters,
- class-balanced sampling prevents a dominant-class shortcut,
- some source/evidence-family-disjoint transfer is possible.

## What this does not prove

It does not establish:

- broad retrieval-policy generalization,
- competence on SEARCH_HYBRID_K3,
- robust REFORMULATE behavior across independent families,
- optimal LoRA hyperparameters,
- real-world production performance.

## Decision

Close Phase 11.

Move to Phase 12 with a learned-policy baseline and use reward-based trajectory optimization rather than further tuning this tiny supervised benchmark.
