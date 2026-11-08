# EXP-044: Parent Beam 2 + Child Beam 2

## Research question

Can a small two-level beam preserve all answer-bearing evidence under hard parent and child distractors?

## Retrieval policy

```text
query
→ dense parent ranking
→ keep top 2 parents
→ pool their 8 sections
→ cross-encoder ranking
→ keep top 2 children
```

## Metrics

- ParentRecall@2
- ChildRecall@1
- ChildRecall@2
- retained child count
- evidence retention rate

## Hypothesis

Parent beam 2 + child beam 2 should preserve all relevant evidence on the current stress benchmark.

## Why this matters

This creates a retrieval interface suitable for later answer generation or section→chunk descent without forcing premature top-1 decisions.