# EXP-102: Retrieval Policy Dataset Audit

## Research question

Can we construct a source-task-disjoint supervised dataset for retrieval-policy learning without leakage?

## Dataset

```text
18 examples
6 source tasks
```

Three paraphrases per source task.

## Split

```text
train:
  4 source tasks
  12 examples

dev:
  1 source task
  3 examples

heldout:
  1 source task
  3 examples
```

All paraphrases from one source task stay in the same split.

## Why this matters

A random example-level split would leak near-duplicate paraphrases between training and evaluation.

That could make fine-tuning appear to generalize when it is only memorizing one underlying information need.

## Audit metrics

- total examples,
- examples per split,
- action distribution,
- number of source tasks,
- source-task leakage across splits.

## Limitation

The dataset is deliberately tiny.

It is suitable for validating SFT mechanics and generalization protocol, not for making claims about broad policy learning.
