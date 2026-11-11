# EXP-094 Result: Query Feature Diagnostic for Retriever Routing

## Validation

```text
243 tests passed
ruff passed
```

## Observed query features and winners

### kbv2-hard-001

```text
winner=dense
token_count=18
temporal_cue_count=1
relational_phrase_count=4
multi_relation_proxy=True
```

### kbv2-hard-002

```text
winner=bm25
token_count=12
temporal_cue_count=1
relational_phrase_count=0
multi_relation_proxy=False
```

### kbv2-hard-005

```text
winner=bm25
token_count=16
temporal_cue_count=1
relational_phrase_count=4
multi_relation_proxy=True
```

### kbv2-hard-006

All three strategies tied.

### kbv2-hard-007

All three strategies tied.

### kbv2-hard-010

Dense and hybrid tied.

## Main finding

Simple surface features do not cleanly separate retriever winners.

The strongest counterexample is:

```text
hard-001:
relational_phrase_count=4
multi_relation_proxy=True
→ Dense uniquely wins

hard-005:
relational_phrase_count=4
multi_relation_proxy=True
→ BM25 uniquely wins
```

The two queries also have similar lengths and identical temporal-cue counts.

Therefore a rule such as:

```text
multi-relation query → Dense
```

is not supported.

## Decision

Do not implement a hand-written query-syntax router yet.

The next diagnostic should use retrieval-aware signals available at inference time, especially ranking confidence and agreement between BM25 and Dense.
