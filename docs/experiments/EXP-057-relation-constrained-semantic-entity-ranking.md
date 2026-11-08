# EXP-057: Relation-Constrained Semantic Entity Ranking

## Research question

Can graph structure repair semantic start-node ambiguity when the first relation is known?

## Controlled change

EXP-056 ranks every entity semantically.

EXP-057 filters entities first:

```text
candidate entity must have
an outgoing edge matching
the first gold relation
```

Then semantic similarity ranks only the structurally valid candidates.

Everything else remains fixed:

- same graph,
- same MiniLM model,
- same entity profiles,
- same positive semantic questions.

## Examples

For the implicit Borealis question:

```text
first relation = incremental_backup_cadence
```

Borealis is a valid subject.

For the Platform Reliability paraphrase:

```text
first relation = maintains_storage_system
```

Platform Reliability is a valid subject while Borealis is not.

## Metrics

- UnconstrainedGoldRank
- ConstrainedGoldRank
- ConstrainedHit@1
- CandidateReduction

## Hypothesis

Both semantic positive cases should rank the correct start entity first after structural filtering.

## Limitation

The first relation is still gold/oracle-provided.

This experiment does not test relation prediction.
