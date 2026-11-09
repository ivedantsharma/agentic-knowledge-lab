# EXP-071: Expanded Hard Benchmark and Per-Challenge Slices

## Research question

Can KnowledgeBench v2 produce stable, interpretable retrieval diagnostics across multiple examples of each hard challenge rather than relying on a single seed case?

## Why expand now?

The seed established that the schema and challenge-aware metrics work.

However, one task per challenge is too fragile:

```text
one unusual query
→ entire challenge metric changes
```

The next dataset therefore moves from:

```text
seed
→ hard benchmark v0
```

## Hard benchmark v0

The set contains 10 tasks spanning:

- multi-hop,
- distractor,
- stale knowledge,
- contradiction,
- ambiguity,
- unanswerable.

Several tasks combine multiple challenges.

New domains include:

- Helios / Identity Foundations / Solstice,
- Security Platform / Meridian,
- Cumulus retry distractor,
- Orion ambiguity,
- cafeteria unanswerable query.

## Per-challenge evaluation

A task may belong to multiple slices.

For example:

```text
multi_hop + stale_knowledge
```

contributes to both:

```text
multi_hop
stale_knowledge
```

The evaluator therefore reports the same metrics over each challenge subset.

## Controlled baseline

Compare the same unchanged retrievers:

```text
BM25
vs
MiniLM dense
```

with:

```text
top_k = 3
```

## What success would prove

Not that the benchmark is final.

It would prove that:

- every major challenge has multiple examples,
- combined challenge labels work,
- aggregate and challenge-slice metrics can coexist,
- baseline retrievers expose distinct weaknesses across slices.

## Failure modes to watch

If every challenge slice produces identical results, the taxonomy is not adding useful information.

If one task still dominates a slice, the set needs further expansion.

If adversarial documents never enter top-k, those challenge examples are still too weak.
