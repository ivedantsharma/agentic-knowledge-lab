# Phase 4 — Diagnosing Generative Planner Protocol Failures

## Observed failure

The first local generative-planner run failed with:

```text
generative planner output must start with SEARCH: or STOP:
```

This does **not** yet tell us that the model failed to reason.

It tells us that the generated text did not satisfy the action protocol.

## Why this boundary matters

A language model produces text.

Our agent executor needs a typed action.

Conceptually:

```text
model output
↓
protocol parser
↓
PlannerAction
↓
executor
```

Possible raw model output:

```text
We should search for the worker platform.
```

But the executor expects:

```text
SEARCH: Which worker platform is maintained by Developer Productivity?
```

Those two strings may express similar intent, but only the second satisfies the current machine-readable contract.

## First debugging rule

Before changing the prompt, model, or parser, inspect the raw generation.

Otherwise several variables change at once and we cannot tell what actually failed.

## Next experiment

The planner now includes the raw generation in parse errors.

We rerun the exact same model and exact same prompt.

Then we classify the failure as one of:

1. useful intent, wrong format,
2. wrong action,
3. irrelevant text,
4. empty / malformed generation.

Only after that do we decide whether to improve:

- prompting,
- output parsing,
- model capability,
- or state representation.
