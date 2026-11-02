# Phase 3 — From Chaining to Robust Multi-Hop Retrieval

## Current capability

The executor now uses information discovered from the corpus.

For the Atlas task:

```text
Atlas
↓ retrieve
Platform Reliability
↓ render next query
Borealis
↓ render next query
every six hours
```

This is the first true data-dependent retrieval chain in the project.

## Why not jump to an LLM planner yet?

Because the current corpus is very clean.

Each relation is nearly unique.

If we add an LLM now and it succeeds, we will not know whether success comes from:

- robust retrieval,
- robust extraction,
- easy data,
- or model reasoning.

So Phase 3 should first stress the deterministic architecture.

## Next benchmark version

The next corpus should include distractors such as:

```text
Atlas Analytics is operated by Developer Productivity.

Platform Reliability previously maintained Aurora.

Borealis full backups run every Sunday.

Cirrus incremental backups run every four hours.
```

These documents contain words and relations similar to the gold path.

## What failures can now happen?

### Retrieval failure

Wrong document is top-1.

### Extraction failure

Right document retrieved, wrong span extracted.

### Propagation failure

A wrong extracted fact changes the next query.

### Chain failure

An early error causes every later hop to diverge.

This is especially important because multi-hop systems amplify upstream mistakes.

## Next metrics

Our current metrics already separate:

- document retrieval,
- chain correctness,
- fact extraction,
- final answer.

The next benchmark will use the same metrics against harder data.

That lets us measure where the chain breaks instead of just observing a wrong answer.
