# ADR-012: Layered Agent Evaluation with Deterministic-First Graders

## Status

Accepted.

## Context

Agent systems can fail at multiple stages:

- planning,
- retrieval,
- evidence collection,
- path order,
- grounding,
- relation selection,
- stopping,
- answer generation.

A single answer-accuracy metric cannot identify where failure occurred.

Model graders can evaluate semantic properties, but they are probabilistic and may themselves be unstable.

## Decision

Use a layered evaluation architecture.

### 1. Structured runtime trace

Represent agent execution explicitly with:

```text
AgentRunTrace
```

### 2. Deterministic graders first

Use deterministic logic whenever the benchmark provides sufficient structure.

Examples:

- evidence coverage,
- path order,
- repeated search,
- exact-span grounding,
- relation alignment from extraction patterns.

### 3. Model graders only for properties not captured deterministically

Model judges may supplement deterministic graders, but must be evaluated against fixed gold cases before being trusted.

### 4. Report a metric vector, not one composite score

Keep:

- answer correctness,
- evidence sufficiency,
- path quality,
- grounding,
- relation alignment,
- efficiency,
- stopping,
- planner failure

as separate fields.

## Rationale

This preserves causal interpretability.

Example:

```text
Semantic planner:
perfect path
+ grounded answer
+ wrong relation
```

is fundamentally different from:

```text
Rule planner:
no initial query
+ no retrieval
```

even though both reduce aggregate answer accuracy by one task.

## Consequences

### Positive

- failures are localizable,
- graders are testable,
- model judges are not treated as authoritative,
- planner comparisons become more informative,
- later RL/reward design can use structured signals.

### Negative

- evaluation is more complex,
- benchmark annotations must support deterministic grading,
- some open-domain semantic properties still require probabilistic judges,
- metric vectors are harder to summarize than one scalar.

## Rejected alternative

### One composite agent score

Rejected because weighting choices are arbitrary and hide failure structure.

### Model judge for all properties

Rejected because deterministic properties should not be delegated to a probabilistic model unnecessarily.

## Final decision

Adopt deterministic-first, layered, trace-based agent evaluation as the default architecture for subsequent phases.
