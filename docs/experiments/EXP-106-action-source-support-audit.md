# EXP-106: Action-Class Source-Support Audit

## Research question

Does the current Phase 11 dataset contain enough independent source tasks per action class to distinguish policy learning from source-task memorization?

## Trigger from EXP-105

SFT produced:

```text
train accuracy   0.0833 → 0.5833
dev accuracy     0.0000 → 1.0000
heldout accuracy 0.3333 → 0.3333
```

This is mixed generalization.

Before changing optimization hyperparameters, we need to determine whether the evaluation design itself has enough class/source diversity.

## Core concept: source/action confounding

Suppose every `REFORMULATE` example comes from one underlying source task.

Then a model might learn:

```text
Helios-like wording → REFORMULATE
```

without learning the general concept:

```text
retrieval saturation → REFORMULATE
```

Paraphrases do not solve this because they still represent one underlying task.

## Audit

For every action class report:

- number of independent source tasks,
- source IDs,
- source IDs by split,
- whether the class has both training and source-disjoint evaluation support.

## Success criterion for class-level generalization

A class is source-disjoint evaluable only if:

1. at least one source task with that class is in train,
2. at least one different source task with that class is in dev or heldout.

## Expected use

EXP-106 is diagnostic.

If several classes fail this criterion, expand the oracle-labeled benchmark before further SFT tuning.
