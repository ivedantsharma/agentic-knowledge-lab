# EXP-009: Deterministic Parent Context

## Compared systems

- plain section chunks
- contextualized section chunks with document title + section title

## Results

| Strategy | Hit@1 | Hit@3 | MRR |
|---|---:|---:|---:|
| Plain sections | 0.6667 | 1.0000 | 0.7778 |
| Parent-context sections | 0.6667 | 1.0000 | 0.8333 |

## Per-task behavior

### Atlas
Relevant section remained rank 1.

### Borealis
Relevant section remained rank 1.

### Cirrus

Plain sections:
1. Queue Overview
2. Retry Policy
3. Dead Letter Handling

Contextualized sections:
1. Retry Policy
2. Dead Letter Handling
3. Queue Overview

The relevant section improved from rank 3 to rank 2.

## Interpretation

Adding parent document identity helped retrieval but was insufficient to make the answer-bearing Cirrus section rank first.

The query strongly mentions retry exhaustion.

The Retry Policy section contains:
- failed jobs
- exponential backoff
- retried
- five times

The Dead Letter Handling section contains the final outcome but still has less direct wording overlap with the query.

## Next hypothesis

A richer chunk-specific context sentence can describe the role of each section within the document without including the answer itself.

Example:

```text
This section of the Cirrus Worker Manual describes what happens to jobs after all retry attempts fail.
```

This is closer to contextual retrieval than a title-only prefix because it explains why the chunk exists in the document.
