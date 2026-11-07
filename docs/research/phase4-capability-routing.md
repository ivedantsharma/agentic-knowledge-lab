# Phase 4 — Capability Routing Across Model Sizes

## What the capacity ablation taught us

The same verifier prompt produced fundamentally different behavior.

### 0.5B

```text
wrong candidate → YES
wrong candidate → YES
correct candidate → YES
correct candidate → YES
```

### 1.5B

```text
wrong candidate → NO
wrong candidate → NO
correct candidate → YES
correct candidate → YES
```

This is not a formatting improvement.

It is a semantic reasoning improvement.

## Capability routing

A naive architecture chooses one model for the entire agent.

A capability-routed architecture chooses models by demonstrated strength.

For this project:

```text
cheap semantic model
→ bootstrap routing

small generative model
→ continuation query generation

larger verifier model
→ relation-sensitive STOP validation

deterministic code
→ hard grounding constraint
```

## Why this is useful

The largest model is not automatically used everywhere.

Instead:

- cheap components handle easy operations,
- more expensive components handle difficult semantic checks,
- deterministic code enforces invariants.

This creates a cost/capability tradeoff that can later be measured explicitly.

## New STOP policy

The final candidate must satisfy:

```text
candidate exists
AND
candidate is grounded in evidence
AND
1.5B verifier says relation aligned
```

Only then may the planner STOP.

Otherwise it continues searching.
