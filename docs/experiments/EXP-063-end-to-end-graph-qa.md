# EXP-063: End-to-End Explicit-Entity Claim-Graph QA

## Research question

Can the Phase 6 components work together from a natural-language question to a provenance-bearing answer without being given the start entity or relation path?

## Pipeline

```text
question
→ lexical entity resolution
→ graph path enumeration
→ semantic path ranking
→ selected claim path
→ answer + provenance
```

## Controlled assumptions

No longer oracle:

- start entity,
- relation path.

Still constrained:

- the start entity must appear explicitly by registered name or alias,
- path search is bounded to three hops,
- the graph is small and synthetic.

## Why use the original four questions?

The individual components were validated separately.

EXP-063 is an integration experiment, so we deliberately avoid simultaneously introducing semantic entity fallback, automatic mention extraction, or a new threshold policy.

That keeps failures attributable.

## Metrics

- EntityResolutionAccuracy
- PathSelectionAccuracy
- AnswerAccuracy
- ProvenanceCoverage
- EndToEndSuccessRate
- AvgPathScoreMargin

A task counts as end-to-end success only if entity, path, answer, and provenance are all correct.

## Margin diagnostic

EXP-062 showed a close path-ranking case for Atlas:

```text
correct Borealis path: 0.782214
legacy Aurora path:    0.755725
margin:                0.026489
```

Therefore EXP-063 records top-1/top-2 path margin rather than reporting accuracy alone.

## What success would prove

The independently tested Phase 6 components can be composed into a reusable natural-language-to-claim-graph QA baseline.

## What success would not prove

It would not establish robust handling of:

- implicit entity mentions,
- ambiguous aliases,
- large graphs,
- unseen relation schemas,
- qualifier-heavy claims,
- calibrated confidence,
- autonomous generative graph planning.
