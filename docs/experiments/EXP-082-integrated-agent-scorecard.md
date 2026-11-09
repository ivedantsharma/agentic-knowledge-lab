# EXP-082: Integrated Agent Evaluation Scorecard

## Research question

Can one evaluation report decompose live agent quality into distinct process and outcome dimensions without collapsing everything into answer accuracy?

## Motivation

Phase 8 has developed separate graders for:

- trace behavior,
- evidence sufficiency,
- evidence-path order,
- groundedness,
- relation alignment,
- final answer correctness.

These should now be evaluated together on the same live runs.

## Controlled setup

Keep fixed:

- Phase 4 planner benchmark v0,
- Phase 4 OOD corpus v0,
- DenseSearchTool,
- MiniLM,
- RuleBasedPlanner,
- SemanticPlanner,
- max steps = 6.

No planner policy is modified.

## Integrated scorecard

For each task:

- AnswerCorrect
- FullEvidence
- OrderedPathComplete
- ExactPathMatch
- AnswerGrounded
- RelationAligned
- PrematureStop
- EfficientSearch
- PlannerFailed

## Why no single composite scalar?

A weighted score would hide failure structure.

For example:

```text
perfect path + wrong relation
```

and:

```text
failed retrieval + no answer
```

should not be reduced to the same opaque number.

Phase 8 therefore reports a vector of interpretable metrics.

## Expected diagnostic

The semantic planner's `ood-001` should expose:

```text
FullEvidence=True
ExactPathMatch=True
AnswerGrounded=True
RelationAligned=False
AnswerCorrect=False
```

while the rule-based planner should fail before search.

That distinction is the purpose of the integrated scorecard.

## What success would prove

The Phase 8 grader stack can diagnose where an agent failed:

```text
planning
retrieval
trajectory
grounding
relation selection
answer
```

rather than reporting only final accuracy.
