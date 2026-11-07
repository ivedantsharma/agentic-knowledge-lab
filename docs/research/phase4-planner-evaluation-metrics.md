# Phase 4 — Planner Evaluation Metrics

## Why final answer accuracy is not enough

Two planners can have the same answer accuracy and fail in very different ways.

Planner A may:

```text
retrieve the right evidence
→ choose the wrong answer
```

Planner B may:

```text
stop before retrieving the right evidence
```

Both produce an incorrect final answer, but the engineering fixes are different.

## Metrics

### Answer Accuracy

```text
correct final answers / tasks
```

This is the end-to-end outcome metric.

### Planner Failure Rate

```text
planner exceptions / tasks
```

This measures whether the planner can produce valid actions.

### Stopped Rate

```text
tasks that emitted STOP / tasks
```

A low stopped rate can reveal loops or failure to recognize sufficient evidence.

### Stop Precision

```text
correct STOPs / all STOPs
```

This asks:

> When the planner decides to stop, how often is that decision correct?

### Premature Stop Rate

A STOP is premature when the task's final evidence document was never retrieved before termination.

```text
premature STOP tasks / all tasks
```

This directly measures the failure mode discovered during the hybrid planner work.

### Search Success Rate

```text
tasks where final evidence was retrieved / tasks
```

This separates retrieval/planning trajectory success from final answer generation.

### Average Search Steps

```text
total SEARCH actions / tasks
```

Lower is not automatically better.

A planner that searches zero times and hallucinates answers is efficient but wrong.

Efficiency matters only alongside correctness.

### Max-Step Exhaustion Rate

```text
tasks that hit the search budget without STOP / tasks
```

This captures looping or inability to recognize completion.

## Answer matching

The benchmark allows the expected answer to be contained inside a longer grounded answer.

Example:

```text
expected:
CIRRUS-DLQ

predicted:
CIRRUS-DLQ dead-letter queue
```

This counts as correct.

The matcher is intentionally simple and deterministic for Phase 4.
