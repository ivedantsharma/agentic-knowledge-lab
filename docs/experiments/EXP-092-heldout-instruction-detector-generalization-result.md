# EXP-092 Result: Held-Out Instruction Detector Generalization

## Validation

```text
239 tests passed
ruff passed
```

## Baseline held-out

```text
true_positive=4
true_negative=0
false_positive=8
false_negative=0

accuracy=0.3333
instruction_precision=0.3333
instruction_recall=1.0000
data_recall=0.0000
```

## Calibrated held-out

```text
true_positive=4
true_negative=2
false_positive=6
false_negative=0

accuracy=0.5000
instruction_precision=0.4000
instruction_recall=1.0000
data_recall=0.2500
```

## Delta

```text
accuracy_delta=+0.1667
instruction_precision_delta=+0.0667
instruction_recall_delta=0.0000
data_recall_delta=+0.2500
```

## Interpretation

The small improvement from EXP-091 generalized to the held-out set.

Therefore the calibration effect was not purely development-set overfitting.

However, the detector still misclassified six of eight DATA examples as INSTRUCTION.

That false-positive rate is too high for use as a sanitizer.

## Main conclusion

Prompt calibration improved the semantic detector modestly, but not enough to make it operationally useful.

The detector remains strongly biased toward the positive class.

Further tuning on this tiny benchmark would risk turning Phase 9 into a prompt-optimization exercise rather than a robustness study.

The detector prompt is therefore frozen and Phase 9 stops here.
