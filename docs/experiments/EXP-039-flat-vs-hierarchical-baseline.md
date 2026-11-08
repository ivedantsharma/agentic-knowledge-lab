# EXP-039: Flat vs Hierarchical Retrieval Baseline

## Research question

Does simple document-first retrieval preserve or improve evidence retrieval compared with global flat section retrieval?

## Corpus

Reuse the Phase 2 structured manuals:

- Atlas Service Manual
- Borealis Storage Manual
- Cirrus Worker Manual

Each contains four semantic sections.

## Tasks

Reuse the Phase 2 evidence tasks:

- Atlas signing-key identifier
- Borealis incremental-backup cadence
- Cirrus dead-letter queue

## Flat baseline

query → rank all 12 sections globally → choose top section

## Hierarchical baseline

query → rank 3 documents → choose top document → rank its 4 sections → choose top section

## Controlled variables

Same:

- questions
- corpus
- MiniLM embedding model
- section rendering
- cosine similarity

Changed:

- search topology only

## Metrics

- DocumentHit@1
- FlatSectionHit@1
- HierarchicalSectionHit@1
- FlatCandidateCountPerQuery
- HierarchicalChildCandidatesPerQuery

## Limitation

Three manuals and three questions are enough to validate the mechanism, not to establish superiority. A harder distractor experiment follows this baseline.