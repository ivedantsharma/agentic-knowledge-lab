# EXP-015: Gold-Fact Query Chaining

## Result

Gold intermediate facts were inserted into query templates.

All retrieval hops remained correct:

```text
HopAccuracy = 1.0000
ExactChainMatch = 1.0000
```

## Interpretation

Replacing fully resolved hop queries with templates did not change retrieval quality.

This validates the query-rendering mechanism.

## Remaining shortcut

The executor still used:

```text
previous_fact = hop.expected_fact
```

Therefore it did not yet obtain intermediate facts from retrieved evidence.

The next experiment removes this shortcut.
