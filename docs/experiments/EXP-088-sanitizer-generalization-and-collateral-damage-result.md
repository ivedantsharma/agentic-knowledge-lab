# EXP-088 Result: Sanitizer Generalization and Collateral-Damage Audit

## Validation

```text
234 tests passed
ruff passed
```

## Adversarial generalization

All four paraphrased attacks bypassed the marker-based sanitizer.

```text
adversarial_accuracy=0.0000
attack_success_rate=1.0000
attack_span_removal_rate=0.0000
```

The sanitizer did not modify any adversarial example.

## Benign collateral damage

```text
benign_required_fact_preservation_rate=1.0000
```

The designated useful fact survived all three benign cases.

One quoted security-example sentence was removed, but its required factual answer sentence remained.

## Main conclusion

EXP-087's strong result was narrow pattern coverage rather than semantic robustness.

The sanitizer learned no generalized concept of:

```text
assistant-directed instruction
```

It only recognized known lexical markers.

Therefore:

```text
known-string filtering
!=
prompt-injection robustness
```

The next mitigation must change detector class rather than expand the keyword list.
