# Phase 4 — Grounding Is Not Relation Alignment

## What EXP-033 exposed

The extract-or-abstain planner selected:

```text
Cirrus
```

from:

```text
Developer Productivity maintains the Cirrus worker platform...
```

The answer passed the exact-span grounding check because `Cirrus` is present in the evidence.

But the question asks:

```text
Where are failed jobs sent after retries are exhausted?
```

`Cirrus` identifies the worker platform.

It does not identify the destination after retries.

## Three separate properties

### 1. Groundedness

```text
Is the candidate supported by / present in evidence?
```

Cirrus:

```text
YES
```

### 2. Topical relevance

```text
Is the candidate related to the subject of the question?
```

Cirrus:

```text
YES
```

### 3. Relation alignment

```text
Does the candidate fill the semantic role requested by the question?
```

Question asks for:

```text
destination
```

Cirrus is:

```text
worker platform
```

Therefore:

```text
relation aligned = NO
```

## Why this matters

A grounded answer can still be wrong.

This is common in retrieval systems:

```text
Question: When was X launched?
Evidence: X was created by Alice in 2020.
Candidate: Alice
```

`Alice` is grounded and relevant, but answers WHO rather than WHEN.

## Next capability probe

Before adding another guard to the planner, test whether Qwen can explicitly verify relation alignment.

We give it:

- question,
- evidence,
- candidate answer,

and ask:

```text
Does this candidate directly answer the exact requested relation?
YES / NO
```

We test both wrong grounded candidates and correct grounded candidates.

Only if this verifier works should we integrate it into the STOP policy.
