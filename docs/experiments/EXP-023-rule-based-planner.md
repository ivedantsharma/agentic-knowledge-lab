# EXP-023: Rule-Based Planner Baseline

## Goal

Remove the oracle planner's access to the benchmark hop sequence.

The planner sees only:

- original question,
- current retrieval state,
- retrieved evidence.

Execution also uses a generic observation parser rather than the current gold hop's extraction rule.

## Result

```text
tasks = 4
StoppedRate = 1.0000
AnswerAccuracy = 1.0000
```

## Interpretation

The rule-based planner successfully decided:

- when to SEARCH,
- which query to issue,
- when to STOP,
- which extracted value to return.

It did this without reading `task.hops`.

This is the first Phase 4 baseline where the planner controls the action sequence.

## Important limitation

The planner contains handcrafted rules matching the current benchmark's language and relation families.

Therefore the result does not show robust natural-language planning.

The next experiment should keep the same underlying evidence chains but paraphrase the questions.

If performance drops, the failure belongs to planner generalization rather than retrieval.
