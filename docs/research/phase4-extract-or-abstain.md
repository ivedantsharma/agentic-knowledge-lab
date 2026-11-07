# Phase 4 — Extract-or-Abstain Stopping

## Why exact-span grounding was not enough

The previous STOP gate required the candidate answer to appear literally in the evidence.

That prevented unsupported hallucinations.

However, the model selected:

```text
Developer Productivity
```

from:

```text
Developer Productivity maintains the Cirrus worker platform...
```

This span is grounded, but it answers the wrong relation.

Therefore:

```text
grounded
!=
correctly answers the question
```

## New formulation

Instead of:

```text
Is this evidence sufficient? YES/NO
↓
Extract an answer
```

we ask a single stricter task:

```text
If the evidence directly contains the answer,
copy the shortest exact answer span.

Otherwise:
INSUFFICIENT
```

This is called **extract-or-abstain**.

## Why combine the decisions?

The old pipeline allowed an early false-positive answerability decision.

Once the model said YES, it searched the document for some plausible answer span.

The new formulation ties sufficiency directly to extraction.

If no span directly answers the requested relation, the correct output is:

```text
INSUFFICIENT
```

## Planner behavior

```text
extract_or_abstain(question, evidence)
↓
INSUFFICIENT
    → generate next query
    → SEARCH

exact grounded span
    → STOP
```

The deterministic grounding check remains as a second guard.

## Research lesson

Abstention is not merely a fallback.

It is an explicit capability:

```text
know when the current evidence does not support an answer
```

For knowledge agents, reliable abstention is often as important as answer generation.
