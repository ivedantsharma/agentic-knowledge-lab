# Phase 6 — Semantic Similarity vs Graph Role

## Semantic relevance is not graph-role correctness

Two entities can be semantically relevant to the same sentence while playing different roles.

Example:

```text
Platform Reliability maintains Borealis.
```

Both nodes are relevant to:

```text
"Which service is maintained by the infrastructure reliability group?"
```

But the traversal start node should be:

```text
Platform Reliability
```

because it is the subject of:

```text
maintains_storage_system
```

## Structural candidate filtering

When the first relation is known, candidate start entities can be restricted to nodes with an outgoing edge of that relation.

```text
all entities
→ entities valid as subject of first relation
→ semantic ranking
```

This combines:

- semantic evidence from text,
- symbolic constraints from the graph.

## Why this is not cheating at this stage

The relation path is still intentionally oracle-provided.

Phase 6 is removing oracle assumptions one at a time.

EXP-057 tests:

```text
unknown entity
+ known first relation
```

Relation prediction remains a later experiment.

## General principle

Embedding similarity answers:

```text
"What looks related?"
```

Graph structure answers:

```text
"What is structurally allowed?"
```

A knowledge system often needs both.
