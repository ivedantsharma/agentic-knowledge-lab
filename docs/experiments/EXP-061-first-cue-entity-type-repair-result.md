# EXP-061 Result: First-Cue Entity-Type Repair

## Aggregate

```text
OriginalTypeInferenceAccuracy=0.6667
FirstCueTypeInferenceAccuracy=1.0000
OriginalResolvableEntityAccuracy=0.5000
FirstCueResolvableEntityAccuracy=0.7500
FirstCueAbstentionAccuracy=1.0000
FirstCueFalsePositiveResolutionRate=0.0000
```

## What was repaired

The first-cue heuristic correctly inferred the type for both mixed-cue mentions.

Example:

```text
"team operating the Atlas authentication service"
→ team
→ Platform Reliability
```

## Remaining failure

For:

```text
"group maintaining the production session metadata cache"
```

the system correctly inferred:

```text
team
```

and the correct team ranked first:

```text
Identity Foundations
score=0.372357
```

but the fixed semantic threshold was:

```text
0.39
```

so the system abstained.

## Interpretation

The remaining miss is a confidence-gating false abstention, not a ranking or type-inference failure.

The experiment therefore separates three components cleanly:

- type inference: repaired,
- semantic ranking: correct,
- fixed global threshold: brittle on one positive.

## Decision

Do not lower the threshold on this same failure example.

That would be direct benchmark tuning.

The limitation is documented and relation-path selection becomes the next Phase 6 research problem.
