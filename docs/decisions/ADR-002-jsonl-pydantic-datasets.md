# ADR-002: Use JSONL plus Pydantic for Benchmark Data

## Status

Accepted

## Context

Benchmark tasks and corpus documents need versioned, inspectable storage and runtime validation.

## Decision

Store datasets as JSONL and validate each line into typed Pydantic models.

## Consequences

Benefits:
- readable Git diffs,
- streaming-friendly format,
- line-specific validation errors,
- typed runtime contracts,
- easy synthetic dataset authoring.

Costs:
- JSONL is not a rich relational format,
- cross-file referential integrity must be checked separately.

This is appropriate for the current research scale.
