# Phase 11 High-Level Design

## Goal

Teach a language model to choose retrieval/search actions from supervised demonstrations rather than rely only on hand-written rules.

## Architecture

```text
query / retrieval state
        ↓
policy model
        ↓
typed retrieval action
        ↓
retrieval system
```

Initial action vocabulary:

```text
SEARCH_HYBRID_K1
SEARCH_HYBRID_K2
SEARCH_HYBRID_K3
SEARCH_HYBRID_K5
REFORMULATE
```

## Training path

```text
oracle behavior
→ measured policy examples
→ source/evidence-family split
→ chat formatting
→ target-only labels
→ LoRA adapters
→ supervised fine-tuning
→ train/dev/heldout evaluation
```

## Key design choices

### Target-only loss

The model sees the full prompt, but prompt labels are masked with:

```text
-100
```

Only assistant action tokens contribute to causal-LM loss.

### Parameter-efficient fine-tuning

The base Qwen model is frozen.

LoRA adapters are trained on:

```text
q_proj
v_proj
```

with:

```text
r=4
alpha=8
```

### Measured labels

Every policy query should be independently oracle-labeled.

EXP-107 showed that paraphrases can change the optimal retrieval budget.

Therefore:

```text
same source task
does not imply
same policy action
```

### Evidence-family split

Queries sharing underlying evidence remain in the same split.

This prevents evaluation leakage through differently worded tasks that depend on the same evidence relation.

### Class-balanced sampling

On the tiny dataset, unbalanced SFT collapsed to the majority K1 action.

Balanced oversampling removed that collapse and improved heldout transfer.

## Results

Frozen policy baseline:

```text
EXP-101 accuracy=0.0000
format compliance=1.0000
```

One-example LoRA optimization:

```text
loss 0.204247 → 0.006459
trainable parameters ≈0.0547%
```

Unbalanced measured-v1 SFT:

```text
train=0.6364
dev=0.6667
heldout=0.0000

all predictions collapsed to K1
```

Balanced measured-v1 SFT:

```text
train=0.9091
dev=1.0000
heldout=0.6667
```

## Limitations

- dataset remains very small,
- benchmark is synthetic,
- K3 has no positive example,
- REFORMULATE has one independent evidence family,
- dev/heldout each contain one evidence family,
- no multiple-seed variance study yet.

Phase 11 demonstrates the supervised learning mechanism and major data-design constraints, not a production-ready retrieval policy.
