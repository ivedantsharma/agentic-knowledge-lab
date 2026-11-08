# Phase 6 — Entity Resolution Failure Modes

Entity linking is not simply "find a similar name."

Different cases deserve different behavior.

## Exact mention

```text
"Atlas"
→ atlas
```

Deterministic resolution is appropriate.

## Alias

```text
"PR Team"
→ platform_reliability
```

This works only because the alias is registered explicitly.

## Overlapping names

```text
Atlas
Atlas Analytics
```

For:

```text
"Atlas Analytics"
```

matching the shorter `Atlas` node would be wrong.

The lexical resolver therefore uses longest explicit surface matching.

## Implicit entity

```text
"the customer-profile storage platform"
```

No registered surface identifies Borealis directly.

A lexical resolver should abstain rather than invent a match.

## Unregistered paraphrase

```text
"infrastructure reliability group"
```

may semantically resemble Platform Reliability, but lexical matching has no evidence that they are identical.

Again, abstention is the correct lexical behavior.

## Why this matters

Entity-link errors occur before traversal.

A single incorrect start node can make every later graph step internally consistent but completely irrelevant.

That is why entity-link accuracy and abstention should be evaluated separately.
