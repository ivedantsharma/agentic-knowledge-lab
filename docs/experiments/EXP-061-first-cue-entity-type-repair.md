# EXP-061: First-Cue Entity-Type Repair

## Research question

Can a simple left-to-right type-cue heuristic repair EXP-060's mixed-cue failures while preserving semantic abstention?

## Motivation

EXP-060 failed on:

```text
team ... service
group ... cache
```

The original inferer treated multiple type categories anywhere in the mention as ambiguity.

## Controlled change

Keep fixed:

- graph,
- mention spans,
- MiniLM,
- entity profiles,
- semantic ranking,
- threshold = 0.39,
- task set.

Change only:

```text
type inference policy
```

from:

```text
if multiple type categories appear → abstain
```

to:

```text
scan left to right → use first explicit type cue
```

## Why this is plausible

In the current noun phrases, the leading cue identifies the referent:

```text
team operating ...
group maintaining ...
storage platform ...
worker platform ...
```

Later nouns often describe related objects rather than the entity being linked.

## Caveat

This is not a general syntactic parser.

EXP-061 is a repair diagnostic on the same task set that exposed EXP-060's failure. It should not be treated as independent held-out validation.

## Metrics

- OriginalTypeInferenceAccuracy
- FirstCueTypeInferenceAccuracy
- OriginalResolvableEntityAccuracy
- FirstCueResolvableEntityAccuracy
- FirstCueAbstentionAccuracy
- FirstCueFalsePositiveResolutionRate
