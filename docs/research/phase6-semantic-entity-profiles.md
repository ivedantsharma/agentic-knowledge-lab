# Phase 6 — Semantic Entity Profiles and Abstention

## Why entity profiles?

An entity name alone may not express what the entity does.

```text
Borealis
```

does not lexically reveal:

```text
customer-profile storage platform
```

But graph evidence does.

A semantic entity profile can combine identity with local graph context:

```text
name
+ type
+ aliases
+ neighboring claim evidence
```

## Why ranking before resolving?

Nearest-neighbor retrieval always has a first place.

That does not mean the first place is correct.

For an unrelated question, some graph entity will still receive the highest similarity score.

Therefore:

```text
rank 1
!=
safe entity link
```

## Threshold calibration

A semantic resolver needs evidence that positive matches score differently from negatives.

We should inspect:

```text
positive top-score distribution
vs
negative top-score distribution
```

before choosing a threshold.

## Hybrid design direction

The eventual capability stack should look like:

```text
exact name / alias
→ lexical resolve

otherwise
→ semantic ranking
→ confidence / threshold check

low confidence
→ abstain
```

This preserves deterministic precision where possible and uses semantic matching only as a fallback.
