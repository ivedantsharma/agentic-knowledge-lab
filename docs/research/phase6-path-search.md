# Phase 6: Path Search versus Gold Relation Paths

Until EXP-061, graph traversal received the relation sequence directly.

Example:

```text
operated_by
→ maintains_storage_system
→ incremental_backup_cadence
```

That tests execution, not route selection.

## Candidate-path search

A graph with branches turns relation selection into a retrieval problem:

```text
start node
→ enumerate plausible structural routes
→ rank routes against the question
→ execute selected route
```

This is different from free-form text retrieval because candidate routes must obey graph connectivity.

## Structural constraint

The graph itself prevents impossible relation sequences.

For example, a path cannot jump directly from Atlas to Borealis unless an edge supports it.

Semantic ranking therefore operates over structurally valid candidates rather than arbitrary generated plans.

## Current baseline

EXP-062 deliberately uses a small bounded path enumerator and MiniLM ranking.

This is a baseline, not the final graph planner.

It lets us measure whether explicit graph structure already provides useful search constraints before adding generative planning.
