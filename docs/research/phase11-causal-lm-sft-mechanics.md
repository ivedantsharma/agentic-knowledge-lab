# Phase 11: Causal-LM SFT Mechanics

## What supervised fine-tuning actually optimizes

A causal language model predicts the next token.

For a token sequence:

```text
x1, x2, x3, ..., xn
```

the model learns probabilities such as:

```text
P(x2 | x1)
P(x3 | x1, x2)
...
P(xn | x1 ... xn-1)
```

The training loss is usually token-level cross entropy.

## Our retrieval-policy example

Conceptually the sequence is:

```text
SYSTEM
USER: <query + action definitions>
ASSISTANT: SEARCH_HYBRID_K5
```

If we train on every token, the model is rewarded for reproducing:

- the system instruction,
- the user query,
- the action definitions,
- the assistant target.

That is not the behavior we actually want to supervise.

We want the loss to focus on:

```text
ASSISTANT: <target action>
```

## The -100 mask

PyTorch/Hugging Face causal-LM loss ignores label positions equal to:

```text
-100
```

So our labels look conceptually like:

```text
input:
[prompt tokens ................ target tokens]

labels:
[-100 -100 -100 ............... target tokens]
```

The prompt remains visible as model input.

It simply does not contribute directly to the supervised loss.

## Important distinction

Masking the prompt does not mean the model cannot see the prompt.

It means:

```text
prompt = conditioning context
target = supervised prediction
```

## Why this matters

Without correct masking, a tiny dataset can spend much of its gradient signal learning to reproduce boilerplate prompt text instead of learning the policy action.

## EXP-103

EXP-103 performs no parameter update.

It validates:

- chat-template construction,
- prompt-token boundary,
- -100 masking,
- supervised-token count,
- target-only forward loss.

This is the last mechanics checkpoint before the first weight-update experiment.
