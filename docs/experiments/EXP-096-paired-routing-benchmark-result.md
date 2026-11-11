# EXP-096 Result: Paired Lexical vs Semantic Routing Benchmark

## Validation

```text
247 tests passed
ruff passed
```

## Aggregate by query style

### lexical_explicit

```text
BM25:
  Recall@3=1.0000
  MRR=0.8333

Dense:
  Recall@3=1.0000
  MRR=0.7500

Hybrid RRF:
  Recall@3=1.0000
  MRR=0.8333
```

### semantic_paraphrase

```text
BM25:
  Recall@3=1.0000
  MRR=0.8056

Dense:
  Recall@3=1.0000
  MRR=0.8056

Hybrid RRF:
  Recall@3=1.0000
  MRR=0.8333
```

## Overall fixed strategies

```text
BM25:
  Recall@3=1.0000
  MRR=0.8194

Dense:
  Recall@3=1.0000
  MRR=0.7778

Hybrid RRF:
  Recall@3=1.0000
  MRR=0.8333
```

## Winner shifts

```text
borealis_backup   → shift
cirrus_retry      → shift
solstice_cache    → shift
meridian_rotation → shift
nimbus_session    → no shift
orion_logs        → no shift
```

```text
winner_shift_pairs=4
total_pairs=6
```

## Interpretation

Changing only query wording changed the winner set in four of six pairs.

Therefore query formulation materially affects relative retriever ranking.

However, query style alone is not enough to justify a router.

Hybrid RRF is:

- tied for best MRR on lexical-explicit queries,
- best MRR on semantic-paraphrase queries,
- best fixed strategy overall.

Therefore a coarse policy such as:

```text
lexical → BM25
semantic → Dense
```

would not improve over always using Hybrid.

## Important distinction

All strategies achieved:

```text
Recall@3=1.0000
```

on every paired task.

So this benchmark currently studies:

```text
ranking quality
```

rather than:

```text
evidence exposure failure
```

The adaptive-routing objective here is therefore MRR / early evidence placement.

## Next step

Measure the per-query oracle MRR on this expanded benchmark and compare it with always-Hybrid.

This quantifies how much routing value remains after using the strongest fixed strategy.
