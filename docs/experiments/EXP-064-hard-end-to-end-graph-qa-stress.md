# EXP-064: Hard End-to-End Hybrid Claim-Graph QA Stress

## Research question

Can the Phase 6 graph QA system handle a mixture of explicit entity mentions, implicit entity descriptions, branching paths, and unrelated questions using a fixed hybrid entity policy?

## Pipeline

```text
question
→ lexical entity match if possible
→ otherwise infer coarse type from question
→ semantic entity ranking within type
→ fixed score threshold 0.39
→ graph path enumeration
→ semantic path ranking
→ answer + provenance
```

## Important constraints

No gold start entity is supplied to the system.

No gold relation path is supplied.

No gold mention span is supplied.

The type inference heuristic and semantic threshold are reused from earlier experiments rather than tuned on EXP-064.

## Stress categories

- explicit entity + branching path,
- implicit service,
- implicit team + branching path,
- unrelated team query requiring abstention,
- unrelated service query requiring abstention.

## Metrics

- AnswerableEndToEndSuccessRate
- EntityResolutionAccuracy
- PathSelectionAccuracy
- AnswerAccuracy
- ProvenanceCoverage
- AbstentionAccuracy
- FalsePositiveAnswerRate

## Interpretation discipline

A failure can occur at different layers:

```text
entity resolution
→ path ranking
→ answer selection
→ abstention
```

The runner prints component-level outcomes so a final score does not hide the cause.

## Scope

This is still a small synthetic mechanism benchmark.

It is not evidence of production-scale graph QA generalization.
