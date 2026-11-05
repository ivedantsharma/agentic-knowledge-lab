# EXP-022: Phase 4 Oracle Planner Baseline

## Goal

Validate the Phase 4 planner-action-tool-state loop before removing access to the benchmark plan.

## Benchmark

- 4 tasks
- two-hop and three-hop chains
- same corpus used by the final Phase 3 benchmark

## Result

```text
AnswerAccuracy = 1.0000
```

All four tasks produced the expected final answer.

## Trace behavior

Each task now executes through:

```text
planner
→ SEARCH action
→ dense search tool
→ observation / extraction
→ PlannerState update
→ planner
→ ...
→ STOP action
```

The trace includes each search and the final stop action.

## Interpretation

The new agent loop did not introduce a regression.

This gives us a stable architectural baseline before replacing the oracle planner.

## Limitation

The oracle planner still reads the benchmark's gold hop sequence.

Therefore this experiment validates execution architecture, not autonomous planning.

## Next experiment

Replace the oracle planner with a deterministic rule-based planner that sees only:

- original question,
- current retrieval state,
- retrieved evidence.

The planner must decide whether to SEARCH or STOP without reading `task.hops`.
