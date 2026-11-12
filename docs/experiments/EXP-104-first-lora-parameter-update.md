# EXP-104: First LoRA Parameter Update

## Research question

Can a small LoRA adapter receive gradients and reduce target-only retrieval-policy loss on one training example?

## Why one example?

This experiment is not evaluating generalization.

It is an optimization mechanics probe.

Before training on the full split, we need to establish:

```text
forward pass
→ target-only loss
→ backward pass
→ gradients
→ optimizer step
→ changed loss
```

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## Parameter-efficient adaptation

LoRA configuration:

```text
rank r=4
alpha=8
dropout=0
target modules:
  q_proj
  v_proj
```

The base parameters remain frozen.

## Training

```text
examples=1
steps=3
learning_rate=5e-4
optimizer=AdamW
loss=target-only causal-LM cross entropy
```

## Metrics

- total parameter count,
- trainable parameter count,
- trainable fraction,
- initial target-only loss,
- per-step training loss,
- final target-only loss,
- loss delta.

## Success criterion

The experiment is mechanically successful if:

1. trainable parameters are a small fraction of total parameters,
2. backward/optimizer steps complete,
3. final target loss is lower than initial target loss.

## What this does not prove

It does not prove:

- dev improvement,
- heldout generalization,
- a useful retrieval policy,
- superiority of this LoRA configuration.

Those require later experiments.

## Dependency

EXP-104 uses Hugging Face PEFT.

The experiment is pinned to:

```text
peft==0.21.2
```

for reproducibility.
