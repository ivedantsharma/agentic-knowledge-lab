# Phase 4 — Local Generative Planner Baseline

## Why generation now?

We have now observed two planner failures:

### Exact rule planner

Fails under paraphrase.

### Semantic intent planner

Handles paraphrase, but maps unseen relations to the nearest known intent.

The dead-letter task is the key example.

The retrieved manual actually contains the correct answer, but the semantic planner asks the wrong relation and stops on:

```text
five times
```

instead of:

```text
CIRRUS-DLQ
```

## New baseline

We introduce a small local instruction model:

```text
google/flan-t5-small
```

It receives:

- original question,
- current entity,
- qualifiers,
- latest retrieved evidence.

It must emit exactly one action:

```text
SEARCH: <query>
```

or:

```text
STOP: <answer>
```

## Why keep the action protocol strict?

Generative models can produce arbitrary prose.

The rest of our system needs typed actions.

So generation is followed by deterministic parsing into the existing PlannerAction schema.

This preserves the architecture:

```text
model
↓
text action
↓
validated PlannerAction
↓
executor
```

## What this tests

Can an open-ended model:

1. formulate a useful search query for an unseen relation,
2. keep the original question in mind after retrieval,
3. avoid stopping on an irrelevant extracted fact,
4. return the answer actually requested?

## Important caveat

FLAN-T5-small is a deliberately small baseline.

Failure would not imply generative planning is invalid.

It would tell us that model capability, prompting, or state representation needs improvement.
