# EXP-068: Strengthen Stale and Contradictory Evidence

## Research question

Can we make stale and contradictory evidence genuinely competitive retrieval candidates without changing the supporting evidence, questions, or retrievers?

## Motivation

EXP-067 found:

```text
BM25 stale rank          = 6
Dense stale rank         = 4

BM25 contradiction rank  = 8
Dense contradiction rank = 9
```

The Aurora distractor was already competitive:

```text
BM25 rank = 3
Dense rank = 1
```

Therefore only the stale and contradiction examples are strengthened.

## Controlled change

Keep fixed:

- task questions,
- task labels,
- supporting documents,
- distractor document,
- document IDs,
- BM25,
- MiniLM,
- ranking code.

Change only the wording/status framing of:

- the stale Borealis policy,
- the contradictory Cirrus policy.

## Versioning

The original corpus remains:

```text
knowledgebench_v2_seed_documents_v0.json
```

The strengthened corpus is:

```text
knowledgebench_v2_seed_documents_v1.json
```

This preserves EXP-066 and EXP-067 reproducibility.

## Desired behavior

The adversarial documents should move closer to the retrieval frontier without becoming mislabeled supporting evidence.

A useful stress benchmark should create competition between:

```text
current vs stale
active vs pending
supporting vs plausible distractor
```

## What success would prove

Only that the benchmark is harder at the retrieval stage.

It would not prove that a downstream system can correctly resolve temporal or policy-status conflicts.
