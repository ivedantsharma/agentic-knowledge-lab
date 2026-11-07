# EXP-024: Rule-Based Planner Paraphrase Failure

## Goal

Test whether the non-oracle rule-based planner generalizes to paraphrased questions while keeping the corpus and evidence chains unchanged.

## Result

```text
tasks = 4
InitialPlanRate = 0.0000
StoppedRate = 0.0000
AnswerAccuracy = 0.0000
```

Every task failed before the first search.

## Diagnosis

The failure is isolated to initial planning.

Retrieval was never called.

Observation parsing was never called.

State propagation was never exercised.

Stopping was never reached.

The planner depended on exact wording patterns such as:

```text
team that operates
worker platform maintained by
signing service maintained by
```

Paraphrasing those relations caused complete failure.

## Conclusion

The rule-based planner is a useful transparent baseline, but it is brittle to linguistic variation.

This justifies introducing a semantic planner baseline.

The next planner will use embedding similarity for goal classification while preserving deterministic execution.
