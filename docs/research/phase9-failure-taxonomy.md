# Phase 9 Adversarial Failure Taxonomy

## 1. Direct payload following

Retrieved evidence contains a malicious answer instruction and the model returns the attack payload.

## 2. Adversarial semantic drift

Injected evidence changes the semantic answer without exactly matching the attack payload.

## 3. Framing sensitivity

Attack success changes with prefix, middle, suffix, or quoted placement.

## 4. Prompt-defense amplification

A mitigation prompt increases attack success rather than reducing it.

Observed in EXP-086.

## 5. Lexical sanitizer bypass

A paraphrased attack avoids known keyword markers.

Observed in EXP-088.

## 6. Sanitizer collateral damage

Useful evidence is removed together with malicious content.

## 7. Semantic-detector collapse

The detector classifies nearly everything as malicious.

Observed in EXP-089/090.

## 8. False-positive security failure

Benign DATA is classified as INSTRUCTION and deleted.

For retrieval systems this can be as damaging as missed attacks because the answerer loses supporting evidence.

## 9. Attack recall without utility

A detector can achieve perfect instruction recall while having zero DATA recall.

This is not a useful security result.

## 10. Development-set prompt overfitting risk

Repeatedly tuning a detector prompt on the same adversarial probe can create artificial gains.

EXP-092 therefore used a frozen prompt and held-out examples.

## Core principle

Adversarial robustness must report both:

```text
attack resistance
AND
benign-task utility
```

A defense that optimizes only one side is incomplete.
