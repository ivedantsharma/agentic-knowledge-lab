# ADR-009 — Capability-Routed Planner Components

## Status

Accepted.

## Context

Phase 4 tested several planner formulations.

Observed capabilities:

### Rule-based planner

Strong on exact known task forms.

Weak on paraphrases and unseen relations.

### Semantic planner

Robust to paraphrasing within known intent classes.

Weak on unseen relations because the intent vocabulary is fixed.

### FLAN-T5 small/base

Useful for some extraction and classification tasks.

Weak for open-ended next-query generation.

### Qwen2.5-0.5B-Instruct

Demonstrated useful continuation-query generation.

Weak on relation-sensitive answer verification.

### Qwen2.5-1.5B-Instruct

Correctly distinguished grounded-but-wrong candidates from grounded-and-correct candidates in the verifier ablation.

## Decision

Do not use one model for every planner operation.

Route planner responsibilities by demonstrated capability:

```text
Semantic planner
→ bootstrap

Qwen 0.5B
→ continuation query generation
→ candidate extraction / abstention

Qwen 1.5B
→ relation verification

deterministic code
→ grounding invariant
```

## Consequences

### Positive

- larger model cost is paid only for the harder verifier task,
- components are selected based on evidence rather than assumption,
- deterministic guarantees remain around model outputs,
- individual capabilities can be ablated independently.

### Negative

- more model components,
- more memory usage,
- more complex orchestration,
- cross-component errors remain possible.

## Rationale

The Phase 4 results show that model capability is task-specific.

A single-model design would either:

- use a weak model for tasks it cannot reliably solve, or
- use a larger model everywhere without experimental justification.

Capability routing better matches the observed evidence.
