# ADR-011: Provenance-Aware Claim Graph with Constrained Semantic Path Search

## Status

Accepted for Phase 6 reference architecture.

## Context

Relationship-heavy knowledge questions require more than flat text similarity.

A useful architecture must preserve:

- canonical entities,
- typed relations,
- claim provenance,
- structurally valid traversal,
- explicit failure modes.

Phase 6 compared deterministic traversal, lexical entity linking, semantic entity linking, type constraints, path enumeration, semantic path ranking, and end-to-end integration.

## Decision

Adopt a provenance-aware claim graph with:

```text
GraphEntity
KnowledgeClaim
EvidenceReference
```

and answer questions through:

```text
entity resolution
→ bounded graph-path enumeration
→ semantic path ranking
→ answer + provenance
```

Use lexical entity linking first.

Allow semantic entity fallback only as a guarded secondary mechanism.

Preserve explicit abstention instead of forcing a nearest-neighbor entity link.

## Why path enumeration instead of free-form relation generation?

For the Phase 6 scale, bounded enumeration offers:

- deterministic structural validity,
- easy debugging,
- exact provenance,
- controlled candidate spaces,
- clear failure attribution.

A generated path can invent invalid relation sequences.

Enumerated candidates cannot violate graph connectivity.

## Why not use NetworkX?

The graph mechanics required in Phase 6 are simple:

- outgoing adjacency,
- bounded traversal,
- cycle avoidance,
- literal termination.

A custom small implementation keeps the mechanics visible and avoids adding a dependency that would hide the research variable.

## Why preserve evidence on every claim?

A graph edge without provenance is only an assertion.

The accepted representation makes claim provenance first-class.

This enables later evaluation of:

- groundedness,
- source quality,
- contradiction,
- staleness,
- evidence coverage.

## Entity-resolution policy

Preferred ordering:

```text
exact name / alias
→ typed semantic fallback
→ confidence gate
→ abstain
```

However, EXP-064 shows that the semantic fallback and fixed threshold are not yet reliable enough for strong end-to-end guarantees.

Therefore the semantic fallback remains an experimental component rather than a production-quality resolver.

## Consequences

### Positive

- graph paths are structurally valid,
- answers carry claim-level provenance,
- path-selection failures are inspectable,
- entity and path errors can be evaluated separately,
- reusable graph QA component exists.

### Negative

- bounded path enumeration does not scale indefinitely,
- entity confidence is brittle,
- implicit entity linking remains incomplete,
- ambiguous same-relation claims need qualifier-aware resolution,
- fixed thresholds are benchmark-sensitive.

## Future evolution

Later phases may replace or extend components with:

- learned entity linking,
- calibrated confidence,
- qualifier-aware claim selection,
- relation planning,
- hybrid text/graph routing,
- larger graph indexes,
- temporal and contradictory claims.
