# Phase 3 — Deterministic Multi-Hop Execution

## What are we testing now?

We already know the full one-shot question retrieves the wrong document first.

Now we give the system the correct decomposition:

```text
Hop 1:
Which team operates Atlas?

Hop 2:
Which storage system is maintained by Platform Reliability?

Hop 3:
What is the incremental backup cadence for Borealis?
```

Each hop is retrieved independently.

## Why is this still not an agent?

Because the queries are stored in the benchmark.

The system is not deciding:
- what to search,
- how many hops to use,
- what intermediate fact to extract,
- when to stop.

Those abilities belong to Phase 4.

For now we isolate a simpler question:

> If we know the correct search sequence, can our retriever execute the evidence chain?

## New metrics

### Hop Accuracy

Fraction of hops whose top-1 retrieved document is correct.

Example:

```text
expected:  A → B → C
retrieved: A → X → C

Hop Accuracy = 2 / 3
```

### Exact Chain Match

This is stricter.

```text
expected:  A → B → C
retrieved: A → B → C
Exact Chain Match = 1
```

Any wrong hop makes it zero.

Why?

Because multi-hop retrieval is sequential.

If an early hop fails, later search planning can be corrupted even if another document happens to be retrieved correctly.
