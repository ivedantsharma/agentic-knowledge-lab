# EXP-066: KnowledgeBench v2 BM25 vs Dense Baseline

## Research question

How do lexical BM25 and MiniLM dense retrieval behave on the same KnowledgeBench v2 seed when the benchmark distinguishes supporting, stale, contradictory, distracting, and unanswerable evidence?

## Controlled comparison

Keep fixed:

- corpus,
- questions,
- top-k = 3,
- task annotations,
- evaluation code.

Change only:

```text
retriever
```

Compare:

```text
BM25
vs
sentence-transformers/all-MiniLM-L6-v2
```

## Why this is different from Phase 1

Phase 1 primarily measured:

- Recall@K,
- Precision@K,
- MRR,
- unanswerable retrieval.

Phase 7 asks a harder question:

> What kind of evidence did the retriever return?

## Metrics

### MeanSupportingRecall@3

Fraction of supporting documents retrieved.

For multi-hop tasks, retrieving only one required document is partial success.

### MRR

Rank of the first supporting document.

MRR can be high even when the rest of the evidence chain is missing.

This is why it must not be interpreted alone.

### MeanEvidenceChainCoverage

For tasks with an ordered evidence chain:

```text
retrieved chain documents
/
required chain documents
```

This measures availability of the evidence chain, not reasoning over its order.

### DistractorHitRate

Among tasks annotated with distractors, how often at least one distractor enters top-k.

### ContradictionHitRate

Among tasks containing contradictory evidence, how often a contradictory document enters top-k.

This metric is diagnostic, not automatically bad: a robust downstream system may need to retrieve contradictions in order to resolve them.

### StaleHitRate

Among tasks with stale documents, how often stale evidence enters top-k.

### UnanswerableRetrievalRate

Fraction of unanswerable tasks where the retriever still returns documents.

A fixed top-k retriever is expected to score poorly here because it has no abstention policy.

This metric deliberately exposes that limitation.

## Interpretation discipline

A high MRR with low chain coverage means:

```text
first useful document found
!=
all required evidence found
```

Likewise, retrieving a contradiction does not prove the retriever failed.

Later evaluators must distinguish:

```text
retrieved contradiction
vs
believed contradiction
```

EXP-066 measures retrieval only.
