# EXP-035: Qwen Relation-Verifier Capacity Ablation

## Research question

Is the relation-alignment failure caused by insufficient model capacity or by the verifier formulation itself?

## Controlled variable

Keep fixed:

- question,
- evidence,
- candidate answers,
- verifier prompt,
- chat interface,
- deterministic decoding.

Change only:

```text
Qwen/Qwen2.5-0.5B-Instruct
→
Qwen/Qwen2.5-1.5B-Instruct
```

## Expected outputs

```text
Cirrus                         → NO
Developer Productivity        → NO
CIRRUS-DLQ                    → YES
CIRRUS-DLQ dead-letter queue  → YES
```

## Interpretation

### If 1.5B gives NO, NO, YES, YES

Model capacity is a meaningful factor for relation verification.

The larger model becomes a candidate verifier component.

### If 1.5B also says YES to everything

The binary verifier formulation itself is likely too weak or poorly conditioned.

At that point we should change the task formulation rather than keep scaling blindly.
