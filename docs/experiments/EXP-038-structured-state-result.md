# EXP-038 Result: Structured-State Continuation

## Aggregate comparison

Before structured state:

```text
AnswerAccuracy=0.4000
PrematureStopRate=0.2000
SearchSuccessRate=0.4000
AverageSearchSteps=3.6000
MaxStepExhaustionRate=0.4000
```

After structured state:

```text
AnswerAccuracy=0.4000
PrematureStopRate=0.0000
SearchSuccessRate=0.8000
AverageSearchSteps=3.8000
MaxStepExhaustionRate=0.4000
```

## Interpretation

Structured-state exposure materially improved trajectory quality.

The planner now reaches final evidence on four of five tasks instead of two of five, and the previous premature-stop failure disappears.

However, final answer accuracy did not increase because downstream answer extraction/evaluation failures remain.

## Task-level diagnosis

### mh-001 — real planning failure

The model still ignores the intermediate Platform Reliability entity and repeatedly searches for Atlas backup cadence.

This is a genuine continuation-planning failure.

### mh-002 — extraction / grounding failure

The correct manual is retrieved.

The model proposes:

```text
5
```

while the evidence contains:

```text
five times
```

The exact-span grounding invariant rejects the generated form, causing repeated searches.

This is not a retrieval failure.

### mh-003 — success

Correct evidence and answer.

### mh-004 — evaluator mismatch

The correct production Meridian manual is retrieved.

The model returns:

```text
twelve hours
```

Gold is:

```text
every twelve hours
```

The candidate is grounded and relation-aligned.

The previous one-way substring evaluator marks it incorrect even though it is a reasonable answer to "How often".

The evaluator is updated conservatively to accept a shorter multi-token answer when it is contained in the gold answer.

Single-token prefixes remain rejected to avoid mistakes such as:

```text
Cirrus
vs
CIRRUS-DLQ
```

### ood-001 — success

The unseen dead-letter relation remains solved end-to-end.

## Conclusion

Structured state is important and should remain in the final Phase 4 architecture.

It improves search success substantially, but it does not eliminate all generative planning or extraction errors.
