# EXP-037: Multi-Task Planner Comparison

## Goal

Compare three planner policies under one shared Phase 4 evaluation harness.

## Task set

Five tasks:

- four known-intent Phase 3 tasks,
- one unseen dead-letter relation task.

Chain lengths include both two-hop and three-hop questions.

## Shared environment

All planners use the same:

- Phase 4 OOD corpus,
- MiniLM dense retriever,
- top-3 retrieval,
- top-1 execution,
- maximum six search steps,
- task ground truth,
- answer matching,
- aggregate metrics.

Only the planner policy changes.

## Planners

### Rule-based

Deterministic surface-pattern planner.

Expected strength:

- exact original benchmark wording.

Expected weakness:

- unseen surface forms and unseen relations.

### Semantic

Embedding-based intent classifier with fixed goal prototypes and fixed query templates.

Expected strength:

- paraphrase robustness.

Expected weakness:

- closed-world relation vocabulary.

### Hybrid

```text
semantic bootstrap
+
Qwen 0.5B continuation
+
Qwen 1.5B relation verifier
+
deterministic grounding
```

Expected strength:

- continuation on unseen relations,
- conservative STOP decisions.

## Metrics

- Answer Accuracy
- Planner Failure Rate
- Stopped Rate
- Stop Precision
- Premature Stop Rate
- Search Success Rate
- Average Search Steps
- Max-Step Exhaustion Rate

## Important interpretation rule

The benchmark is still small and synthetic.

Do not claim that the hybrid planner is generally superior based on five tasks.

Use the comparison to identify mechanisms and failure modes.
