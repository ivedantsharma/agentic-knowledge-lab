# EXP-102 Result: Retrieval Policy Dataset Audit

## Validation

```text
258 tests passed
ruff passed
```

## Dataset audit

```text
examples=18
split_counts={
  'train': 12,
  'dev': 3,
  'heldout': 3
}
action_counts={
  'SEARCH_HYBRID_K5': 6,
  'REFORMULATE': 3,
  'SEARCH_HYBRID_K2': 3,
  'SEARCH_HYBRID_K1': 6
}
source_tasks=6
leaked_sources={}
```

## Interpretation

The source-task-disjoint split is structurally valid.

No source task appears in more than one split, so paraphrases of the same underlying information need do not leak from training into evaluation.

## Dataset limitation

```text
SEARCH_HYBRID_K3
```

exists in the policy vocabulary but has zero positive examples in dataset v0.

Therefore later Phase 11 experiments must not claim learned competence on that action class.

## Decision

Proceed to supervised-fine-tuning mechanics:

- chat formatting,
- tokenization,
- causal-LM labels,
- prompt masking,
- target-only loss.
