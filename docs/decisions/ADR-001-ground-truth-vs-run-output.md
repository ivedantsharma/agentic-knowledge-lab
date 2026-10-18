# ADR-001: Separate Ground Truth from System Outputs

## Status

Accepted

## Context

KnowledgeBench needs to compare expected benchmark truth with what a retriever or agent actually produced.

Mixing both into one object would make leakage and evaluation mistakes easier.

## Decision

Use separate schemas:

```text
KnowledgeTask
= ground truth

RunResult
= observed system output
```

Join them using task_id.

## Consequences

Benefits:
- clear evaluator boundary,
- reduced risk of answer-key leakage,
- easier experiment logging,
- cleaner future agent traces.

Cost:
- requires an explicit join/evaluation layer.
