# EXP-035 Result: Qwen Relation-Verifier Capacity Ablation

## Models compared

```text
Qwen/Qwen2.5-0.5B-Instruct
Qwen/Qwen2.5-1.5B-Instruct
```

## 0.5B result

```text
Cirrus                         → YES
Developer Productivity        → YES
CIRRUS-DLQ                    → YES
CIRRUS-DLQ dead-letter queue  → YES
```

The 0.5B verifier failed to discriminate wrong from correct candidates.

## 1.5B result

```text
Cirrus                         → NO
Developer Productivity        → NO
CIRRUS-DLQ                    → YES
CIRRUS-DLQ dead-letter queue  → YES
```

This exactly matches the expected labels.

## Conclusion

Relation verification is sensitive to model capacity in this experiment.

The 1.5B model demonstrates the semantic discrimination that the 0.5B model lacked.

## Architectural implication

Use capability-specific models:

```text
SemanticPlanner
→ bootstrap

Qwen2.5-0.5B-Instruct
→ continuation query generation

Qwen2.5-1.5B-Instruct
→ relation-alignment verification

deterministic exact-span check
→ grounding invariant
```

This avoids paying the larger-model cost for every planner operation while assigning the verifier role to the model that demonstrated the capability.

## Limitation

The verifier result is based on four synthetic probe cases.

It validates the mechanism, not broad generalization.
