# Phase 3 High-Level Design

## Goal

Support deterministic multi-hop retrieval over compositional questions.

## Pipeline

```text
MultiHopTask
↓
query template
↓
render from RetrievalState
↓
dense retrieval
↓
top document
↓
fact / qualifier extraction
↓
update RetrievalState
↓
next hop
↓
...
↓
final answer
```

## Core components

### MultiHopTask

Stores:

- task question,
- ordered evidence hops,
- expected documents,
- expected facts,
- query templates,
- extraction rules.

### RetrievalState

Carries:

- current entity,
- qualifiers,
- source document ID,
- evidence text.

### Dense retrieval

Uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

with cosine similarity.

### Fact extraction

Current Phase 3 baseline uses deterministic regex extraction.

This is intentionally simple.

The research focus is multi-hop execution and state propagation, not general-purpose information extraction.

## Evaluation

Phase 3 metrics:

- Hop Accuracy,
- Exact Chain Match,
- Fact Accuracy,
- Answer Accuracy.

These separate:

- retrieval failure,
- extraction failure,
- propagation failure,
- final-answer failure.

## Failure discovered

A hard-distractor experiment exposed a context-loss failure.

```text
Borealis + production
↓ compressed to
Borealis
↓ ambiguous query
↓ staging document wins
```

Structured state repaired the failure by preserving:

```text
qualifier = production
```

## Boundary with Phase 4

Phase 3 assumes the search plan is known.

Phase 4 removes that assumption.

The Phase 4 system will need to decide:

- what to search next,
- how to formulate the next query,
- whether another hop is necessary,
- when to stop,
- how to recover from failed searches.
