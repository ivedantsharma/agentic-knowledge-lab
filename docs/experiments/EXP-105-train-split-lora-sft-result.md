# EXP-105 Result: Train-Split LoRA Supervised Fine-Tuning

## Configuration

```text
model=Qwen/Qwen2.5-0.5B-Instruct
epochs=2
learning_rate=2e-4
train=12 examples
dev=3 examples
heldout=3 examples
LoRA r=4
target_modules=[q_proj, v_proj]
```

## Before training

```text
train:
  accuracy=0.0833
  format_compliance=1.0000
  predictions={
    SEARCH_HYBRID_K3: 10,
    SEARCH_HYBRID_K2: 2
  }

dev:
  accuracy=0.0000
  format_compliance=1.0000
  predictions={
    SEARCH_HYBRID_K3: 3
  }

heldout:
  accuracy=0.3333
  format_compliance=1.0000
  predictions={
    SEARCH_HYBRID_K3: 1,
    SEARCH_HYBRID_K2: 1,
    SEARCH_HYBRID_K1: 1
  }
```

## Training loss

```text
epoch 1 mean loss=0.396621
epoch 2 mean loss=0.184536
```

## After training

```text
train:
  accuracy=0.5833
  format_compliance=1.0000
  predictions={
    SEARCH_HYBRID_K5: 8,
    REFORMULATE: 2,
    SEARCH_HYBRID_K1: 2
  }

dev:
  accuracy=1.0000
  format_compliance=1.0000
  predictions={
    SEARCH_HYBRID_K5: 3
  }

heldout:
  accuracy=0.3333
  format_compliance=1.0000
  predictions={
    SEARCH_HYBRID_K5: 1,
    REFORMULATE: 1,
    SEARCH_HYBRID_K1: 1
  }
```

## Accuracy deltas

```text
train   +0.5000
dev     +1.0000
heldout +0.0000
```

## Interpretation

LoRA SFT changed policy behavior and substantially improved fit to the training set.

The unseen dev source task also improved to perfect accuracy.

However, the heldout source task did not improve.

The post-training model also shows a strong bias toward:

```text
SEARCH_HYBRID_K5
```

Therefore this is evidence of partial transfer, not broad policy generalization.

## Important dataset confound

Action classes are not independently represented across many source tasks.

Current source support includes:

- SEARCH_HYBRID_K5: two source tasks,
- SEARCH_HYBRID_K1: two source tasks,
- SEARCH_HYBRID_K2: one source task,
- REFORMULATE: one source task,
- SEARCH_HYBRID_K3: zero source tasks.

This makes source memorization and class learning difficult to separate for several actions.

## Decision

Do not tune epochs, learning rate, or LoRA rank yet.

First audit and improve action-class source diversity.
