# EXP-057 Result: Mention-Span Semantic Entity Ranking

## Aggregate

```text
WholeQuestionHit@1=0.5000
MentionSpanHit@1=1.0000
MentionSpanHit@3=1.0000
PositiveMentionTopScores=[0.466511, 0.489684]
NegativeMentionTopScores=[0.266007, 0.315516]
```

## Main result

Restricting the semantic query to the entity mention repaired the ranking failure from EXP-056.

For:

```text
"infrastructure reliability group"
```

the ranking changed from:

```text
whole question:
1. borealis
2. platform_reliability
```

to:

```text
mention span:
1. platform_reliability
2. atlas
3. borealis
```

## Interpretation

The primary failure in EXP-056 was query representation.

Whole-question embeddings mixed:

- the entity mention,
- the requested answer type,
- the relation expressed by the question.

Mention-focused embeddings better isolate the entity-linking objective.

## Score separation

On this diagnostic set:

```text
lowest positive top score = 0.466511
highest negative top score = 0.315516
```

There is a gap of roughly:

```text
0.151
```

This supports testing a thresholded semantic fallback.

## Important caveat

The mention spans were provided manually.

Therefore this experiment does not yet solve mention extraction.

It only shows that semantic entity ranking is effective when given an appropriate mention representation.
