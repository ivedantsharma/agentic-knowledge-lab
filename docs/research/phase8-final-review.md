# Phase 8 Final Review

## Status

Complete.

Phase 8 is closed as an agent-evaluation and grader-validation phase.

## Central question

> Can we evaluate what an agent actually did, not only whether its final answer was correct?

For the controlled benchmark:

> Yes. The Phase 8 evaluation stack separates planning, evidence sufficiency, trajectory quality, groundedness, relation alignment, efficiency, stopping, and final answer correctness.

## What was built

### Agent trace schema

`AgentRunTrace` with structured SEARCH and STOP steps.

### Agent evaluation task schema

Defines:

- expected answer,
- required documents,
- reasonable search budget.

### Deterministic trace grader

Measures:

- evidence coverage,
- repeated search,
- premature stop,
- efficiency.

### Grounding grader

Checks whether stopped answers appear in consumed evidence.

### Relation-alignment grader

Checks whether answers match the relation-specific value extracted from the annotated final hop.

### Evidence-path grader

Measures:

- coverage,
- order,
- exact path,
- extra documents.

### Integrated scorecard

Reports a vector of process and outcome metrics.

### Model-grader evaluation

The existing Qwen relation verifier was evaluated against deterministic gold cases and robustness variants.

## Experiment progression

### EXP-075

Controlled traces validated the initial grader contract.

Key result:

```text
correct answer
can coexist with
premature stop
```

and:

```text
correct answer
can coexist with
inefficient search
```

### EXP-076

Live rule and semantic planners had equal answer accuracy:

```text
0.8000
```

but different evidence behavior.

### EXP-077

Semantic OOD result:

```text
EvidenceCoverage=1.0000
AnswerGrounded=True
AnswerCorrect=False
```

### EXP-078

Relation-alignment grading showed:

```text
Grounded=True
RelationAligned=False
```

for the semantic OOD answer.

### EXP-079

Semantic planner followed the exact gold evidence path on all tasks:

```text
ExactPathMatchRate=1.0000
```

yet still answered the OOD task incorrectly.

### EXP-080

Model relation grader:

```text
Accuracy=0.8750
FalsePositive=0
FalseNegative=1
```

### EXP-081

Meaning-preserving Borealis variants produced unstable model-grader judgments.

### EXP-082

Integrated scorecard showed equal answer accuracy with different causal failure modes.

## Main research lessons

### 1. Correct answers do not prove good trajectories

A correct answer can come from incomplete evidence or inefficient search.

### 2. Retrieval success is not answer success

Full evidence can still lead to the wrong answer.

### 3. Groundedness is not relation correctness

An answer can be present in evidence but answer the wrong semantic role.

### 4. Perfect evidence paths are insufficient

Correct traversal does not guarantee correct fact selection.

### 5. Planner failure and answer-selection failure are different

They should not be collapsed into one error category.

### 6. Model graders are fallible components

They require their own evaluation.

### 7. Grader robustness matters

Meaning-preserving input changes can flip judgments.

### 8. Deterministic-first grading is preferable

When benchmark structure supports exact evaluation, deterministic graders are clearer and more reliable.

## Why Phase 8 stops here

The phase now includes:

- reusable trace schema,
- live trace recording,
- deterministic process graders,
- grounding,
- relation alignment,
- path evaluation,
- efficiency metrics,
- model-grader evaluation,
- model-grader robustness analysis,
- integrated scorecard,
- failure taxonomy,
- architecture decision.

Further work would move from evaluation infrastructure into adversarial robustness.

## What Phase 8 deliberately does not solve

- prompt-injection resistance,
- malicious documents,
- long-context distraction,
- repeated adversarial search loops,
- production-scale model-grader calibration,
- human-vs-model judge agreement,
- cost-aware agent evaluation.

These belong to later phases.

## Next phase

Phase 9:

# Adversarial Robustness & Failure Analysis

The focus shifts from:

```text
Can we diagnose normal agent failures?
```

to:

```text
How does the system behave when retrieval content actively tries to mislead it?
```
