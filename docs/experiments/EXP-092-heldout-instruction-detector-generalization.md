# EXP-092: Held-Out Instruction Detector Generalization

## Research question

Does the small calibration gain from EXP-091 generalize to unseen instruction/data examples?

## Why held-out evaluation now

The calibrated prompt was developed after observing errors on the 10-span EXP-090 probe.

Evaluating repeatedly on that same set would risk prompt overfitting.

Therefore:

```text
EXP-090/091 probe
= development set

EXP-092
= frozen held-out set
```

The calibrated prompt is not changed before this experiment.

## Held-out set

12 new spans:

- factual evidence,
- operator procedures,
- ordinary software behavior,
- quoted attacks,
- reported attacks,
- security discussion,
- direct assistant attacks,
- indirect answer overrides.

None are copied from the development probe.

## Controlled variables

Keep fixed:

- detector model,
- decoding,
- classifier labels,
- baseline prompt,
- calibrated prompt.

Change only:

```text
development examples
→ held-out examples
```

## Metrics

Treat INSTRUCTION as positive:

- accuracy,
- instruction precision,
- instruction recall,
- DATA recall,
- confusion counts.

## Interpretation

If calibrated DATA recall improves on held-out examples while instruction recall remains high, the prompt change shows some generalization.

If the gain disappears, EXP-091 was likely probe-specific.

No further prompt tuning should occur before this held-out result is recorded.
