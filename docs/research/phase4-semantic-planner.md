# Phase 4 — Semantic Planner Baseline

## Motivation

The rule-based planner scored:

```text
1.0000 AnswerAccuracy
```

on the original wording, but:

```text
0.0000 AnswerAccuracy
```

on paraphrases.

This shows the planner had learned no language invariance.

## New idea

Use embeddings to classify the user's question into a small planning goal.

Current goal prototypes:

- backup cadence,
- retry count,
- cache duration,
- signing-key rotation.

The same MiniLM model already used for retrieval provides semantic representations.

## Anchor entity

The planner also needs to know where to begin.

Instead of hard-coding task entities, it discovers candidate entity names from the corpus using organization-relation patterns such as:

```text
X is operated by ...
X maintains ...
```

It then matches those discovered entities against the question.

## Planner flow

```text
question
↓
semantic goal classification
↓
anchor entity detection
↓
initial SEARCH
↓
retrieved evidence
↓
structured state
↓
evidence-driven next SEARCH
↓
STOP
```

## Why this is still not an LLM agent

The planner chooses among a fixed set of semantic intents.

It does not generate arbitrary plans.

That makes it:

- more robust than exact regex matching,
- more interpretable than a generative model,
- useful as another baseline before model-generated planning.

## Research question

Can semantic intent matching recover planner performance under paraphrase without changing retrieval or the benchmark?
