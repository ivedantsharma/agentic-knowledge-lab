# Phase 2 — Structure-Aware Retrieval Experiment

## Research question

Does preserving semantic section boundaries improve retrieval compared with arbitrary fixed-size word chunks?

## Compared systems

### Fixed 18-word chunks

Small enough to create boundary failures.

### Fixed 30-word chunks

Best fixed-size configuration from the previous experiment.

### Section-aware chunks

One retrieval unit per semantic section.

Examples:

- Token Rotation
- Backup Policy
- Dead Letter Handling

## Important difference

The section-aware chunk text includes the section title.

Example:

```text
Token Rotation. Access-token signing keys rotate every 24 hours,
and the current key identifier is ATLAS-KV-104.
```

The heading becomes useful retrieval context.

## Metrics

We report:

- Recall@1
- Recall@3
- Hit@1
- Hit@3
- MRR
- fragmented task list
- total chunk count

## Hypothesis

Structure-aware chunks should improve rank-1 retrieval by keeping:
- local topic context,
- answer-bearing text,
- meaningful boundaries

inside the same retrieval unit.

They should also avoid the redundancy introduced by arbitrary overlap.
