# Phase 11 Foundations: Fine-Tuning Retrieval/Search Behavior

## Central shift

Phase 10 asked:

> What retrieval action would be useful?

Phase 11 asks:

> Can a model learn to choose those actions from demonstrations?

This is an imitation-learning problem before it becomes an RL problem.

## Supervised fine-tuning intuition

A language model already has pretrained parameters.

Supervised fine-tuning changes those parameters so that, for inputs from our task distribution, desired outputs become more likely.

For retrieval policy learning:

```text
input:
query / retrieval state

target:
retrieval action
```

Example:

```text
Query:
How many retries does Cirrus use before dead-letter handling?

Target:
SEARCH_HYBRID_K1
```

## Why start with a discrete action vocabulary?

Free-form search plans are difficult to grade.

A small typed vocabulary gives us exact metrics and cleaner supervision.

Initial Phase 11 actions:

```text
SEARCH_HYBRID_K1
SEARCH_HYBRID_K2
SEARCH_HYBRID_K3
SEARCH_HYBRID_K5
REFORMULATE
```

This vocabulary comes directly from the Phase 10 control axes.

## Why no fine-tuning in EXP-101?

Before changing model weights we need:

1. valid training examples,
2. deterministic labels,
3. a stable output protocol,
4. a frozen-model baseline.

Without a pre-training baseline, a later improvement cannot be attributed to fine-tuning.

## Seed labels

Phase 10 gives six seed policy demonstrations.

Budget labels come from the adaptive top-k oracle.

REFORMULATE comes from the observed saturation case where increasing k failed but query decomposition recovered additional evidence.

## Important limitation

Six examples are not a fine-tuning dataset.

They are a seed set used to validate:

- schema,
- label semantics,
- baseline protocol.

The dataset must be expanded and split before SFT.
