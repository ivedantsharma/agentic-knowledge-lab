# ADR-008 — Separate Planner, Executor, State, and Tools

## Status

Accepted.

## Context

Agentic retrieval combines several failure-prone operations:

- deciding what to do,
- formulating queries,
- retrieving documents,
- parsing observations,
- updating state,
- deciding when to stop.

If these responsibilities are combined into one opaque component, failures are difficult to diagnose.

Phase 4 experiments repeatedly required distinguishing:

- planning failure,
- retrieval failure,
- extraction failure,
- stopping failure,
- protocol failure.

## Decision

Keep planner policy separate from:

- search execution,
- observation parsing,
- state storage,
- evaluation.

Use typed planner actions:

```text
SEARCH(query)
STOP(answer)
```

as the boundary between planner and executor.

## Consequences

### Positive

- failures can be isolated,
- planners can be compared under the same executor,
- deterministic and model-based planners can share infrastructure,
- traces become reproducible,
- evaluation becomes component-aware.

### Negative

- more interfaces and modules,
- more explicit orchestration code,
- state synchronization must be handled carefully.

## Rationale

The additional structure is justified because Phase 4 is a research system, not only an application demo.

We need to know why a trajectory succeeds or fails.
