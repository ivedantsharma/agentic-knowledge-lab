# EXP-103: Causal-LM Target-Only Loss Mechanics

## Research question

Can we correctly construct a retrieval-policy SFT example so only the assistant target contributes to causal-LM loss?

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## Input

Use one training example from:

```text
phase11_policy_dataset_v0.json
```

## Procedure

1. render the system + user prompt,
2. render the full prompt + assistant target,
3. find the prompt-token boundary,
4. replace prompt labels with -100,
5. keep assistant target labels unchanged,
6. run a frozen forward pass.

No optimizer and no parameter update are used.

## Metrics / diagnostics

- prompt token count,
- full token count,
- supervised token count,
- masked token count,
- decoded supervised suffix,
- target-only loss,
- full-sequence loss.

## Important interpretation

The two loss values optimize different token sets.

Therefore:

```text
lower masked loss vs lower unmasked loss
```

is not itself a quality comparison.

The purpose is to verify that the intended target tokens are the only supervised region.

## Success criterion

The decoded supervised region must contain the target action and must not contain the user prompt.

If that holds, the preprocessing path is ready for an actual SFT update.
