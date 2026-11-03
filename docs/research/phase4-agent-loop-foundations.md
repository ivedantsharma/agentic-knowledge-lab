# Phase 4 — Agentic Search Planner Foundations

## What changes from Phase 3?

Phase 3 assumed the retrieval plan was already known.

The executor received:

- the next query template,
- the extraction rule,
- the number of hops,
- the stopping point.

Phase 4 separates **planning** from **execution**.

## Core loop

```text
question
↓
planner observes state
↓
planner chooses action
↓
executor performs action
↓
state is updated
↓
planner observes new state
↓
...
↓
STOP
```

This is an agent loop.

## Three separate responsibilities

### Planner

Decides what should happen next.

Examples:

```text
SEARCH("Which team operates Atlas?")
STOP("every six hours")
```

### Executor

Carries out the action.

For a SEARCH action it may:

1. call the retriever,
2. get documents,
3. extract evidence,
4. update state.

The executor should not decide the high-level plan.

### State

Stores what the system currently knows.

It may contain:

- original question,
- current retrieval state,
- step number,
- search history,
- retrieved evidence,
- previous actions,
- final answer.

## Why separate them?

Suppose an agent returns the wrong answer.

Without separation, we only know:

```text
system failed
```

With separation, we can ask:

- Did the planner choose a bad query?
- Did retrieval return the wrong document?
- Did extraction produce the wrong fact?
- Did the planner stop too early?
- Did the planner continue too long?

This separation is essential for evaluation.

## First baseline: oracle planner

We will NOT immediately ask an LLM to plan.

First we build an oracle planner that reads the benchmark's known hop sequence.

Why?

Because it gives us a reference implementation of the agent loop.

If the oracle planner fails, the problem is in:

- the loop,
- execution,
- state handling,
- or trace recording.

Only after this works do we replace the oracle with a planner that must decide for itself.
