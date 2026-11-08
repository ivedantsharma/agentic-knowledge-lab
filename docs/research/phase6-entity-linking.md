# Phase 6 — Entity Linking Before Relation Planning

## What is entity linking?

Entity linking maps text in a question to a stable graph node.

```text
"Atlas"
→ entity_id = atlas
```

The graph should operate on stable IDs, not raw strings.

## Why not use embeddings immediately?

If the question contains an exact known entity name, semantic retrieval adds unnecessary uncertainty.

A useful capability hierarchy is:

```text
exact name
→ registered alias
→ semantic/entity model
→ unresolved/abstain
```

Each stronger mechanism should be introduced only when the simpler one fails.

## Longest-match rule

Names can overlap.

For example:

```text
Atlas
Atlas Analytics
```

A resolver should prefer the longest explicit surface rather than matching `Atlas` inside `Atlas Analytics`.

## Ambiguity matters

Entity linking should not silently guess when equally strong surfaces map to different entities.

Ambiguous linking is an explicit failure mode that later benchmarks should measure.

## Phase 6 experiment ladder

```text
EXP-053:
gold entity + gold relations

EXP-054:
resolved entity + gold relations

later:
resolved entity + predicted relations

later:
graph/text hybrid retrieval
```

This removes oracle assumptions one at a time.
