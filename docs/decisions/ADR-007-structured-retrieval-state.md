# ADR-007: Carry Structured Retrieval State Between Hops

## Status

Accepted

## Context

The initial multi-hop executor carried only:

```text
previous_fact: str
```

This caused an information-loss failure.

The system extracted:

```text
Borealis
```

but discarded the qualifier:

```text
production
```

As a result, the next query became ambiguous between production and staging Borealis manuals.

## Decision

Carry structured retrieval state between hops.

Current state:

```text
RetrievalState
├── entity
├── qualifiers
├── source_document_id
└── evidence_text
```

## Consequences

Benefits:

- preserves retrieval-relevant qualifiers,
- retains provenance,
- reduces lossy compression between hops,
- creates a natural foundation for future agent state.

Costs:

- state design becomes part of retrieval architecture,
- extraction errors can still corrupt state,
- more fields may be required for temporal, relational, or multi-entity questions.

## Future extension

Later phases may add:

- relation,
- time constraints,
- unresolved subquestions,
- visited documents,
- search history,
- confidence,
- candidate evidence.

Those additions should be driven by observed failures rather than added speculatively.
