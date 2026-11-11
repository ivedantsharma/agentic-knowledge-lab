# EXP-090 Result: Semantic Instruction Detector Classification Probe

## Validation

```text
237 tests passed
ruff passed
```

## Aggregate

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

## Diagnosis

The detector classified every span as:

```text
INSTRUCTION
```

Therefore its perfect instruction recall is not meaningful robustness.

It is a degenerate constant-positive classifier.

## Category behavior

Correct:

- direct attacks,
- indirect attack.

Incorrect:

- factual statements,
- quoted attack text,
- human procedures,
- ordinary software descriptions,
- reported historical attack text.

## Main conclusion

The semantic detector does not currently understand the distinction between:

```text
text that contains imperative or instruction-like language
```

and:

```text
text that is actually directing the current assistant
```

This explains EXP-089's total evidence deletion.

The next experiment should calibrate the classifier decision rule on the frozen labeled probe before returning to the end-to-end sanitizer.
