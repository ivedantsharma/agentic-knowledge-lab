# Phase 6 — Confidence Thresholds Need Held-Out Evaluation

## Why not evaluate a threshold on the calibration examples?

Suppose we observe:

```text
positives > 0.46
negatives < 0.32
```

and choose:

```text
threshold = 0.39
```

Testing that threshold on the same examples tells us almost nothing.

The threshold was chosen because those examples already separated around it.

## Development versus held-out data

A basic research split is:

```text
development set
→ inspect behavior
→ choose policy / threshold

held-out set
→ evaluate policy without retuning
```

EXP-057 acts as development data.

EXP-058 is the held-out diagnostic.

## What failure would mean

If positive held-out cases fall below 0.39:

```text
false abstention
```

If unrelated held-out cases rise above 0.39:

```text
false positive entity link
```

Either result would show that raw cosine score alone is not a stable confidence estimate.

## Calibration warning

Cosine similarity is a ranking score.

It is not a calibrated probability.

A threshold that works on one synthetic dataset should not be interpreted as:

```text
score >= 0.39 means 39% confidence
```

or as a universal production threshold.
