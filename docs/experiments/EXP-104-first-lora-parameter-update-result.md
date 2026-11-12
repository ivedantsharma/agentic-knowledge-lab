# EXP-104 Result: First LoRA Parameter Update

## Validation

```text
261 tests passed
ruff passed
```

## Configuration

```text
model=Qwen/Qwen2.5-0.5B-Instruct
example=p11-train-001a
target=SEARCH_HYBRID_K5
steps=3
learning_rate=5e-4

LoRA:
  r=4
  alpha=8
  dropout=0
  target_modules=[q_proj, v_proj]
```

## Parameter efficiency

```text
total_parameters=494303104
trainable_parameters=270336
trainable_fraction=0.00054690
```

Only about 0.0547% of model parameters were trainable.

## Loss

```text
step 1=0.204247
step 2=0.119492
step 3=0.031394

initial_loss=0.204247
final_loss=0.006459
loss_delta=-0.197788
```

## Interpretation

The LoRA optimization path is mechanically valid.

The experiment demonstrates:

- base-model freezing,
- LoRA trainable parameters,
- backward propagation,
- optimizer updates,
- rapidly decreasing target-only loss.

## What it does not prove

This is a one-example memorization probe.

It does not demonstrate:

- train-set policy learning,
- dev generalization,
- heldout generalization,
- useful class discrimination.

## Decision

Proceed to full train-split LoRA SFT and evaluate train/dev/heldout separately.
