# EXP-068 Result: Strengthened Stale and Contradictory Evidence

## BM25 rank changes

### Stale Borealis policy

```text
v0 rank = 6
v1 rank = 2
```

### Cirrus contradiction

```text
v0 rank = 8
v1 rank = 3
```

## Dense MiniLM rank changes

### Stale Borealis policy

```text
v0 rank = 4
v1 rank = 4
```

### Cirrus contradiction

```text
v0 rank = 9
v1 rank = 2
```

## Interpretation

The v1 corpus successfully makes the stale and contradictory documents retrieval-competitive.

The stale policy is now especially challenging for BM25.

The pending Cirrus policy is highly competitive for both retrievers, especially Dense.

The Aurora distractor remains strong:

```text
BM25 rank = 3
Dense rank = 1
```

## Scientific conclusion

The original zero stale/contradiction hit rates were mostly benchmark weakness rather than evidence of robust retrieval behavior.

The strengthened v1 corpus is a better basis for challenge-aware retrieval evaluation.

Supporting evidence and task questions were kept fixed, so the rank shifts are attributable to the adversarial-document wording/status changes.
