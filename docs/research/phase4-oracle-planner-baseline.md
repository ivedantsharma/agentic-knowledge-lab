# Phase 4 — Oracle Planner Baseline

## Purpose

The oracle planner is not an autonomous agent.

It knows the benchmark's gold hop sequence.

Its purpose is to validate the new agent architecture:

```text
planner
→ action
→ tool
→ observation
→ state update
→ planner
```

## Action space

The initial action space is intentionally tiny:

```text
SEARCH(query)
STOP(answer)
```

Later we may add actions only if experiments require them.

## Search tool abstraction

Dense retrieval is now wrapped behind a search-tool interface.

The planner does not directly compute embeddings or cosine similarity.

It only requests:

```text
SEARCH("Which team operates Atlas?")
```

The tool returns ranked documents.

This separation will let future planners use the same executor while we compare different planning policies.

## Trace

Every executed action is recorded.

A trace step stores:

- step index,
- action,
- query,
- retrieved document,
- extracted fact,
- metadata.

This becomes essential later for agent evaluation.

## Expected result

Because the oracle planner follows the known Phase 3 plan, it should preserve the existing 100% answer accuracy.

If it does not, the new agent loop has introduced a regression.
