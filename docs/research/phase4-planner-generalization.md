# Phase 4 — Planner Generalization Stress Test

## Why paraphrase?

The rule-based planner scored 100% on the original benchmark.

But its rules explicitly look for phrases such as:

```text
team that operates
worker platform maintained by
signing service maintained by
```

That creates a risk:

> The planner may be matching benchmark wording rather than understanding the planning problem.

## Controlled stress test

We preserve:

- the same corpus,
- the same gold evidence chains,
- the same answers.

We change only:

- question wording.

This isolates planner language generalization.

## Example

Original:

```text
How many retry attempts are used by the worker platform
maintained by Developer Productivity?
```

Paraphrase:

```text
Developer Productivity owns a worker platform.
What is the maximum number of retries a failed job gets there?
```

The retrieval problem is unchanged.

Only the planner's interpretation of the question is stressed.

## Metrics

We report:

- InitialPlanRate
- StoppedRate
- AnswerAccuracy

If InitialPlanRate drops, the planner cannot even form a first action.

If it forms a plan but AnswerAccuracy drops, we inspect later query generation and stopping.

## Expected scientific value

A failure here is useful.

It would demonstrate why handcrafted symbolic rules are a baseline rather than the final agentic planner.

That gives us a justified reason to introduce model-based query planning next.
