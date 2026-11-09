# EXP-063: End-to-End Natural-Language Graph QA

## Research question

Can the Phase 6 components work together from a natural-language question to a provenance-backed answer without gold start-entity IDs or gold relation paths?

## Pipeline

```text
question
→ lexical entity resolution
→ graph path enumeration
→ semantic path ranking
→ deterministic traversal
→ answer + evidence
```

## Removed oracle assumptions

EXP-053 supplied:

- gold start entity,
- gold relation path.

EXP-063 supplies neither.

The current tasks explicitly name their start entities, so deterministic lexical linking is used rather than semantic fallback.

## Fixed components

- branching Phase 6 graph,
- MiniLM path ranker,
- maximum path length = 3,
- deterministic traversal semantics,
- existing Phase 6 task set.

## Metrics

- EntityLinkAccuracy
- PathSelectionAccuracy
- AnswerAccuracy
- ProvenanceCoverage

## What success would establish

The independently tested Phase 6 components compose correctly into a single natural-language graph-QA pipeline on the current synthetic benchmark.

## What success would not establish

It would not solve:

- implicit start-entity mention extraction,
- large-graph path search,
- ambiguous duplicate claims,
- qualifier-aware selection such as production vs staging,
- independent generalization beyond the development corpus.

Those limitations remain explicit.
