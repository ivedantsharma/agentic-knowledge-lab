# Phase 5 — Fragmentation vs Candidate Concentration

## Two different chunk-level failures

### Fragmentation

The evidence does not exist completely inside any chunk.

Example:

```text
chunk A: ... backups run every
chunk B: six hours.
```

No ranker can retrieve an exact evidence span that no candidate contains.

Overlap addresses this by duplicating boundary context.

### Candidate concentration

The relevant chunk exists, but several chunks from another section occupy the highest ranks.

EXP-046 Cirrus:

```text
rank 1: distractor section chunk
rank 2: distractor section chunk
...
rank 4: relevant chunk
```

This is fundamentally different from fragmentation.

## Why hierarchy creates an opportunity

Chunks have parents.

A flat global top-k ignores this ancestry:

```text
top 2 chunks
→ both may come from the same section
```

A hierarchy-aware policy can preserve diversity across retained sections.

Before implementing such a policy, measure where the relevant chunk ranks within its own section.