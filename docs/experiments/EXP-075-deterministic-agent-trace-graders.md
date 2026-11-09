# EXP-075: Deterministic Agent Trace Grader Foundations

## Phase 8 central question

> Can we evaluate what an agent did, not only whether its final answer was correct?

## Motivation

Phase 4 already measured planner outcomes such as:

- answer accuracy,
- stopping,
- search success,
- average search steps.

However, the main comparison runner printed actions instead of consistently producing a reusable trace artifact.

Phase 8 therefore begins by separating:

```text
task ground truth
from
agent run trace
from
grader
```

## Why deterministic graders first?

Before introducing model-based judges, we need metrics with exact expected behavior.

A model grader would make it difficult to know whether an error came from:

- the agent,
- the benchmark,
- or the grader.

## Trace contract

An agent run contains ordered steps:

```text
SEARCH(query, retrieved_document_ids)
...
STOP(answer)
```

Structural rules include:

- contiguous step indices,
- SEARCH requires a query,
- STOP requires an answer,
- at most one STOP,
- STOP must be final.

## Initial deterministic metrics

### Required Evidence Coverage

```text
retrieved required documents
/
required documents
```

### Premature Stop

True when the agent stops before all required evidence has been retrieved.

This deliberately distinguishes:

```text
correct answer
```

from:

```text
correctly justified stopping
```

### Repeated Searches

Counts exact normalized duplicate queries.

This is a simple first proxy for search loops.

### Efficient Search

True when:

- search count does not exceed the task's reasonable budget,
- no query is repeated.

### Answer Correctness

Exact normalized answer comparison for this controlled experiment.

## Controlled trace cases

EXP-075 uses four synthetic traces over the same task:

1. ideal,
2. premature stop,
3. redundant search,
4. wrong evidence.

No live model or retriever is changed.

The experiment tests the grader contract only.

## What success would prove

If the graders distinguish these traces correctly, we have a stable foundation for evaluating live Phase 4 planners in later Phase 8 experiments.

It would not yet prove robust semantic groundedness or general agent quality.
