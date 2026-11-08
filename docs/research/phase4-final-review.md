# Phase 4 Final Review

## Status

Phase 4 complete.

## Central question

Phase 3 asked:

> Can the system execute a known retrieval chain?

Phase 4 asked:

> Can the system decide and execute the retrieval chain itself?

The answer is:

> Yes for a controlled synthetic setting, but planner reliability depends strongly on task type and component capability.

## What was built

### Agent infrastructure

- PlannerAction schema
- PlannerState
- PlannerTraceStep
- DenseSearchTool
- observation parser
- reusable query renderer

### Planner baselines

- oracle planner
- rule-based planner
- semantic planner
- generative FLAN planner
- Qwen continuation planner
- capability-routed hybrid planner

### Verification and stopping

- answerability probes
- extract-or-abstain
- exact-span grounding
- relation-alignment verifier
- model-capacity ablation for verification

### Evaluation

- multi-task planner benchmark
- answer accuracy
- planner failure rate
- stopped rate
- stop precision
- premature-stop rate
- search success rate
- average search steps
- max-step exhaustion rate

## Final five-task benchmark

```text
Rule-based
AnswerAccuracy       = 0.8000
PlannerFailureRate   = 0.2000
SearchSuccessRate    = 0.8000
StopPrecision        = 1.0000

Semantic
AnswerAccuracy       = 0.8000
PlannerFailureRate   = 0.0000
SearchSuccessRate    = 1.0000
StopPrecision        = 0.8000

Hybrid
AnswerAccuracy       = 0.6000
PlannerFailureRate   = 0.0000
SearchSuccessRate    = 0.8000
StopPrecision        = 1.0000
PrematureStopRate    = 0.0000
```

## Interpretation

The hybrid planner should not replace the deterministic or semantic planners yet.

Its main contribution is expanded capability:

```text
unseen relation
→ semantic planner fails
→ hybrid succeeds
```

Its main weakness is trajectory stability on some familiar tasks.

## Remaining hybrid failure modes

### Backup task

Continuation planner ignores the intermediate team entity and becomes trapped on an Atlas snapshot distractor.

Category:

```text
continuation-query failure
```

### Retry-count task

The correct final evidence is retrieved.

The model proposes:

```text
5
```

while the evidence contains:

```text
five times
```

Exact-span grounding rejects the representation.

Category:

```text
extraction / grounding representation failure
```

## Research lessons

### Lesson 1

Agentic search needs evaluation of the trajectory, not only the final answer.

### Lesson 2

A retriever can succeed while the planner still fails.

### Lesson 3

Grounding, relevance, and relation alignment are separate properties.

### Lesson 4

False-positive STOP decisions are especially expensive.

### Lesson 5

Structured state remains useful even when a generative model sees raw evidence.

### Lesson 6

Model capability should be measured per subtask.

### Lesson 7

Do not optimize repeatedly against a tiny benchmark after the mechanism is understood.

## Why Phase 4 stops here

Further tuning on the same five tasks would risk benchmark overfitting.

The remaining failures are documented and can become future training/evaluation examples.

The research goal of Phase 4 was not to achieve perfect benchmark accuracy.

It was to:

- construct agentic planning infrastructure,
- expose planner failure modes,
- test closed vs open planning,
- build stopping/verification mechanisms,
- create planner-level evaluation.

Those objectives are complete.

## Phase 5

Next:

# Hierarchical Retrieval

We will study:

- document → section → chunk retrieval,
- coarse-to-fine search,
- parent-child navigation,
- hierarchical indexes.

The new research question is:

> Can hierarchical retrieval improve evidence discovery while controlling context size and search cost?
