# EXP-107: Existing-Corpus Oracle Policy Label Mining

## Research question

Can the existing Phase 10 paired-query benchmark provide additional independent retrieval-policy labels for Phase 11?

A second question is equally important:

> Do paraphrases of the same underlying information need preserve the same oracle retrieval budget?

## Why this matters

Phase 11 dataset v0 assumes paraphrases inherit the source task's policy label.

That assumption has not been validated.

Phase 10 already showed that wording can change retrieval rankings.

Therefore we must recompute the oracle policy action for each query variant rather than blindly copying labels.

## Data source

Use the six Phase 10 query pairs:

- Borealis backup,
- Cirrus retry,
- Solstice cache,
- Meridian rotation,
- Nimbus session,
- Orion logs.

Each pair contains:

```text
lexical_explicit
semantic_paraphrase
```

with the same supporting evidence target.

## Oracle labeling rule

Use Hybrid RRF over the existing 22-document hard corpus.

For:

```text
k in {1, 2, 3, 5}
```

compute supporting-document recall.

Assign the smallest k that reaches the maximum observed recall:

```text
1 → SEARCH_HYBRID_K1
2 → SEARCH_HYBRID_K2
3 → SEARCH_HYBRID_K3
5 → SEARCH_HYBRID_K5
```

## Metrics

Per query:

- oracle action,
- minimal k,
- Recall@1/2/3/5.

Per source pair:

- whether both wording variants receive the same action.

Aggregate:

- action counts,
- stable pair count,
- unstable pair count.

## Interpretation

### Stable pair

Supports the assumption that this source's policy label is robust to the tested wording change.

### Unstable pair

Shows that policy is query-specific rather than source-task-specific.

In that case, paraphrases must be individually oracle-labeled; they cannot automatically inherit one source label.

## Limitation

This experiment mines only budget actions.

It cannot generate new REFORMULATE examples because that label additionally requires demonstrated retrieval saturation plus improvement from query transformation.
