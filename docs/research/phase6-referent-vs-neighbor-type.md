# Phase 6: Referent Type vs Neighbor Type

A relational mention may contain multiple entity-type words.

Example:

```text
team operating the Atlas authentication service
```

Two type words appear:

```text
team
service
```

But they play different roles.

The phrase refers to a `team`; the `service` is the object of the relation.

This distinction matters for constrained graph retrieval.

## Strict cue agreement

A rule that requires every detected type cue to agree treats the phrase as ambiguous.

That is safe but loses recall.

## Head-like cue heuristic

A lightweight alternative is to use the earliest explicit type cue in these controlled mention templates.

This approximates the referent head:

```text
team operating ...
group maintaining ...
worker platform ...
```

EXP-061 tests whether this small structural rule is sufficient before introducing a parser or learned type classifier.
