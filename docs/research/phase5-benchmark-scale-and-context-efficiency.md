# Phase 5 — When a Benchmark Cannot Measure the Intended Benefit

## EXP-049 result

Three-level retrieval preserved evidence but did not reduce context compared with full sections.

This does not imply chunk retrieval is useless.

It means the current benchmark cannot measure the intended advantage.

## Why benchmark scale matters

If a section contains only 12 words:

```text
section ≈ local chunk window
```

There is almost nothing to compress.

If a realistic section contains 150–500 words, a 20–40 word local evidence window can be much smaller than the full section.

## Research lesson

A negative result can indicate either:

1. the method does not work, or
2. the benchmark does not exercise the dimension the method is designed to improve.

We should distinguish these before changing architecture.

## Next requirement

Create longer structured sections where:

- each section contains multiple unrelated facts,
- the target evidence occupies a local span,
- distractor facts exist before and after the answer,
- section-level retrieval remains meaningful.

Then compare:

```text
full retained section context
vs
deduplicated local chunk windows
```

with evidence retention held constant.
