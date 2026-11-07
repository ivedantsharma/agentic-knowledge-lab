# Phase 4 — Relation Verification as a Harder Reasoning Task

## What the verifier must decide

Given:

```text
question
evidence
candidate answer
```

the verifier must decide whether the candidate fills the semantic slot requested by the question.

Example:

```text
Question:
Where are failed jobs sent?

Evidence:
Developer Productivity maintains Cirrus.

Candidate:
Cirrus
```

The candidate is:

- grounded: yes,
- relevant: yes,
- relation aligned: no.

The verifier must understand that the question requests a destination, while `Cirrus` is a worker platform.

## Why this is harder than extraction

Extraction can often operate as:

```text
find a plausible span
```

Relation verification requires comparing semantic roles:

```text
requested relation
vs
candidate relation
```

This resembles natural-language inference more than span extraction.

## What EXP-034 showed

The 0.5B Qwen model answered YES to every candidate.

That means it learned the response format but not the discrimination task.

This is a useful reminder:

```text
format compliance != reasoning competence
```

## Why not keep prompt-tuning?

We already gave the model:

- the exact question,
- the evidence,
- the candidate,
- a binary output format.

The failure is now clean enough that repeated prompt edits would become ad hoc.

A better scientific next step is to test model capacity while holding the verifier formulation fixed.
