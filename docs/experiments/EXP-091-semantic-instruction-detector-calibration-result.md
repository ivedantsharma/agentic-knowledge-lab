# EXP-091 Result: Semantic Instruction Detector Prompt Calibration

## Validation

```text
239 tests passed
ruff passed
```

## Baseline

```text
true_positive=4
true_negative=0
false_positive=6
false_negative=0

accuracy=0.4000
instruction_precision=0.4000
instruction_recall=1.0000
data_recall=0.0000
```

## Calibrated

```text
true_positive=4
true_negative=1
false_positive=5
false_negative=0

accuracy=0.5000
instruction_precision=0.4444
instruction_recall=1.0000
data_recall=0.1667
```

## Delta

```text
accuracy_delta=+0.1000
instruction_precision_delta=+0.0444
instruction_recall_delta=0.0000
data_recall_delta=+0.1667
```

## Interpretation

Prompt calibration produced a small improvement.

The detector correctly reclassified one ordinary software-behavior sentence as DATA.

However, it still misclassified five of six DATA spans as INSTRUCTION.

Therefore the calibrated detector remains unusable as a sanitizer.

## Main lesson

Repeated prompt tuning on the same tiny probe would create evaluation leakage.

The calibrated prompt is now frozen.

The next experiment must use a fresh held-out classifier set before any further detector changes.
