# Phase 4 Failure Taxonomy

## Purpose

A planner benchmark should not reduce every failure to:

```text
wrong answer
```

Different failures require different fixes.

## 1. Bootstrap planning failure

The planner cannot form the first useful search.

Example:

```text
rule-based planner on the unseen dead-letter wording
```

Symptom:

```text
planner error before retrieval
```

## 2. Intent classification failure

The planner maps a question to the wrong known goal.

Example:

```text
dead-letter question
→ classified as retry-count intent
```

The retriever may still reach the right document while the planner asks the wrong relation.

## 3. Continuation-query failure

The planner reaches an intermediate fact but formulates a poor next query.

Examples:

```text
Platform Reliability
→ jumps back to Atlas backup cadence
```

or:

```text
Cirrus + production
→ "Cirrus worker platform"
```

## 4. State-loss failure

Important intermediate information is omitted from the next planning step.

Example:

```text
Meridian + production
→ query drops production
```

This can change document ranking.

## 5. Retrieval failure

A reasonable query is generated, but the retriever does not rank the required evidence first.

This should be separated from query-planning failure.

## 6. Observation/extraction failure

The correct document is retrieved but the parser/model extracts an unusable representation.

Example:

```text
evidence = "five times"
candidate = "5"
```

The semantic answer is plausible, but exact grounding fails.

## 7. Grounding failure

The model proposes an answer not supported by the evidence.

Example:

```text
"Failed jobs are sent to the developer's own platform."
```

Deterministic exact-span grounding rejects this.

## 8. Relation-alignment failure

The answer is present in the evidence but fills the wrong semantic role.

Example:

```text
Question: Where are failed jobs sent?
Candidate: Cirrus
```

`Cirrus` is grounded but is a platform, not a destination.

## 9. Premature STOP

The planner stops before retrieving the final evidence document.

This is particularly costly because the trajectory terminates immediately.

## 10. Max-step exhaustion

The planner repeatedly searches without making progress.

Examples:

- repeated distractor retrieval,
- repeated same-document retrieval,
- inability to accept a valid answer.

## Why this taxonomy matters

The same final metric can hide different causes.

For research iteration, each failed task should first be assigned to one of these categories before changing architecture or prompts.
