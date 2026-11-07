# Phase 4 — What the Successful Hybrid Trace Proves

## The central result

The planner encountered a tempting intermediate answer:

```text
Cirrus
```

It was:

- present in evidence,
- topically relevant,
- wrong for the requested relation.

The 1.5B relation verifier rejected it.

That allowed the agent to continue searching and retrieve the final manual.

## Why this matters

A weaker architecture would have stopped at:

```text
Cirrus
```

because it was grounded.

The successful architecture distinguishes:

```text
grounded
from
relation-correct
```

This is the main technical lesson from the Phase 4 stopping-policy work.

## Capability routing

The final mechanism is intentionally heterogeneous.

Different components solve different problems:

- embeddings identify the initial anchor,
- the 0.5B model generates continuation queries,
- the 1.5B model performs relation-sensitive verification,
- deterministic code enforces exact grounding.

This is better supported by experiment than using one model everywhere.

## What is still missing

The current result is a mechanism validation.

Phase 4 is not complete until we evaluate:

- search success,
- stop precision,
- premature-stop rate,
- step efficiency,
- answer accuracy,
- planner failure rate,
- behavior across more than one task.

The next milestone is therefore evaluation, not another architecture change.
