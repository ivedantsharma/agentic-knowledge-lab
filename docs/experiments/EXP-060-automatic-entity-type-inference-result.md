# EXP-060 Result: Automatic Lexical Entity-Type Inference

## Aggregate

```text
TypeInferenceAccuracy=0.6667
ResolvableEntityAccuracy=0.5000
AbstentionAccuracy=1.0000
FalsePositiveResolutionRate=0.0000
```

## What worked

Service mentions with only service-type cues resolved correctly.

Unrelated negatives still abstained perfectly.

## Failure pattern

Two positive team mentions failed:

```text
"team operating the Atlas authentication service"

"group maintaining the production session metadata cache"
```

The strict lexical type inferer saw cues for both types:

```text
team + service

group + cache
```

and returned no type.

## Diagnosis

Not every type word in a mention describes the referent.

In:

```text
team operating the Atlas authentication service
```

the referent is the `team`.

The later word `service` describes the object operated by that team.

The strict "all type cues must agree" rule is therefore too conservative for relational noun phrases.

## Next experiment

EXP-061 compares the strict rule with an earliest-cue/head-like heuristic while keeping the semantic ranker, threshold, and benchmark fixed.
