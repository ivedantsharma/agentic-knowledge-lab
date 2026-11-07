# Phase 4 — Why Planning Is Harder Than Extraction

## Three different inference problems

### Extraction

```text
Question:
Where are failed jobs sent?

Evidence:
Jobs are sent to CIRRUS-DLQ.

Task:
Return the answer.
```

This is close to span selection.

The answer already exists in the input.

### Answerability

```text
Question + evidence
↓
Does this evidence contain the requested relation?
```

This requires comparing semantics between the question and evidence.

A related fact is not enough.

For example:

```text
Question asks:
WHERE are jobs sent?

Evidence says:
jobs are retried five times
```

The evidence is relevant, but not sufficient.

### Query generation

```text
question + incomplete evidence
↓
infer what information is missing
↓
formulate a new search query
```

This is a planning operation.

The desired query may contain words that do not occur in the current evidence.

## What EXP-028 taught us

FLAN-T5-small can perform the easiest operation:

```text
grounded extraction
```

but failed the two planner-centric operations:

```text
query generation
stopping judgment
```

Therefore a single model name should not be treated as a binary property:

```text
"model works" / "model doesn't work"
```

The correct question is:

```text
Which capability is the model reliable enough to own?
```

This is an important design principle for agent systems.
