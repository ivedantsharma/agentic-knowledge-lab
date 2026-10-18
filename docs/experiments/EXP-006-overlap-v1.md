# EXP-006: Chunk Overlap — 18 Words, 0 vs 6

## Results

| Metric | 0 overlap | 6-word overlap |
|---|---:|---:|
| Chunks indexed | 11 | 14 |
| Recall@1 | 0.3333 | 0.6667 |
| Recall@3 | 1.0000 | 0.6667 |
| MRR | 0.6111 | 0.6667 |

## Per-task behavior

### Atlas

Overlap fixed the rank-1 boundary failure.

Without overlap:

1. context-heavy chunk
2. answer-bearing chunk

With 6-word overlap:

1. answer-bearing chunk

The overlapping chunk now contains both token-rotation context and the key identifier.

### Borealis

The relevant chunk remained rank 1 in both configurations.

### Cirrus

Overlap increased the number of chunks and created several highly related retry/dead-letter chunks.

The answer-bearing chunk containing `CIRRUS-DLQ` fell outside top 3.

This is an example of overlap increasing redundancy and competition among near-duplicate chunks.

## Conclusion

Overlap is a tradeoff.

It can repair boundary context loss, but it can also:
- create more chunks,
- increase redundancy,
- crowd top-k with neighboring chunks.

Therefore "more overlap is better" is not supported.

## Benchmark design issue

Hard-coded relevant chunk IDs are brittle because changing stride changes chunk boundaries and IDs.

Next decision:

Represent relevance using source-level evidence text and derive relevant chunk IDs automatically for each chunking configuration.
