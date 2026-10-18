# ADR-005: Preserve Native Document Structure During Ingestion

## Status

Accepted

## Context

Phase 2 experiments showed that arbitrary word boundaries can:
- fragment evidence,
- remove parent context,
- create redundant overlapping chunks.

Markdown and similar formats already contain semantic structure through headings.

## Decision

When source formats expose reliable structure, preserve it during ingestion.

For Markdown:
- level-1 heading becomes document title,
- level-2/3 headings become sections,
- section bodies become structured text.

Fixed-size chunking remains available as a fallback and experimental baseline.

## Consequences

Benefits:
- better provenance,
- more interpretable chunks,
- fewer arbitrary boundaries,
- easier structure-aware retrieval.

Costs:
- parser logic becomes format-specific,
- malformed documents may expose poor structure,
- some sections may still require subdivision.
