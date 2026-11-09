# EXP-076 Result: Live Planner Trace Recording and Deterministic Grading

## Rule-based planner

```text
AnswerAccuracy=0.8000
FullEvidenceRate=0.8000
PrematureStopRate=0.0000
EfficientSearchRate=1.0000
AverageSearchSteps=2.0000
AverageRepeatedSearches=0.0000
```

The four known-intent tasks followed complete gold evidence chains.

The OOD dead-letter task failed before any action:

```text
planner_failed=True
planner_error=rule-based planner cannot form initial query
```

## Semantic planner

```text
AnswerAccuracy=0.8000
FullEvidenceRate=1.0000
PrematureStopRate=0.0000
EfficientSearchRate=1.0000
AverageSearchSteps=2.4000
AverageRepeatedSearches=0.0000
```

## Key diagnostic

On `ood-001` the semantic planner retrieved:

```text
org_dev_productivity
manual_cirrus
```

These are exactly the task's required documents.

Therefore:

```text
FullEvidence=True
PrematureStop=False
```

but:

```text
AnswerCorrect=False
```

## Interpretation

Evidence availability is necessary but not sufficient for correct agent behavior.

The semantic planner reached the correct evidence but selected the wrong fact/relation from that evidence.

This motivates EXP-077:

```text
groundedness
vs
task correctness
```
