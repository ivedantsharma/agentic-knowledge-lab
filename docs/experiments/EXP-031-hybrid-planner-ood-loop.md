# EXP-031: Hybrid Planner Full OOD Loop

## Research question

Can a capability-based hybrid planner solve the unseen dead-letter relation end-to-end?

## Components

```text
bootstrap:
SemanticPlanner

continuation query generation:
Qwen2.5-0.5B-Instruct

answerability:
Qwen2.5-0.5B-Instruct

answer extraction:
Qwen2.5-0.5B-Instruct

retrieval:
MiniLM dense search
```

## Expected trajectory

```text
Question
↓
bootstrap SEARCH for Developer Productivity worker platform
↓
retrieve org_dev_productivity
↓
Qwen says evidence is insufficient
↓
Qwen generates dead-letter destination query
↓
retrieve manual_cirrus
↓
Qwen says evidence is sufficient
↓
Qwen extracts CIRRUS-DLQ
↓
STOP
```

## What this experiment tests

Unlike the capability probes, generated text now changes the actual retrieval trajectory.

A weak generated query may retrieve the wrong document.

Therefore success requires:

- correct bootstrap,
- useful continuation query,
- successful retrieval,
- correct stopping,
- grounded answer extraction.

## Limitation

This is still one OOD synthetic task.

Success validates the mechanism, not general planner robustness.
