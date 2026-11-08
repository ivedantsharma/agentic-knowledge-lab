# Phase 6 Foundations: Knowledge Graphs and Claim/Evidence Retrieval

## Central research question

Can explicit entity, relation, and claim structure improve retrieval when the answer depends on relationships rather than only textual similarity?

## From text retrieval to graph retrieval

Text retrieval asks:

```text
Which text is relevant to this query?
```

Graph retrieval asks:

```text
Which entity are we at?
Which relation should we follow?
Which claim supports that edge?
Where is the evidence for that claim?
```

## Entity

An entity is a stable node representing something in the knowledge base.

Examples:

```text
Atlas
Platform Reliability
Borealis
```

The entity ID is the stable machine-facing identity.

The display name is human-facing.

## Relation

A relation is a typed edge.

Example:

```text
Atlas --operated_by--> Platform Reliability
```

Relations are directional.

`operated_by` is not automatically interchangeable with `operates`.

## Claim

A claim is a subject-relation-object assertion:

```text
(subject, relation, object)
```

The object may be another entity:

```text
Atlas --operated_by--> Platform Reliability
```

or a literal value:

```text
Borealis --incremental_backup_cadence--> "every six hours"
```

## Evidence

A graph edge should not be treated as self-justifying.

Each claim points back to textual evidence:

```text
claim
→ source document
→ evidence text
```

This turns a plain knowledge graph into a claim/evidence graph.

## Why provenance matters

Without provenance, graph traversal can return an answer but cannot explain where the edge came from.

For a knowledge system, we want:

```text
answer
+ path
+ source evidence
```

## EXP-053 baseline

The first Phase 6 baseline uses:

- gold start entity,
- gold relation path,
- deterministic traversal,
- no LLM,
- no semantic relation prediction.

This isolates graph mechanics.

Later experiments will make entity resolution and relation selection progressively less oracle-like.
