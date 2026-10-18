# ADR-006: Label Evidence Independently of Chunk IDs

## Status

Accepted

## Context

Changing chunk size or overlap changed chunk IDs and boundaries.

Hard-coded chunk relevance labels became brittle.

## Decision

Store benchmark relevance at source level using:

```text
source_document_id
evidence_text
```

Derive relevant chunk IDs for each chunking configuration.

## Consequences

Benefits:
- stable benchmark questions,
- fair comparison across chunkers,
- automatic detection of fragmented evidence.

Costs:
- exact text matching is limited,
- multi-hop evidence will require richer evidence annotations later.
