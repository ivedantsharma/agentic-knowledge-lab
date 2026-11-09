# EXP-077: Groundedness Is Not Task Correctness

## Research question

Can a planner stop with an answer that is explicitly present in consumed evidence but still fails to answer the requested relation?

## Trigger from EXP-076

The semantic planner on `ood-001`:

- retrieved all required documents,
- consumed `manual_cirrus`,
- stopped,
- produced the wrong answer.

The manual contains both:

- retry-count information,
- dead-letter destination information.

This creates a controlled test for:

```text
grounded
vs
correct
```

## Deterministic groundedness definition

An answer is grounded when its normalized exact text appears in at least one document actually consumed by the agent.

This is intentionally strict and simple.

It does not attempt semantic entailment.

## New diagnostic

```text
grounded_but_wrong =
answer_grounded
AND NOT answer_correct
```

This identifies answers that are supported by evidence but fill the wrong semantic role.

## Why this matters

A system can retrieve the right document and quote a real fact from it while still answering the wrong question.

Example:

```text
Question asks:
Where are failed jobs sent?

Evidence contains:
five retries
CIRRUS-DLQ

Answer:
five times
```

The answer is grounded but relation-misaligned.

## Controlled setup

Keep fixed:

- Phase 4 benchmark,
- Phase 4 corpus,
- RuleBasedPlanner,
- SemanticPlanner,
- DenseSearchTool,
- MiniLM,
- trace recording from EXP-076.

Add only the deterministic grounding grader.

## Limitation

Exact-span grounding does not handle paraphrases.

A model-based groundedness grader is deferred until deterministic behavior is understood.
