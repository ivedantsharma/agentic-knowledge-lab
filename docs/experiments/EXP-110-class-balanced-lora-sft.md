# EXP-110: Class-Balanced Measured v1 LoRA SFT

## Research question

Was the all-K1 collapse in EXP-109 primarily caused by class imbalance?

## Controlled change

Keep fixed from EXP-109:

- measured dataset v1,
- evidence-family splits,
- Qwen2.5-0.5B-Instruct,
- LoRA r=4,
- alpha=8,
- q_proj + v_proj,
- learning rate=2e-4,
- epochs=2,
- AdamW,
- target-only causal-LM loss.

Change only:

```text
training example sampling distribution
```

## Balancing method

Oversample each action class present in the training split until every present class has the same effective number of examples.

No synthetic query text is created.

Existing examples are repeated.

## Why oversampling?

EXP-109 training data is strongly imbalanced toward K1.

The model collapsed to K1 on every train, dev, and heldout query.

If balancing removes that collapse, class frequency was an important cause.

If balancing still fails to generalize, the deeper limitation is likely data diversity / query-policy learnability rather than simple frequency.

## What stays unsupported?

SEARCH_HYBRID_K3 still has no positive examples.

Oversampling cannot create missing semantic coverage.

## Metrics

Before and after training:

- train accuracy,
- dev accuracy,
- heldout accuracy,
- prediction distribution.

Training:

- original class counts,
- balanced effective counts,
- epoch mean loss.

## Interpretation

The key result is not just accuracy.

We specifically test whether prediction collapse disappears and whether heldout K2 behavior improves.
