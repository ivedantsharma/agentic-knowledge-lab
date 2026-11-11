# EXP-096: Paired Lexical vs Semantic Routing Benchmark

## Research question

Does changing only the wording style of a query alter which retriever performs best?

## Trigger from EXP-095

Neither shallow query features nor retrieval-confidence signals cleanly separated retriever winners on the six answerable hard-v0 tasks.

The benchmark is too small to justify a routing policy.

## New benchmark design

Create six query pairs over the same existing KnowledgeBench v2 corpus.

For each underlying fact:

```text
same supporting document
same answer semantics
different query wording
```

Two query styles:

### lexical_explicit

Uses document/service terminology close to the corpus.

### semantic_paraphrase

Expresses the same information need with more indirect wording.

## Pairs

- Borealis backup cadence,
- Cirrus retry limit,
- Solstice cache duration,
- Meridian key rotation,
- Nimbus session cache,
- Orion log retention.

Total:

```text
6 pairs
12 tasks
```

## Candidate retrievers

- BM25,
- Dense MiniLM,
- equal-weight RRF hybrid.

All receive:

```text
top_k=3
```

## Metrics

Per task:

- Recall@3,
- Reciprocal Rank,
- winner set.

Aggregate by query style:

- mean Recall@3,
- MRR.

Pair diagnostic:

- whether the winner set changes between lexical and semantic wording.

## Why pairing matters

If query wording changes the best retriever while evidence stays fixed, that is direct evidence that query understanding can support routing.

If winner sets remain mostly unchanged, the current retrievers or corpus may not provide enough strategy diversity.

## Important limitation

These are synthetic paired queries authored for mechanism isolation.

They are not a natural-language production distribution and must not be treated as one.
