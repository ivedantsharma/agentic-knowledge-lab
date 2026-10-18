# Phase 3 — Multi-Hop Retrieval Foundations

## What changes in Phase 3?

Until now, our questions could be answered from one retrieval step.

Example:

```text
Question:
What is the Atlas signing-key identifier?

Search once
↓
Token Rotation section
↓
ATLAS-KV-104
```

That is single-hop retrieval.

## Multi-hop retrieval

A multi-hop question requires one fact before we know how to search for the next fact.

Example:

```text
Question:
What backup schedule is used by the storage system maintained by the team that operates Atlas?
```

Suppose the corpus contains:

```text
Document A:
Atlas is operated by Platform Reliability.

Document B:
Platform Reliability maintains Borealis.

Document C:
Borealis incremental backups run every six hours.
```

No single document directly contains the full answer path.

We need:

```text
Hop 1:
Atlas
→ Platform Reliability

Hop 2:
Platform Reliability
→ Borealis

Hop 3:
Borealis
→ every six hours
```

## Why this matters

A normal retriever receives one query and returns documents.

A multi-hop system may need to:
- retrieve evidence,
- extract an intermediate entity,
- form a new query,
- retrieve again,
- combine evidence.

This is the foundation of agentic search.

## Important separation

Phase 3 is NOT yet about autonomous planning.

We will first build deterministic multi-hop retrieval so we understand the mechanics.

Phase 4 will add the agent that decides the hops by itself.

## Research question

Can a deterministic multi-step retrieval process solve questions that a single retrieval query cannot solve reliably?

## Phase 3 research loop

```text
multi-hop benchmark
→ single-hop baseline
→ observe failure
→ deterministic decomposition
→ multiple retrieval hops
→ evidence-chain evaluation
→ failure analysis
```
