# EXP-026: Semantic Planner Unseen-Intent Failure

## Goal

Test whether the semantic planner can handle a requested relation outside its fixed intent set.

## Task

```text
Where are failed jobs sent after the production worker
platform owned by Developer Productivity exhausts all retries?
```

Expected answer:

```text
CIRRUS-DLQ
```

## Result

The planner classified the question as:

```text
retry
```

It correctly found:

```text
Developer Productivity
→ Cirrus
→ manual_cirrus
```

But then it generated the retry-count query:

```text
How many times are failed jobs retried by the
production Cirrus worker platform?
```

The observation parser extracted:

```text
five times
```

and the planner stopped with that value.

Final result:

```text
AnswerCorrect = 0.0000
```

## Diagnosis

Retrieval reached a document that actually contained the requested answer:

```text
Jobs that exhaust retries are sent to the
CIRRUS-DLQ dead-letter queue.
```

The failure therefore came from planner intent restriction and stopping semantics.

The planner optimized for the nearest known intent rather than the original requested relation.

## Conclusion

The semantic planner is:

- robust to paraphrase,
- but closed-world over a fixed action/intent vocabulary.

This motivates open-ended query generation.
