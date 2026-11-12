# EXP-105: Train-Split LoRA Supervised Fine-Tuning

## Research question

Does LoRA SFT on the 12-example training split improve retrieval-policy action prediction, and does any improvement transfer to source-task-disjoint dev and heldout examples?

## Why this is the first generalization experiment

EXP-104 trained on one example and only tested whether optimization worked.

EXP-105 uses:

```text
train=12 examples / 4 source tasks
dev=3 examples / 1 unseen source task
heldout=3 examples / 1 unseen source task
```

Therefore we can distinguish:

```text
memorization
from
source-task generalization
```

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## LoRA

```text
r=4
alpha=8
dropout=0
target_modules=[q_proj, v_proj]
```

## Training

```text
epochs=2
learning_rate=2e-4
optimizer=AdamW
batch size=1
target-only causal-LM loss
```

No dev-driven hyperparameter tuning is performed in this experiment.

## Evaluation

Evaluate the same LoRA-wrapped model:

1. before training,
2. after training.

Report separately for:

- train,
- dev,
- heldout.

Metrics:

- exact action accuracy,
- format compliance,
- prediction distribution.

## Interpretation

Possible outcomes:

### Train improves, dev/heldout do not

The adapter learned training patterns but did not generalize.

### Train and dev improve, heldout does not

Some transfer exists, but generalization is unstable.

### Train/dev/heldout improve

Promising evidence for learned policy behavior, still limited by tiny synthetic data.

### Prediction collapses to one action

Loss reduction alone is misleading; the policy has become degenerate.

## Important limitation

The dev and heldout sets each contain only one source task with three paraphrases.

Accuracy therefore has very high variance.

No broad performance claim is justified from EXP-105 alone.
