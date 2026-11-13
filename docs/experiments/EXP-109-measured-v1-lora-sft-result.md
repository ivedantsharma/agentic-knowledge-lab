# EXP-109 Result: Measured Dataset v1 LoRA SFT

## Configuration

```text
model=Qwen/Qwen2.5-0.5B-Instruct
epochs=2
learning_rate=2e-4
train_examples=11
dev_examples=3
heldout_examples=3
LoRA r=4
target_modules=[q_proj, v_proj]
```

## Before training

```text
train accuracy=0.1818
dev accuracy=0.0000
heldout accuracy=0.3333
```

The frozen model remained strongly biased toward SEARCH_HYBRID_K3.

## Training loss

```text
epoch 1 mean loss=0.233535
epoch 2 mean loss=0.138683
```

## After training

```text
train accuracy=0.6364
dev accuracy=0.6667
heldout accuracy=0.0000
```

Prediction distribution after training:

```text
train:
  SEARCH_HYBRID_K1 = 11 / 11

dev:
  SEARCH_HYBRID_K1 = 3 / 3

heldout:
  SEARCH_HYBRID_K1 = 3 / 3
```

## Accuracy deltas

```text
train   +0.4545
dev     +0.6667
heldout -0.3333
```

## Interpretation

The adapter learned a degenerate majority-class policy.

Loss decreased and apparent train/dev accuracy increased, but the model collapsed to:

```text
SEARCH_HYBRID_K1
```

for every evaluated query.

Therefore target-only loss reduction is not sufficient evidence of policy learning.

The clean v1 dataset exposes a failure that the noisier v0 dataset partially obscured.

## Likely mechanism

The training set is class-imbalanced.

K1 is the dominant action, while K5 and REFORMULATE are rare.

With only 11 training examples, predicting the majority class is an easy optimization path.

## Decision

Run one controlled class-balancing experiment before Phase 11 closeout.

Keep fixed:

- model,
- LoRA configuration,
- optimizer,
- learning rate,
- epochs,
- measured v1 labels,
- evidence-family splits.

Change only the effective class sampling distribution.
