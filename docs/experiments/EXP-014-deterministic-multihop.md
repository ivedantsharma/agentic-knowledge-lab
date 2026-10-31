# EXP-014: Deterministic Multi-Hop Retrieval

## Goal

Test whether decomposing a compositional question into ordered retrieval hops fixes the failure observed in the one-shot dense baseline.

## Task

Question:

```text
What backup cadence is used by the storage system maintained by the team that operates Atlas?
```

Gold chain:

```text
org_atlas
→ org_platform_reliability
→ manual_borealis
```

## Results

### Hop 1

Query:

```text
Which team operates Atlas?
```

Expected:

```text
org_atlas
```

Retrieved:

```text
org_atlas
```

Cosine score:

```text
0.686297
```

### Hop 2

Query:

```text
Which storage system is maintained by Platform Reliability?
```

Expected:

```text
org_platform_reliability
```

Retrieved:

```text
org_platform_reliability
```

Cosine score:

```text
0.800256
```

### Hop 3

Query:

```text
What is the incremental backup cadence for Borealis?
```

Expected:

```text
manual_borealis
```

Retrieved:

```text
manual_borealis
```

Cosine score:

```text
0.721497
```

## Metrics

```text
HopAccuracy = 1.0000
ExactChainMatch = 1.0000
```

## Comparison with single-hop baseline

Single-hop dense search:

- top-1 was a distractor,
- final answer document ranked 4th.

Deterministic multi-hop search:

- all three hops correct,
- complete ordered evidence chain recovered.

## Interpretation

The retriever itself was capable of finding each required document when given a focused query.

The main failure in the one-shot baseline was query composition.

This establishes an important Phase 3 result:

> Multi-hop decomposition can recover an evidence chain that a single compositional query fails to retrieve reliably.

## Limitation

The hop queries are still benchmark-provided.

The system has not yet:
- extracted the intermediate fact automatically,
- generated the next query from that fact,
- decided how many hops are needed,
- decided when to stop.

Those are the next steps.
