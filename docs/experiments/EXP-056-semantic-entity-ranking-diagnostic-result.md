# EXP-056 Result: Semantic Entity Ranking Diagnostic

## Aggregate

```text
LexicalAbstentionRate=1.0000
SemanticHit@1=0.5000
SemanticHit@3=1.0000
PositiveTopScores=[0.545878, 0.498791]
NegativeTopScores=[0.311179, 0.322663]
```

## Positive score separation

The two positive questions produced substantially higher top semantic scores than the unrelated negatives.

```text
positive minimum top score = 0.498791
negative maximum top score = 0.322663
```

This suggests semantic profiles contain useful signal.

However, the sample is too small to justify a production threshold.

## Critical failure

For the paraphrased Platform Reliability question:

```text
Borealis              0.498791
Platform Reliability  0.491856
```

The correct start node ranks second.

A simple threshold on the top score would therefore accept the wrong entity.

## Diagnosis

The semantic ranker matches the question to the correct local graph neighborhood but does not understand which node plays the required graph role.

Borealis and Platform Reliability share evidence:

```text
Platform Reliability maintains the Borealis storage system...
```

Both profiles therefore look relevant.

The missing signal is structural:

```text
maintains_storage_system
requires the start node to be a subject of that relation
```

## Conclusion

Do not implement:

```text
semantic top-1 + score threshold
```

yet.

The next experiment should test whether the known first relation can constrain semantic candidate ranking to structurally valid start nodes.
