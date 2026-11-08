# EXP-047 Result: Per-Section Chunk Rank Diagnostic

## Key result

Atlas:

```text
relevant_local_rank=1
relevant_global_rank=1
```

Borealis:

```text
relevant_local_rank=2
relevant_global_rank=2
```

Cirrus:

```text
relevant_local_rank=2
relevant_global_rank=4
```

## Interpretation

The Cirrus evidence-bearing chunk is not deeply weak inside its correct section.

Inside:

```text
manual_gamma::Dead Letter Handling
```

the ranking is:

```text
1. "A job that fails all retry attempts is moved to"
2. "is moved to the dead-letter queue named CIRRUS-DLQ."
```

The relevant chunk falls to global rank 4 only after chunks from the hard distractor section are pooled.

Therefore the main Cirrus failure is candidate concentration across sections, not a complete chunk-scorer failure.

## Additional pattern

For both Borealis and Cirrus, the highest-scoring chunk in the correct section is adjacent to the answer-bearing chunk.

This motivates a section-aware neighbor-expansion experiment rather than another model change.
