# EXP-090: Semantic Instruction Detector Classification Probe

## Research question

Why did the semantic instruction detector delete every span in EXP-089?

## Motivation

EXP-089 showed:

```text
semantic_attack_span_removal_rate=1.0000
benign_required_fact_preservation_rate=0.0000
```

Before changing the prompt or model, isolate the detector from the rest of the pipeline.

## Controlled classifier set

Ten independently labeled spans:

### DATA

- factual statements,
- quoted injection examples,
- human procedural instructions,
- ordinary software behavior,
- reported historical attack text.

### INSTRUCTION

- direct assistant-directed attacks,
- indirect answer overrides.

## Metrics

Treat INSTRUCTION as the positive class.

Measure:

- true positives,
- true negatives,
- false positives,
- false negatives,
- accuracy,
- instruction precision,
- instruction recall,
- DATA recall.

## Why DATA recall matters

For a sanitizer, a false positive means:

```text
useful evidence
→ classified as instruction
→ deleted
```

Therefore attack recall alone is insufficient.

A useful detector needs both:

```text
high instruction recall
AND
high DATA recall
```

## Scientific purpose

This experiment diagnoses the classifier itself.

No extraction model is involved.

No sanitization pipeline is involved.

No detector prompt changes are made yet.
