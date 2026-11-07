# EXP-027: Few-Shot Generative Planner Prompt

## Motivation

The zero-shot FLAN-T5-small planner produced:

```text
retry attempts are sent to the production worker platform.
```

This failed in two ways:

1. it did not obey the required SEARCH / STOP action protocol,
2. it did not preserve the requested relation.

The question asked for a destination after retries were exhausted.

The model instead generated a malformed statement about retry attempts and the worker platform.

## Why not loosen the parser first?

A tolerant parser helps when the model expresses the correct action in the wrong syntax.

That is not what happened here.

The raw output did not contain a usable search query or correct final answer.

Therefore parser relaxation would hide the underlying model failure.

## Why few-shot prompting?

Zero-shot prompting gives instructions only.

Few-shot prompting adds demonstrations of the desired behavior.

The new prompt contains three examples:

- no evidence yet → SEARCH for an intermediate relation,
- evidence is relevant but incomplete → SEARCH for the missing relation,
- evidence directly answers the question → STOP with the answer.

The examples use different entities and facts from the benchmark so they demonstrate the behavior without supplying the benchmark answer.

## Experimental variable

Only the prompt changes.

We keep:

- the same FLAN-T5-small model,
- the same OOD task,
- the same retriever,
- the same state representation,
- the same parser,
- the same generation settings.

This lets us attribute any behavior change to few-shot prompting.

## What to inspect

The most important output is still:

```text
raw_output='...'
```

Possible outcomes:

1. correct SEARCH / STOP action,
2. useful action but wrong protocol,
3. correct protocol but wrong relation,
4. unrelated generation.

Only after observing that output should we consider tolerant parsing or constrained decoding.
