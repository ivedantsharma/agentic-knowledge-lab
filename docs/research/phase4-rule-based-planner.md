# Phase 4 — Rule-Based Planner Baseline

## What privilege was removed?

The oracle planner read:

```text
task.hops[state.step_index]
```

That gave it the gold next query and gold stopping point.

The rule-based planner does not read `task.hops`.

It sees only:

- the original question,
- the current retrieval state,
- evidence from the previous search.

## Observation parser

Execution also no longer uses the benchmark's current extraction pattern.

Instead, a deterministic observation parser maps retrieved text into:

```text
RetrievalState
├── entity
├── qualifiers
├── source_document_id
└── evidence_text
```

This is still rule-based and domain-specific.

That is acceptable for this baseline because the goal is to isolate the planner loop before adding an LLM.

## Planner behavior

The planner decides between:

```text
SEARCH(query)
STOP(answer)
```

It generates queries from:
- question structure,
- current entity,
- current qualifiers,
- semantic type implied by previous evidence.

It stops when the evidence appears to contain the final relation requested by the question.

## Safety against loops

The runner includes:

```text
MAX_STEPS = 6
```

An agent must have an external step budget even if its own stopping policy fails.

## What this experiment measures

We report:

- StoppedRate
- AnswerAccuracy
- full action trace

Later we will add richer planner metrics such as unnecessary-search count, stop accuracy, and query quality.

## Limitation

The planner rules are handcrafted for the current benchmark relation families.

This is not general natural-language planning.

It is a transparent non-LLM baseline that future autonomous planners must beat.
