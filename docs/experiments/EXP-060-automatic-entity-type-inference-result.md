# EXP-060 Result: Automatic Lexical Entity-Type Inference

## Aggregate

```text
tasks=6
TypeInferenceAccuracy=0.6667
ResolvableEntityAccuracy=0.5000
AbstentionAccuracy=1.0000
FalsePositiveResolutionRate=0.0000
```

## What worked

Service-oriented mentions were inferred correctly:

```text
"storage platform containing production customer profile data"
→ service

"worker platform running production asynchronous workloads"
→ service
```

Unrelated negatives also remained safely below the semantic acceptance threshold.

## What failed

Two positive team mentions produced no type:

```text
"team operating the Atlas authentication service"
→ None

"group maintaining the production session metadata cache"
→ None
```

## Diagnosis

The original lexical type inferer gathers every explicit type cue in the mention.

Both failed mentions contain two different cue types:

```text
team ... service
group ... cache
```

The inferer therefore treats them as ambiguous and abstains.

This is a type-parsing failure, not a semantic-ranking failure.

## Next controlled change

EXP-061 keeps the graph, mention text, MiniLM model, type-constrained semantic ranking, and threshold fixed.

Only the type inference rule changes:

```text
mixed cues → abstain
```

becomes:

```text
use the earliest explicit type cue
```

This is a lightweight noun-phrase-head heuristic rather than a general parser.
