# EXP-038: Structured-State Generative Continuation

## Motivation

EXP-037 showed that the hybrid planner solved the unseen relation but regressed on known tasks.

The dominant failure mode was loss of structured intermediate state during query generation.

## Controlled change

Before:

```text
original question
+
latest evidence
→ generated query
```

After:

```text
original question
+
current entity
+
qualifiers
+
latest evidence
→ generated query
```

No other component changes.

## Hypothesis

Explicit state should reduce:

- repeated retrieval loops,
- skipped intermediate relations,
- environment qualifier loss.

## Expected examples

### Retry task

State:

```text
entity=Cirrus
qualifier=production
```

A better query should mention both the production Cirrus platform and retry count.

### Signing task

State:

```text
entity=Meridian
qualifier=production
```

A better query should preserve `production`, reducing the chance that the development manual outranks the production manual.

### Backup task

State:

```text
entity=Platform Reliability
```

The model should search for the storage system maintained by Platform Reliability instead of jumping back to Atlas backup snapshots.

## Evaluation

Re-run the exact EXP-037 five-task comparison.

Compare hybrid metrics before and after the state-preservation change.

Rule-based and semantic results should remain unchanged.
