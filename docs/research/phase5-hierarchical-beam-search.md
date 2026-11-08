# Phase 5 — Hierarchical Beam Search

## Why beams exist at multiple levels

A hierarchy can make irreversible mistakes whenever it collapses to top-1.

Example:

```text
documents
→ keep top 2 parents
→ sections
→ keep top 2 children
→ downstream answer stage
```

Each beam preserves multiple plausible paths.

## EXP-043 lesson

At parent beam 2:

```text
ChildRecall@1 = 0.6667
ChildRecall@2 = 1.0000
```

So the answer-bearing Cirrus section is lost only when we force a top-1 child decision.

## Cost tradeoff

Keeping more children increases downstream context or reranking cost.

Therefore beam width is a resource-allocation parameter, not only an accuracy parameter.

## General principle

Use narrow beams where confidence is high and wider beams where ambiguity remains.

Phase 5 is not implementing adaptive beams yet, but fixed beam experiments establish the recall/cost curve first.