# Phase 4 — Planner Capability Decomposition

## Why this experiment exists

The few-shot generative planner produced:

```text
STOP: No, no, no, no, ...
```

This tells us:

- the output protocol improved,
- the action decision was wrong,
- the answer was ungrounded,
- generation entered a repetition loop.

But one planner prompt currently asks a small model to perform several tasks simultaneously.

## Decompose the planner

A generative search planner contains at least three distinct capabilities.

### 1. Query generation

Given:

```text
question + current evidence
```

produce:

```text
next useful search query
```

### 2. Answerability / stopping

Given:

```text
question + evidence
```

decide:

```text
is there enough evidence to stop?
```

### 3. Grounded answer extraction

Given:

```text
question + sufficient evidence
```

produce only the requested answer.

These are separate ML capabilities.

A model may be good at one and poor at another.

## Why this matters architecturally

If one monolithic prompt fails, we do not know which capability caused the failure.

A capability probe lets us ask:

```text
Can FLAN-T5-small generate a useful query?
Can it judge answerability?
Can it extract CIRRUS-DLQ from explicit evidence?
```

If query generation works but stopping fails, we should not discard the model entirely.

We could use it only as a query generator and keep stopping deterministic or use another component.

If all three fail, the model is simply too weak for this role.

## The five probes

The diagnostic script tests:

1. initial query generation with no evidence,
2. next-query generation after intermediate evidence,
3. final answer extraction from sufficient evidence,
4. answerability with no evidence,
5. answerability with sufficient evidence.

## Research principle

Before increasing model size or rewriting the architecture:

> isolate the failing capability.

This avoids treating "the agent failed" as one undifferentiated problem.
