# Phase 4 High-Level Design

## Goal

Move from executing a known retrieval chain to deciding the retrieval trajectory autonomously.

The Phase 4 system must decide:

- what to search,
- how to formulate the next query,
- whether current evidence is sufficient,
- when to stop,
- how to avoid premature stopping.

## Final architecture

```text
User Question
    ↓
PlannerState
    ↓
Step 0: Semantic Bootstrap Planner
    ↓
SEARCH action
    ↓
DenseSearchTool
    ↓
Retrieved Document
    ↓
Observation Parser
    ↓
RetrievalState
(entity, qualifiers, evidence, source)
    ↓
Step 1+: Qwen Continuation Planner
    ├── candidate extraction / abstention
    ├── continuation query generation
    └── structured-state conditioning
    ↓
Grounding Check
    ↓
Qwen Relation Verifier
    ↓
SEARCH or STOP
```

## Core components

### PlannerAction

Typed action interface:

```text
SEARCH(query)
STOP(answer)
```

This gives a deterministic software boundary around probabilistic model output.

### PlannerState

Stores:

- original question,
- current step index,
- RetrievalState,
- trace,
- final answer,
- stopped flag.

### RetrievalState

Carries forward:

- current entity,
- qualifiers,
- source document ID,
- raw evidence text.

Structured state remains necessary even after introducing a generative model.

### DenseSearchTool

Uses MiniLM dense retrieval and returns ranked documents.

Retrieval remains separate from planner policy so planning and retrieval failures can be diagnosed independently.

### SemanticPlanner

Used for bootstrap planning.

It is robust to paraphrasing within its known intent space, but closed-world because it relies on fixed goal prototypes and query templates.

### QwenContinuationPlanner

Uses:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

for:

- continuation query generation,
- extract-or-abstain candidate generation.

The query prompt includes:

- original question,
- current entity,
- qualifiers,
- latest evidence.

### QwenRelationVerifier

Uses:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

to verify that a grounded candidate answers the exact relation requested by the question.

### Deterministic grounding

A candidate answer must occur in the retrieved evidence before STOP is allowed.

This prevents unsupported hallucinated answers.

## STOP policy

The final STOP condition is:

```text
candidate exists
AND candidate is grounded
AND relation verifier accepts candidate
→ STOP
```

Otherwise:

```text
→ SEARCH
```

## Evaluation

Phase 4 planner metrics:

- Answer Accuracy
- Planner Failure Rate
- Stopped Rate
- Stop Precision
- Premature Stop Rate
- Search Success Rate
- Average Search Steps
- Max-Step Exhaustion Rate

## Final benchmark result

Five-task benchmark:

| Planner | Answer Accuracy | Planner Failure | Search Success | Stop Precision |
|---|---:|---:|---:|---:|
| Rule-based | 0.80 | 0.20 | 0.80 | 1.00 |
| Semantic | 0.80 | 0.00 | 1.00 | 0.80 |
| Hybrid | 0.60 | 0.00 | 0.80 | 1.00 |

## Interpretation

The hybrid planner is not generally superior on this benchmark.

Its value is capability extension:

- it solves the unseen dead-letter relation,
- it avoids premature stopping after relation verification,
- it is less reliable than deterministic/semantic planners on some known tasks.

Phase 4 therefore supports capability routing and explicit state, not a claim that generative planning should replace deterministic planning everywhere.
