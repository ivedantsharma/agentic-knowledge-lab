# EXP-008: Structure-Aware Chunking

## Compared systems

- fixed 18-word chunks
- fixed 30-word chunks
- structure-aware section chunks

## Results

| Strategy | Chunks | Hit@1 | Hit@3 | MRR |
|---|---:|---:|---:|---:|
| 18 words | 11 | 0.3333 | 1.0000 | 0.6111 |
| 30 words | 6 | 0.6667 | 1.0000 | 0.8333 |
| sections | 12 | 0.6667 | 1.0000 | 0.7778 |

## Interpretation

Structure-aware chunks improved substantially over 18-word chunks.

They did not outperform the 30-word fixed-size baseline overall.

Atlas and Borealis were ranked correctly at position 1.

Cirrus remained a failure:
- relevant Dead Letter Handling section ranked third,
- Queue Overview ranked first,
- Retry Policy ranked second.

## Failure analysis

The query refers to:
- Cirrus,
- jobs,
- exhausted retries.

The relevant section contains:
- failed job,
- retry attempts,
- CIRRUS-DLQ.

But it does not contain the parent document identity "Cirrus Worker Manual".

This suggests a lost-parent-context failure.

## Next hypothesis

Prepending concise parent document/section context before embedding may make the relevant section easier to retrieve.
