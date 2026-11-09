# EXP-069: Challenge-Aware Baselines on Strengthened v1 Corpus

## Research question

How do BM25 and MiniLM behave when stale and contradictory evidence are made retrieval-competitive while all supporting evidence and task questions remain unchanged?

## Controlled comparison

Relative to EXP-066, keep fixed:

- questions,
- task labels,
- supporting documents,
- distractor document,
- top-k = 3,
- BM25,
- MiniLM,
- evaluator.

Change only:

```text
v0 corpus
→ v1 corpus
```

where the stale Borealis and contradictory Cirrus documents have stronger lexical/semantic overlap with the questions.

## Why this experiment matters

EXP-068 showed the adversarial documents moved into the retrieval frontier.

EXP-069 quantifies the consequence through the challenge-aware metrics:

- MeanSupportingRecall@3
- MRR
- MeanEvidenceChainCoverage
- DistractorHitRate
- ContradictionHitRate
- StaleHitRate
- UnanswerableRetrievalRate

## Expected interpretation

A harder benchmark may reduce supporting recall while increasing stale or contradiction hit rates.

That is not a benchmark regression.

It means the candidate set now contains realistic conflict that later systems must resolve.

## Important distinction

Retrieving stale or contradictory evidence is not identical to believing it.

EXP-069 evaluates retrieval exposure only.

Conflict resolution belongs to later retrieval/agent evaluation stages.
