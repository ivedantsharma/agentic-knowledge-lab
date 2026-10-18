# Phase 1 — KnowledgeBench v2 Retrieval Stress Tests

KnowledgeBench v1 showed that dense retrieval beat BM25 on one semantic paraphrase task, while both systems tied on lexical tasks.

That means v1 still does not strongly test the hypothesis that BM25 has an advantage on exact lexical retrieval.

v2 is designed to stress the two retrievers in opposite directions.

---

## 1. Lexical stress tests

These use opaque identifiers with little semantic meaning.

Examples:

- INC-847291-B
- ZXQ-19F7-A3
- ERR-KV-4097

Distractor documents contain very similar identifiers.

Expected behavior:

- BM25 should benefit from exact token overlap.
- Dense retrieval may struggle because arbitrary identifiers have weak semantic structure.

---

## 2. Semantic stress tests

These minimize exact word overlap while preserving meaning.

Example:

Document:

```text
Virtual environments isolate dependencies between Python projects.
```

Query:

```text
How can I keep libraries used by one codebase from contaminating another?
```

Expected behavior:

- Dense retrieval should benefit from semantic similarity.
- BM25 may lose signal because important words differ.

---

## 3. Distractor stress tests

Several documents contain related vocabulary.

Only one actually answers the query.

This tests whether:
- lexical overlap creates false positives,
- semantic similarity can distinguish intent,
- ranking remains stable under near-miss documents.

---

## 4. Unanswerable stress tests

No correct document exists.

We keep these because both current retrievers always return top-k results.

This establishes the need for later abstention or evidence-sufficiency mechanisms.

---

## 5. Primary metrics

For v2 we care especially about:

- Recall@1
- MRR
- category-level Recall@1

Recall@3 may still saturate and hide ranking differences.

---

## 6. Interpretation rule

We should build hybrid retrieval only if the experiment demonstrates complementary strengths.

Desired evidence pattern:

```text
BM25 > Dense on lexical stress tasks
Dense > BM25 on semantic stress tasks
```

If that pattern does not appear, we should not assume hybrid retrieval is justified.
