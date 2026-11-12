# EXP-109: Measured Dataset v1 LoRA SFT

## Research question

Does LoRA SFT behave differently when trained on individually oracle-labeled examples with evidence-family-disjoint evaluation?

## Controlled comparison to EXP-105

Keep fixed:

```text
model=Qwen/Qwen2.5-0.5B-Instruct
LoRA r=4
alpha=8
dropout=0
target_modules=[q_proj, v_proj]
epochs=2
learning_rate=2e-4
optimizer=AdamW
batch size=1
target-only loss
```

Change only:

```text
dataset v0
→ measured dataset v1
```

## Why this comparison matters

EXP-105 used inherited paraphrase labels and only source-task-disjoint splits.

EXP-107 showed that paraphrases can change the oracle action.

EXP-108 built v1 with:

- individually measured labels,
- evidence-family-disjoint splits.

Therefore EXP-109 tests whether the apparent generalization in EXP-105 survives stricter data construction.

## Metrics

Before and after SFT:

- train exact action accuracy,
- dev exact action accuracy,
- heldout exact action accuracy,
- format compliance,
- prediction distribution.

Training:

- epoch mean target-only loss.

## Interpretation

### Stronger heldout behavior

Would suggest cleaner labels/splits help policy learning.

### Lower apparent dev/heldout performance

Would not necessarily be worse.

It may mean the stricter dataset removed leakage or easy source correlations that inflated EXP-105.

### Class collapse

If predictions concentrate on K1 or K2, class imbalance is likely dominating optimization.

## Limitations

v1 still has:

```text
K3 positives=0
REFORMULATE independent families=1
```

so EXP-109 still cannot establish full five-action competence.
