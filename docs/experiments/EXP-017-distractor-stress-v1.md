# EXP-017: Distractor Stress Test v1

## Goal

Test extracted-fact multi-hop chaining against a larger corpus containing relation and entity distractors.

## Result

```text
HopAccuracy      = 1.0000
ExactChainMatch  = 1.0000
FactAccuracy     = 1.0000
AnswerCorrect    = 1.0000
```

## Interpretation

The added distractors did not change the top-1 result for any hop.

That means the current distractors are useful as sanity checks, but they are not sufficiently competitive to expose a failure.

The current pipeline remains:

```text
retrieve
→ extract
→ render next query
→ retrieve
→ extract
→ render next query
→ retrieve
→ answer
```

and still succeeds end-to-end.

## Research consequence

Do not conclude the pipeline is robust.

Instead, construct harder distractors that overlap on the exact relation and entity being queried.

Examples:

- another document saying Platform Reliability maintains a different storage system,
- another document saying Borealis incremental backups use a different cadence in a different environment,
- another Atlas-like entity whose wording is nearly identical.

The next benchmark version should create genuine ranking ambiguity.
