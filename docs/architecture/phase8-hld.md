# Phase 8 High-Level Design

## Goal

Evaluate agent behavior as a sequence of decisions rather than only a final answer.

The central question is:

> Can we decompose agent quality into interpretable dimensions such as evidence sufficiency, trajectory quality, groundedness, relation alignment, efficiency, stopping, and final correctness?

## Evaluation architecture

```text
Benchmark Task
    ↓
Live Agent Execution
    ↓
AgentRunTrace
    ├── SEARCH(query, consumed docs)
    └── STOP(answer)
            ↓
Deterministic Graders
    ├── trace behavior
    ├── evidence sufficiency
    ├── path order
    ├── groundedness
    └── relation alignment
            ↓
Integrated Scorecard
            ↓
Optional Model Grader
(evaluated against deterministic gold)
```

## Core principle

Do not collapse agent evaluation into one scalar.

Two systems can have the same answer accuracy while failing for entirely different reasons.

## Trace schema

`AgentRunTrace` stores:

- task ID,
- ordered steps,
- SEARCH queries,
- consumed document IDs,
- STOP answers,
- metadata.

Structural validation enforces:

- contiguous step indices,
- SEARCH requires query,
- STOP requires answer,
- at most one STOP,
- STOP must be final.

## Deterministic graders

### Agent trace grader

Measures:

- search steps,
- repeated searches,
- required evidence coverage,
- premature stop,
- efficient search,
- full evidence retrieval.

### Grounding grader

Checks whether the stopped answer appears in evidence actually consumed by the agent.

This evaluates:

```text
answer supported by evidence?
```

not:

```text
answer correct for the requested relation?
```

### Relation-alignment grader

Uses the final-hop extraction pattern to recover the relation-specific answer from the gold final evidence.

Measures whether the stopped answer fills the requested semantic role.

### Evidence-path grader

Compares consumed evidence sequence to the ordered gold hop path.

Metrics:

- path coverage,
- ordered path complete,
- exact path match,
- extra documents.

## Model grader

The existing `QwenRelationVerifier` is evaluated as a grader rather than trusted automatically.

Model:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

It receives:

- question,
- evidence,
- candidate answer,

and predicts YES/NO for relation alignment.

## Key experiment results

### EXP-075

Controlled synthetic traces separated:

- correct answer,
- premature stop,
- redundant search,
- wrong evidence.

### EXP-076

Rule-based and semantic planners both achieved:

```text
AnswerAccuracy=0.8000
```

but:

```text
Rule FullEvidence=0.8000
Semantic FullEvidence=1.0000
```

### EXP-077

Semantic OOD case:

```text
EvidenceCoverage=1.0000
AnswerGrounded=True
AnswerCorrect=False
```

Therefore:

```text
grounded != correct
```

### EXP-078

Semantic OOD case:

```text
FinalEvidenceConsumed=True
RelationAligned=False
```

Therefore:

```text
grounded != relation aligned
```

### EXP-079

Semantic planner:

```text
ExactPathMatchRate=1.0000
```

but OOD answer still wrong.

Therefore:

```text
perfect evidence path != correct answer
```

### EXP-080

Model relation grader:

```text
Accuracy=0.8750
FalsePositives=0
FalseNegatives=1
```

### EXP-081

Meaning-preserving Borealis variants caused prediction flips.

Therefore the model grader is input-form sensitive.

### EXP-082 integrated scorecard

Rule-based:

```text
answer_correct_rate=0.8000
full_evidence_rate=0.8000
ordered_path_rate=0.8000
exact_path_rate=0.8000
grounded_rate=0.8000
relation_aligned_rate=0.8000
efficient_rate=1.0000
premature_stop_rate=0.0000
planner_failure_rate=0.2000
```

Semantic:

```text
answer_correct_rate=0.8000
full_evidence_rate=1.0000
ordered_path_rate=1.0000
exact_path_rate=1.0000
grounded_rate=1.0000
relation_aligned_rate=0.8000
efficient_rate=1.0000
premature_stop_rate=0.0000
planner_failure_rate=0.0000
```

## Main architectural lesson

Agent evaluation is a pipeline:

```text
planning
→ retrieval
→ evidence path
→ grounding
→ relation selection
→ answer
```

A failure at any layer should remain diagnosable.

## Limitations

- small synthetic benchmark,
- deterministic exact-span groundedness,
- extraction-pattern relation grader depends on benchmark annotations,
- efficiency uses simple search budgets,
- no latency/cost model,
- no tool-selection diversity,
- model grader tested on a tiny controlled set,
- no human grader comparison.

Phase 8 validates evaluation structure and failure decomposition, not broad grader generalization.
