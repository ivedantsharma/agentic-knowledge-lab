# EXP-078: Deterministic Relation-Alignment Grader

## Research question

Can a deterministic grader distinguish:

```text
answer appears in evidence
```

from:

```text
answer fills the exact relation requested by the task
```

## Trigger from EXP-077

The semantic planner's OOD run produced:

```text
EvidenceCoverage=1.0000
AnswerGrounded=True
AnswerCorrect=False
GroundedButWrong=True
```

The consumed Cirrus manual contains both the retry count and the dead-letter destination.

Therefore document-level groundedness cannot distinguish the requested relation.

## Existing benchmark signal

Each final hop already contains an `extraction_pattern`.

Example:

```text
sent to the (.+?) dead-letter queue
```

Applied to the gold final evidence document, this extracts:

```text
CIRRUS-DLQ
```

## Deterministic relation-alignment rule

A stopped answer is relation-aligned when:

1. the final expected evidence document was actually consumed,
2. the final-hop extraction pattern matches that document,
3. the stopped answer equals the extracted relation value after normalization.

## Why this is stronger than grounding

```text
five times
```

is grounded in the Cirrus manual.

But it is not captured by:

```text
sent to the (.+?) dead-letter queue
```

Therefore it is grounded but relation-misaligned.

## Controlled setup

Keep fixed:

- Phase 4 tasks,
- Phase 4 corpus,
- RuleBasedPlanner,
- SemanticPlanner,
- DenseSearchTool,
- trace recording,
- exact-span groundedness.

Add only the deterministic relation-alignment grader.

## Limitation

This grader relies on benchmark-authored extraction patterns.

It is suitable for controlled evaluation, not a general open-domain semantic judge.

Model-based relation grading remains a later Phase 8 experiment.
