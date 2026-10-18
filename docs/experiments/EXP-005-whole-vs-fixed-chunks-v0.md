# EXP-005: Whole-Document vs Fixed-Chunk Dense Retrieval v0

## Status

Diagnostic result with one discovered annotation error.

## Whole-document result

- Recall@1: 1.0000
- Recall@3: 1.0000
- MRR: 1.0000

All three source documents were ranked first for their respective questions.

## Fixed 18-word chunk result as originally labeled

- Recall@1: 0.3333
- Recall@3: 1.0000
- MRR: 0.6667

## Important benchmark issue

The task:

```text
p2-chunk-003
Where are Cirrus jobs sent after exhausting all retries?
```

was labeled relevant to:

```text
manual_gamma::chunk-0001
```

But the generated chunks show that the answer text:

```text
attempts is moved to the dead-letter queue named CIRRUS-DLQ
```

is in:

```text
manual_gamma::chunk-0002
```

Therefore the original v0 chunk-level aggregate metrics are not valid enough for comparison.

The v0 files are preserved for reproducibility.

A corrected v1 task file should be used for subsequent experiments.

## Genuine boundary finding

For the Atlas task:

```text
What is the current Atlas signing-key identifier?
```

the relevant information is split across a chunk boundary.

Chunk 0 ends with:

```text
Token Rotation. Access-token signing
```

Chunk 1 begins with:

```text
keys rotate every 24 hours, and the current key identifier is ATLAS-KV-104
```

Dense retrieval ranked chunk 0 first and the answer-bearing chunk 1 second.

This is a real example of chunk-boundary context loss.

## Decision

Preserve v0.

Create corrected v1 labels and test whether overlap repairs the boundary failure.
