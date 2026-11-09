# EXP-076: Live Planner Trace Recording and Deterministic Grading

## Research question

Can the existing Phase 4 planners be evaluated through the new Phase 8 trace contract without changing their behavior?

## Controlled setup

Keep fixed:

- Phase 4 planner benchmark v0,
- Phase 4 OOD corpus v0,
- DenseSearchTool,
- MiniLM embeddings,
- RuleBasedPlanner,
- SemanticPlanner,
- max steps = 6.

Change only the evaluation plumbing:

```text
printed runtime behavior
→ structured AgentRunTrace
→ deterministic Phase 8 graders
```

## Why start with rule and semantic planners?

They avoid introducing Qwen/model-grader variability while we validate trace recording.

The hybrid planner is deferred until the trace contract is proven on deterministic/semantic planner execution.

## Important evidence-consumption rule

DenseSearchTool returns top-3, but the existing Phase 4 loop passes only top-1 into:

```text
parse_retrieval_observation(...)
```

Therefore EXP-076 records only the top-1 document as retrieved evidence in the agent trace.

This prevents the evaluator from crediting documents the planner did not actually consume.

## Task conversion

Each MultiHopTask becomes an AgentEvalTask:

```text
required_document_ids =
all gold hop document IDs

max_reasonable_search_steps =
number of gold hops
```

This is a controlled baseline, not a claim that every valid agent must follow exactly the gold number of searches.

## New aggregate metrics

- AnswerAccuracy
- FullEvidenceRate
- PrematureStopRate
- EfficientSearchRate
- AverageSearchSteps
- AverageRepeatedSearches

## What success would prove

The new trace framework can reproduce meaningful process-level distinctions on real planner executions.

It would not yet prove semantic groundedness, tool-selection quality, or general agent correctness.
