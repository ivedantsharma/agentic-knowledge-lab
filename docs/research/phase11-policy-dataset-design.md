# Phase 11 Retrieval Policy Dataset Design

## Goal

Construct a supervised dataset for learning retrieval actions from queries.

Each example is:

```text
input:
query

target:
retrieval policy action
```

## Action vocabulary

```text
SEARCH_HYBRID_K1
SEARCH_HYBRID_K2
SEARCH_HYBRID_K3
SEARCH_HYBRID_K5
REFORMULATE
```

## Labeling rules

### SEARCH_HYBRID_K1 / K2 / K3 / K5

Use the smallest Hybrid retrieval budget that reaches the maximum observed supporting-document recall over:

```text
k ∈ {1, 2, 3, 5}
```

### REFORMULATE

Use when:

1. retrieval recall saturates below full supporting recall through k=5, and
2. an oracle query transformation recovers additional supporting evidence.

This prevents REFORMULATE from becoming a subjective label.

## Data augmentation principle

We may create paraphrases of an already-labeled query only when the information need and evidence target remain unchanged.

Paraphrases inherit the original oracle action.

This is an assumption that must later be tested on heldout paraphrases.

## Split rule

Do not randomly split paraphrases of the same source task across train and heldout.

All variants of one source task stay in the same split.

Otherwise the heldout set would leak the underlying task.

## Initial split

Training source tasks:

```text
kbv2-hard-001
kbv2-hard-005
kbv2-hard-006
kbv2-hard-007
```

Development source task:

```text
kbv2-hard-002
```

Heldout source task:

```text
kbv2-hard-010
```

This split is intentionally source-task disjoint.

## Limitation

The dataset is still synthetic and very small.

Its role is to validate the SFT mechanism, not to claim general retrieval-policy learning.
