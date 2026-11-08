# EXP-058: Held-Out Thresholded Semantic Entity Resolution

## Research question

Does a confidence threshold calibrated from EXP-057 separate resolvable mention spans from unrelated mention spans on a new held-out set?

## Development observation from EXP-057

```text
lowest positive score = 0.466511
highest negative score = 0.315516
```

A provisional threshold of:

```text
0.39
```

is selected between those ranges.

## Important methodology

EXP-057 is treated as development/calibration data.

EXP-058 uses new questions.

The threshold must not be changed after viewing EXP-058 merely to make the held-out set pass.

If it fails, the failure is evidence that a single cosine threshold is not robust enough.

## Fixed components

- MiniLM embedding model,
- entity profiles,
- mention-span representation,
- cosine similarity,
- graph.

## New component

```text
top semantic candidate
→ accept only if score >= 0.39
→ otherwise abstain
```

## Metrics

- OverallAccuracy
- ResolvableEntityAccuracy
- AbstentionAccuracy
- FalsePositiveResolutionRate

## Limitation

Mention spans remain oracle-provided.

This experiment validates only candidate ranking + confidence gating.
