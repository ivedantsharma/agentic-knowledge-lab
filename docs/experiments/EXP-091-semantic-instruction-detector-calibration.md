# EXP-091: Semantic Instruction Detector Prompt Calibration

## Research question

Can the same detector model distinguish assistant-directed instructions from benign instruction-like prose after clarifying the classification boundary?

## Trigger from EXP-090

The baseline detector produced:

```text
InstructionRecall=1.0000
DataRecall=0.0000
```

It classified every span as INSTRUCTION.

## Controlled variable

Keep fixed:

- model,
- 10 labeled spans,
- labels,
- decoding,
- output classes.

Change only the classifier prompt.

## Calibration change

The calibrated prompt makes the semantic boundary explicit.

### INSTRUCTION

A span directly attempts to control the current AI assistant.

### DATA

Includes:

- factual statements,
- software behavior,
- human procedures,
- quoted attacks,
- reported attacks,
- security examples,
- imperative-looking text not directed at the current assistant.

The prompt also includes small positive and negative examples.

## Comparison

Run baseline and calibrated detectors on the exact same frozen probe.

## Metrics

- accuracy,
- instruction precision,
- instruction recall,
- DATA recall,
- confusion counts.

## Success criterion

Useful calibration should increase DATA recall substantially without collapsing instruction recall.

## Important limitation

This is prompt calibration on a tiny probe.

Even a strong result would not establish generalization.

If calibration works, the next step is a fresh held-out instruction-classification set before returning to end-to-end sanitization.
