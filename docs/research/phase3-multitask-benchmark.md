# Phase 3 — Multi-Task Benchmark Expansion

## Why expand now?

All previous Phase 3 experiments centered on one Atlas → Platform Reliability → Borealis chain.

That is useful for debugging, but it is too small for evaluating a general multi-hop architecture.

A system can accidentally overfit to:
- one relation pattern,
- one hop count,
- one qualifier,
- one answer type.

## Benchmark v4

We now include multiple independent chains.

Examples include:

- Atlas → Platform Reliability → Borealis → backup cadence,
- Developer Productivity → Cirrus → retry limit,
- Helios → Identity Foundations → Solstice → cache duration,
- Security Platform → Meridian → key-rotation cadence.

The benchmark includes both:
- two-hop tasks,
- three-hop tasks.

It also includes environment qualifiers such as production versus staging/development.

## Aggregate evaluation

Per-task scores are still useful for failure analysis.

But we now also report:

- aggregate Hop Accuracy,
- Exact Chain Match Rate,
- aggregate Fact Accuracy,
- Answer Accuracy.

## Why this matters

A multi-hop system should be judged across chains, not only on one successful trace.

This is the first Phase 3 step toward a benchmark rather than a demo.
