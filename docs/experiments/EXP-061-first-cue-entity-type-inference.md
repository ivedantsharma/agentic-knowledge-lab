# EXP-061: First-Cue Entity-Type Inference

## Research question

Can an earliest explicit type-cue heuristic repair relational mentions that contain both referent and object type words?

## Controlled comparison

Strict agreement:

```text
team + service
→ ambiguous
→ abstain
```

First-cue rule:

```text
team + service
→ first type cue = team
→ rank team entities
```

Everything else remains fixed:

- same six EXP-060 tasks,
- same MiniLM entity ranker,
- same entity profiles,
- same threshold = 0.39.

## Hypothesis

The first-cue heuristic should repair:

- team operating the Atlas authentication service,
- group maintaining the production session metadata cache,

without changing the unrelated-negative abstention behavior.

## Caveat

"First cue" is only a lightweight approximation to syntactic head detection.

It is useful as a deterministic baseline, not as a universal linguistic rule.
