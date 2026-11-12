# EXP-107 Result: Existing-Corpus Oracle Policy Label Mining

## Validation

```text
267 tests passed
ruff passed
```

## Oracle labels

```text
route-001 Borealis lexical   -> SEARCH_HYBRID_K1
route-002 Borealis semantic  -> SEARCH_HYBRID_K1

route-003 Cirrus lexical     -> SEARCH_HYBRID_K2
route-004 Cirrus semantic    -> SEARCH_HYBRID_K1

route-005 Solstice lexical   -> SEARCH_HYBRID_K1
route-006 Solstice semantic  -> SEARCH_HYBRID_K2

route-007 Meridian lexical   -> SEARCH_HYBRID_K2
route-008 Meridian semantic  -> SEARCH_HYBRID_K2

route-009 Nimbus lexical     -> SEARCH_HYBRID_K1
route-010 Nimbus semantic    -> SEARCH_HYBRID_K1

route-011 Orion lexical      -> SEARCH_HYBRID_K1
route-012 Orion semantic     -> SEARCH_HYBRID_K1
```

## Action counts

```text
SEARCH_HYBRID_K1 = 8
SEARCH_HYBRID_K2 = 4
SEARCH_HYBRID_K3 = 0
SEARCH_HYBRID_K5 = 0
```

## Pair stability

Stable:

- Borealis,
- Meridian,
- Nimbus,
- Orion.

Unstable:

- Cirrus: lexical K2, semantic K1,
- Solstice: lexical K1, semantic K2.

Therefore:

```text
stable_pairs=4
unstable_pairs=2
```

## Main finding

Paraphrases do not always preserve the oracle retrieval-budget action.

The same evidence target can require a different minimal k under different wording.

Therefore the Phase 11 v0 assumption:

```text
paraphrase inherits source task action
```

is not generally valid.

## Decision

Future policy examples must be individually oracle-labeled.

Do not copy a source-task action onto new paraphrases unless the oracle has been recomputed for that exact query.
