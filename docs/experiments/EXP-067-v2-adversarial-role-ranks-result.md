# EXP-067 Result: Adversarial Role-Rank Diagnostic

## BM25

For the Atlas/Borealis task:

```text
supporting ranks = 1, 4, 5
distractor rank  = 3
stale rank       = 6
```

For the Cirrus task:

```text
supporting ranks      = 1, 2
contradiction rank    = 8
```

## Dense MiniLM

For the Atlas/Borealis task:

```text
supporting ranks = 2, 3, 5
distractor rank  = 1
stale rank       = 4
```

For the Cirrus task:

```text
supporting ranks      = 1, 4
contradiction rank    = 9
```

## Interpretation

The Aurora distractor is a genuine retrieval stressor.

The stale Borealis document is moderately competitive for Dense but weak for BM25.

The Cirrus contradiction is too weak for both retrievers.

Therefore the zero stale/contradiction hit rates from EXP-066 should not be interpreted as robust handling of those challenge types.

The benchmark should strengthen stale and contradictory evidence before using those metrics as meaningful stress indicators.
