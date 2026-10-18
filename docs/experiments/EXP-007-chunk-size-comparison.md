# EXP-007: Chunk Size Comparison

## Configurations

- 12 words, 0 overlap
- 18 words, 0 overlap
- 18 words, 6 overlap
- 30 words, 0 overlap

## Observed results

### 12 words, 0 overlap

- 15 chunks
- Borealis evidence fragmented
- Recall@1: 0.0000
- Recall@3: 0.5000
- MRR: 0.2500

This configuration is too fine-grained for the current corpus.

### 18 words, 0 overlap

- 11 chunks
- no fragmented evidence tasks
- Recall@1: 0.3333
- Recall@3: 1.0000
- MRR: 0.6111

### 18 words, 6 overlap

- 14 chunks
- no fragmented evidence tasks
- ordinary Recall@1: 0.5000
- Recall@3: 0.6667
- MRR: 0.6667

Important metric caveat:

Overlap duplicated Atlas evidence across two chunks.

Ordinary Recall@1 therefore reports 0.5 even though one valid answer-bearing chunk was ranked first.

Hit@K should be added for this setting.

### 30 words, 0 overlap

- 6 chunks
- no fragmented evidence tasks
- Recall@1: 0.6667
- Recall@3: 1.0000
- MRR: 0.8333

This is the strongest fixed-size setting tested so far.

## Findings

1. Very small chunks can split evidence completely.
2. Moderate overlap can repair boundary context but increases redundancy.
3. Larger chunks preserve more context and performed better here.
4. Larger chunks still do not guarantee rank-1 evidence retrieval.
5. Metrics must account for duplicated evidence created by overlap.

## Next hypothesis

The source manuals already contain semantic section boundaries.

A structure-aware chunker that keeps sections such as:

- Token Rotation
- Backup Policy
- Dead Letter Handling

together may preserve more useful context than arbitrary word-count boundaries while avoiding excessive overlap.
