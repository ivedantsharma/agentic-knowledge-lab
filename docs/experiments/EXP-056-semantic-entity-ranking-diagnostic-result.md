# EXP-056 Result: Semantic Entity Ranking Diagnostic

## Aggregate

```text
LexicalAbstentionRate=1.0000
SemanticHit@1=0.5000
SemanticHit@3=1.0000
PositiveTopScores=[0.545878, 0.498791]
NegativeTopScores=[0.311179, 0.322663]
```

## Positive case 1

Question:

```text
What is the backup cadence of the customer-profile storage platform?
```

Ranking:

```text
1. borealis              0.545878  correct
2. platform_reliability  0.323625
3. solstice              0.300118
```

This is a successful implicit-entity semantic match.

## Positive case 2

Question:

```text
Which service is maintained by the infrastructure reliability group?
```

Ranking:

```text
1. borealis              0.498791
2. platform_reliability  0.491856  correct
3. atlas                 0.450390
```

The gold entity is rank 2.

## Negative cases

Unrelated questions receive lower top scores:

```text
payroll database question → 0.311179
office catering question  → 0.322663
```

There is useful score separation between these negatives and the two positive questions.

## Why thresholding is not yet justified

A threshold below approximately 0.49 would accept the second positive question, but its rank-1 entity is wrong.

Therefore:

```text
high semantic score
!=
correct entity role
```

A top-score threshold alone would turn the second case into a confident false-positive link.

## Diagnosis

The ranker embeds the whole question.

For:

```text
Which service is maintained by the infrastructure reliability group?
```

the question contains strong semantics about a service being maintained.

Borealis is a service connected to Platform Reliability, so its profile scores slightly higher than the team entity actually mentioned by the phrase:

```text
infrastructure reliability group
```

This is an entity-role / mention-localization failure, not simply a weak embedding model.

## Next experiment

Hold the semantic model and entity profiles fixed.

Change only the semantic query representation:

```text
whole question
→ gold entity mention span
```

This isolates semantic entity mapping from mention detection.
