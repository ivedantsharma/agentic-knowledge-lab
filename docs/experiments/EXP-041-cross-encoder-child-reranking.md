# EXP-041: Cross-Encoder Child Reranking

## Research question

Can a cross-encoder correctly rank child sections inside the already-correct parent document where MiniLM fails?

## Controlled variables

Keep fixed:

- structured corpus
- evidence tasks
- parent document retrieval
- original user question
- selected parent document
- candidate child sections.

Change only:

- child scoring model.

## Baseline

MiniLM bi-encoder cosine similarity over sections.

## Treatment

Cross-encoder:

```text
cross-encoder/ms-marco-MiniLM-L6-v2
```

Score only the sections inside the selected parent document.

## Metrics

- DocumentHit@1
- DenseChildHit@1
- CrossEncoderChildHit@1
- per-task candidate scores.

## Hypothesis

The cross-encoder should distinguish:

```text
Retry Policy
```

from:

```text
Dead Letter Handling
```

because it can jointly model the query-section relation rather than relying on independent embeddings.

## Limitation

Three tasks remain a mechanism test only.