# EXP-098 Result: Adaptive Top-K Budget Oracle

## Validation

```text
251 tests passed
ruff passed
```

## Per-task minimal budget

```text
kbv2-hard-001 → k=5
kbv2-hard-002 → k=5
kbv2-hard-005 → k=3
kbv2-hard-006 → k=2
kbv2-hard-007 → k=1
kbv2-hard-010 → k=1
```

## Fixed budget recall

```text
k=1 → mean recall=0.5556
k=2 → mean recall=0.6389
k=3 → mean recall=0.6944
k=5 → mean recall=0.8889
```

## Oracle summary

```text
mean_minimal_k=2.8333
max_required_k=5
```

## Main finding

The required retrieval budget varies materially by task.

Therefore adaptive top-k has substantially more evidence behind it than retriever selection on this benchmark.

## Saturation failure

kbv2-hard-005 is qualitatively different:

```text
Recall@1=0.0000
Recall@2=0.0000
Recall@3=0.3333
Recall@5=0.3333
```

Increasing k does not recover the full evidence chain.

This indicates a query-formulation or multi-step retrieval failure rather than only insufficient candidate budget.

## Decision

Do not build a top-k predictor from six tasks yet.

First test whether query transformation repairs the saturated multi-hop case.

If transformation succeeds, Phase 10 should distinguish:

```text
budget adaptation
from
query adaptation
```

rather than treating all retrieval failures as top-k problems.
