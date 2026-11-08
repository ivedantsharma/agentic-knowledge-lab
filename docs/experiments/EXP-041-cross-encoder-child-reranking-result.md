# EXP-041 Result: Cross-Encoder Child Reranking

## Aggregate result

```text
DocumentHit@1=1.0000
DenseChildHit@1=0.6667
CrossEncoderChildHit@1=1.0000
```

## Atlas

Both dense and cross-encoder retrieval rank Token Rotation first.

Cross-encoder ranking:

```text
Token Rotation            8.140610
Authentication Overview   0.405419
Cache Behavior           -8.088100
Deployment Notes         -9.804974
```

## Borealis

Both dense and cross-encoder retrieval rank Backup Policy first.

Cross-encoder ranking:

```text
Backup Policy      9.152600
Restore Process    1.711374
Encryption        -1.733370
Storage Overview  -5.020986
```

## Cirrus

Dense child retrieval fails:

```text
Retry Policy
score=0.620166
```

Cross-encoder reranking succeeds:

```text
Dead Letter Handling  1.141416
Retry Policy         -1.107666
Queue Overview       -2.359130
Observability        -4.122324
```

## Interpretation

The cross-encoder resolves the exact within-document ambiguity that the dense bi-encoder could not.

This validates a coarse-to-fine pattern:

```text
cheap document routing
→ small child candidate set
→ expensive pairwise reranking
```

## Why the result matters

The improvement is not caused by changing the parent retriever, query, or corpus.

The only meaningful change is the child scorer.

Therefore the Cirrus repair is attributable to stronger pairwise relevance modeling.

## Limitation

The corpus contains only three documents and twelve sections.

This validates the mechanism, not robustness.

The next experiment should stress the hierarchy itself by making parent routing ambiguous.