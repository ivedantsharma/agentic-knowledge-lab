# EXP-072: Candidate-Budget Sensitivity on KnowledgeBench v2 Hard v0

## Research question

How do support coverage and adversarial exposure change as the retrieval candidate budget grows?

## Controlled variable

Keep fixed:

- hard benchmark v0,
- task labels,
- BM25 scoring,
- MiniLM scoring,
- document corpus,
- questions.

Change only:

```text
top_k ∈ {1, 3, 5}
```

## Why this matters

A retrieval system can appear safer simply because it returns fewer candidates.

Likewise, a larger candidate set may improve multi-hop evidence coverage while also exposing:

- stale documents,
- contradictions,
- distractors.

This creates a retrieval frontier rather than one universally best k.

## Metrics

For every k:

- supporting recall,
- MRR,
- evidence-chain coverage,
- distractor hit rate,
- contradiction hit rate,
- stale hit rate,
- ambiguity candidate coverage,
- unanswerable retrieval rate.

The same metrics are also reported by challenge slice.

## Expected tradeoff

Typical pattern:

```text
larger k
→ higher supporting recall
→ higher chain coverage
→ potentially higher adversarial exposure
```

The benchmark should make this tradeoff visible.

## Important limitation

This experiment measures candidate-set composition only.

It does not model context-window cost, reranking cost, or downstream answer quality.
