# Phase 4 — Closed-World vs Open-Ended Planning

## What the semantic planner solved

The rule planner required exact phrases.

The semantic planner instead maps different phrasings to the same intent.

For example:

```text
"maximum number of retries"
```

and:

```text
"how many times are failed jobs retried"
```

can map to the same retry intent.

That is semantic robustness.

## What it still cannot do

The planner's action policy is still:

```text
choose one of:
backup
retry
cache
signing
```

Then use a predefined query template.

This means the planner is **closed-world**.

If a new question asks about:

- dead-letter destination,
- backup retention,
- ownership,
- deployment cadence,
- another unseen relation,

the planner has no matching intent.

A semantic classifier cannot invent a new action schema.

## Why this matters

A real agentic search system must handle questions whose decomposition was not enumerated ahead of time.

That is where generative planning becomes useful:

```text
question
↓
model proposes next search query
↓
tool result
↓
model updates plan
↓
search / stop
```

## Before adding a generative model

We should first create an out-of-distribution planner benchmark that contains a relation absent from the fixed intent set.

This gives us a concrete reason to introduce generation rather than adding an LLM simply because agents usually use one.
