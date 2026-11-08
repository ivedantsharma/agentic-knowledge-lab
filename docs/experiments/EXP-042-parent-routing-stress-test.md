# EXP-042: Parent Routing Stress Test

## Research question

What happens when the correct parent document is not obviously the top document?

## Motivation

EXP-041 assumes top-1 parent routing is correct.

That is a dangerous assumption in larger corpora.

## New concept: parent beam width

Instead of:

```text
top-1 document
→ rerank its sections
```

we can use:

```text
top-N documents
→ pool their sections
→ rerank pooled children
```

This creates a recall/cost tradeoff.

## Experiment design

Create semantically similar parent distractors around the existing manuals.

Compare:

```text
Parent beam = 1
Parent beam = 2
Parent beam = 3
```

while keeping the cross-encoder as the child scorer.

## Metrics

- ParentRecall@K
- EndToEndHit@1
- number of child candidates reranked
- per-task parent rank

## Hypothesis

Top-1 parent routing may fail under stronger distractors.

Increasing parent beam width should recover some failures at additional reranking cost.

## Research value

This tests the central hierarchical tradeoff:

```text
narrow routing
vs
parent recall
vs
reranking cost
```