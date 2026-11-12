# Phase 11: LoRA / PEFT Foundations

## Why not full fine-tuning first?

Full fine-tuning updates every trainable parameter in the base language model.

For a model with hundreds of millions of parameters, that increases:

- optimizer memory,
- gradient memory,
- checkpoint size,
- risk of damaging general capabilities.

For our first policy-learning experiment this is unnecessary.

## LoRA intuition

Suppose a pretrained linear layer has weight matrix:

```text
W
```

Standard fine-tuning learns a full update:

```text
W + ΔW
```

LoRA freezes `W` and represents the update approximately as:

```text
ΔW = B A
```

where `A` and `B` are much smaller low-rank matrices.

If the original matrix is large but the chosen rank is small, the number of trainable parameters drops dramatically.

## What stays frozen?

The pretrained Qwen backbone remains frozen.

For EXP-104 we attach LoRA adapters to attention projections:

```text
q_proj
v_proj
```

and train only those adapter parameters.

## Why q_proj and v_proj?

This is a small mechanics experiment, not a final architecture search.

Restricting LoRA to two attention projections keeps the trainable parameter count and CPU memory lower while still creating a genuine learned modification to the model.

## EXP-104 goal

EXP-104 intentionally trains on one example for a few gradient steps.

This is called an overfit or memorization probe.

Success means:

- LoRA parameters are the only trainable parameters,
- gradients propagate,
- optimizer updates occur,
- target-only loss decreases.

Success does **not** mean the retrieval policy generalizes.

Generalization is tested only after training on the full train split and evaluating dev/heldout data.
