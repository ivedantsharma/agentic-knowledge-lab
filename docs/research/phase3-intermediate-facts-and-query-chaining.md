# Phase 3 — Intermediate Facts and Query Chaining

## What did we just prove?

The one-shot question failed.

The decomposed hop queries succeeded.

That means our next problem is no longer:

```text
Can the retriever find the document?
```

It becomes:

```text
Can the system use evidence from one hop
to construct the next hop?
```

## Current deterministic baseline

Right now the benchmark contains:

```text
Hop 1 query:
Which team operates Atlas?

Expected fact:
Platform Reliability

Hop 2 query:
Which storage system is maintained by Platform Reliability?
```

Notice the problem:

The next query already contains the answer from the previous hop.

So the benchmark is currently doing the chaining for us.

## The next abstraction: an intermediate fact

An intermediate fact is a value discovered at one hop that is needed later.

For this task:

```text
Atlas
↓
Platform Reliability
↓
Borealis
↓
every six hours
```

Intermediate facts are:

```text
Platform Reliability
Borealis
```

The final fact is:

```text
every six hours
```

## Next experiment

We will make the chain template explicit.

Instead of storing a fully resolved query such as:

```text
Which storage system is maintained by Platform Reliability?
```

we can represent:

```text
Which storage system is maintained by {previous_fact}?
```

Then the executor can:

1. retrieve hop 1,
2. obtain the intermediate fact,
3. substitute it into the next query template,
4. retrieve hop 2,
5. continue.

## Important caution

At first we will still use the benchmark's expected intermediate fact.

Why?

Because automatic fact extraction is a separate variable.

We want to test query chaining before mixing in extraction errors.

So the progression is:

```text
A. gold full hop queries
B. gold intermediate facts + query templates
C. extracted facts + query templates
D. generated queries
E. autonomous planning
```

This keeps the research controlled.
