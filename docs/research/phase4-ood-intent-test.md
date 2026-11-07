# Phase 4 — Out-of-Distribution Intent Test

## Why this test?

The semantic planner solved paraphrases, but it still chooses among a fixed set of goals:

- backup,
- retry,
- cache,
- signing.

We now add a question whose goal is absent from that list:

```text
Where are failed jobs sent after all retries are exhausted?
```

The answer requires a dead-letter destination relation.

## What stays constant?

The question still begins from Developer Productivity and must reach Cirrus.

The same dense retriever, observation parser, structured state, and action loop are used.

The changed variable is the requested relation.

## Expected behavior

Because the planner has no dead-letter intent, it must map the question to one of its existing prototypes.

That may cause:

- the wrong final query,
- premature stopping,
- the wrong extracted answer,
- or planner failure.

## Why this matters

If the semantic planner fails, we have demonstrated two distinct limitations:

1. rule planner: brittle to paraphrase,
2. semantic classifier: robust to paraphrase but closed-world.

That gives a principled motivation for the next architecture: a generative planner that can propose a search query not enumerated in advance.
