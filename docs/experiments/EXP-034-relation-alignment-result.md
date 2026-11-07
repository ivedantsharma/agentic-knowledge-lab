# EXP-034 Result: Relation-Alignment Verifier Probe

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## Results

```text
wrong_candidate_intermediate
candidate='Cirrus'
output='YES'

wrong_candidate_owner
candidate='Developer Productivity'
output='YES'

correct_candidate_final
candidate='CIRRUS-DLQ'
output='YES'

long_correct_candidate_final
candidate='CIRRUS-DLQ dead-letter queue'
output='YES'
```

## Diagnosis

The verifier fails completely on discrimination.

Expected:

```text
NO
NO
YES
YES
```

Observed:

```text
YES
YES
YES
YES
```

Therefore Qwen2.5-0.5B-Instruct is not reliable enough to own relation-alignment verification for this benchmark.

## Important distinction

The model follows the output format.

The failure is semantic, not syntactic.

It cannot distinguish:

- a grounded but relation-wrong span,
- a grounded and relation-correct span.

## Architectural consequence

Do not integrate this verifier into the STOP policy.

Doing so would add complexity without adding a useful correctness signal.

## Next experiment

Keep the same four verifier cases and prompt.

Change only Qwen model capacity:

```text
Qwen2.5-0.5B-Instruct
→
Qwen2.5-1.5B-Instruct
```

This tests whether relation verification is below the 0.5B model's capability threshold or whether the formulation itself is flawed.
