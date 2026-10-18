# EXP-010: Rich Chunk-Specific Context

## Compared systems

- parent-title contextual chunks
- rich chunk-specific contextual chunks

## Results

| Strategy | Hit@1 | Hit@3 | MRR |
|---|---:|---:|---:|
| Parent-title context | 0.6667 | 1.0000 | 0.8333 |
| Rich chunk-specific context | 0.6667 | 1.0000 | 0.8333 |

## Per-task behavior

Atlas and Borealis remained rank 1.

Cirrus remained:

1. Retry Policy
2. Dead Letter Handling
3. Queue Overview

The relevant answer-bearing chunk did not move to rank 1.

## Interpretation

More contextual prose did not improve retrieval beyond the simpler parent-title prefix.

Therefore the failure is not explained only by missing document identity or missing section-role context.

The current embedding model may be mapping:
- "exhausting all retries"
- "failed jobs ... retried at most five times"

closer than:
- "exhausting all retries"
- "after all retry attempts fail ... dead-letter queue"

even though the second chunk contains the requested outcome.

## Decision

Do not keep manually adding context until the desired ranking appears.

Instead inspect actual similarity scores for the failure case and determine whether:
- the embedding representation is the limiting factor,
- lexical retrieval behaves differently,
- or reranking is justified.
