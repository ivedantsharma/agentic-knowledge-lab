# EXP-056 Result: Semantic Entity Ranking Diagnostic

## Aggregate

```text
LexicalAbstentionRate=1.0000
SemanticHit@1=0.5000
SemanticHit@3=1.0000
PositiveTopScores=[0.545878, 0.498791]
NegativeTopScores=[0.311179, 0.322663]
```

## Positive finding: score separation

The lowest positive top score is approximately:

```text
0.4988
```

The highest unrelated-negative top score is approximately:

```text
0.3227
```

On this tiny diagnostic set, positive and unrelated top-score ranges are separated.

This suggests semantic confidence may help distinguish some resolvable questions from unrelated questions.

## Critical failure: top-1 entity can still be wrong

For:

```text
Which service is maintained by the infrastructure reliability group?
```

the ranking was:

```text
1. borealis              0.498791
2. platform_reliability  0.491856  <- gold
```

Therefore a threshold on the top score would accept the wrong entity.

## Diagnosis

The ranker embeds the entire question.

The question contains two semantic roles:

- the entity mention to resolve: "infrastructure reliability group",
- the requested answer type: "service".

Borealis is highly compatible with the full question because it is a service maintained by Platform Reliability.

The semantic ranker is therefore partly performing answer retrieval rather than mention linking.

## Conclusion

Do not convert semantic top-1 into an entity link yet.

The next experiment should isolate the entity mention span from the rest of the question.
