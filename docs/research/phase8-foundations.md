# Phase 8 Foundations: Agent Evaluation and Graders

## Evaluation target shift

Phase 7 evaluated:

```text
candidate-set composition
```

Phase 8 evaluates:

```text
agent behavior over time
```

A final answer alone cannot reveal whether an agent:

- searched unnecessary documents,
- repeated queries,
- stopped before evidence was sufficient,
- retrieved the correct evidence by accident,
- ignored contradictory evidence,
- used tools inefficiently.

## Three-layer evaluation model

```text
Benchmark Task
    ↓
Agent Run Trace
    ↓
Graders
```

### Benchmark Task

Defines what should be accomplished.

### Agent Run Trace

Records what actually happened.

### Grader

Maps the trace and task into interpretable metrics.

This separation prevents the runtime from silently containing benchmark ground truth.

## Planned Phase 8 progression

1. deterministic trace schema and graders,
2. wire trace recording into a live planner runner,
3. retrieval-path and evidence-sufficiency metrics,
4. tool-use efficiency metrics,
5. stopping-policy graders,
6. deterministic groundedness checks,
7. grader disagreement / failure analysis,
8. only then introduce model-based grading where deterministic rules are insufficient.

## Principle

Use the simplest grader that can validly measure the property.

Do not use an LLM judge for something deterministic code can measure exactly.
