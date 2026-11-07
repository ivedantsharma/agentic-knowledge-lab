# Phase 4 — Capability-Based Hybrid Planner

## Why hybrid?

Our experiments established different strengths.

### Semantic planner

Strength:

```text
original question
→ identify anchor / first hop
```

Weakness:

```text
closed-world intent vocabulary
```

### Qwen2.5-0.5B-Instruct

Weakness:

```text
bootstrap query from no evidence
```

Strengths after intermediate evidence:

```text
generate missing-information query
judge answerability
extract grounded answer
```

A hybrid planner assigns each component the capability it demonstrated.

## Pipeline

```text
Step 0
original question
↓
SemanticPlanner
↓
SEARCH

Step 1+
retrieved evidence
↓
Qwen answerability check
├── YES → grounded extraction → STOP
└── NO  → generate next query → SEARCH
```

## Why this is not cheating

The semantic bootstrap planner does not read the gold hop labels.

It derives the initial search from the question and corpus-discovered entities.

Qwen then controls the open-ended continuation.

The benchmark answer is never supplied to either planner.

## Why modularity matters

A monolithic agent asks one model to be good at every operation.

A modular agent can instead use:

- deterministic code where rules are reliable,
- embedding models for semantic routing,
- generative models for open-ended language decisions.

The architecture follows measured capability rather than aesthetic preference.

## Current experiment

We now run the unseen dead-letter task through the full hybrid SEARCH/STOP loop.

This is the first experiment where Qwen-generated queries directly affect retrieval.
