# Phase 2 — Evidence-Based Chunk Relevance

## Problem

A benchmark task should describe the information needed to answer a question.

It should not depend on one particular chunking algorithm.

This is brittle:

```text
relevant_document_ids = ["manual_gamma::chunk-0003"]
```

because changing chunk size or overlap changes the chunk layout.

## Better representation

Store source-level evidence:

```text
source_document_id
evidence_text
```

Example:

```text
question:
Where are Cirrus jobs sent after exhausting retries?

source_document_id:
manual_gamma

evidence_text:
CIRRUS-DLQ
```

Then, for each chunking configuration:

1. generate chunks,
2. keep chunks from the required source document,
3. find chunks containing the evidence text,
4. use those chunk IDs as relevant IDs.

## Why this matters

The benchmark question remains stable while chunking changes.

That lets us fairly compare:

- 12-word chunks,
- 18-word chunks,
- 30-word chunks,
- overlap,
- structure-aware chunks,
- contextualized chunks.

## Limitation

Exact evidence-text matching is only a Phase 2 baseline.

Later tasks may require:
- evidence spans,
- multiple evidence pieces,
- multi-hop evidence,
- semantic evidence equivalence.

But it is much safer than manually hard-coding chunk IDs.
