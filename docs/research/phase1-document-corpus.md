# Phase 1 — Document Corpus Schema and Loader

Our benchmark tasks now live on disk.

But those tasks reference document IDs such as:

```text
doc_python
doc_http
doc_rl
```

Those IDs need to point to real corpus documents.

We therefore create a typed document schema and a versioned corpus file.

---

## 1. Document schema

A first document needs:

- document_id
- text
- metadata

Example:

```python
KnowledgeDocument(
    document_id="doc_python",
    text="Python virtual environments isolate project dependencies...",
    metadata={"source": "synthetic"},
)
```

---

## 2. Why document IDs matter

Benchmark tasks refer to relevant evidence by ID.

Example:

```text
Task kb-001
relevant_document_ids = {"doc_python"}
```

The corpus must therefore contain:

```text
document_id = "doc_python"
```

If the benchmark references a missing document, evaluation is invalid.

---

## 3. Corpus format

We will also use JSONL.

One document per line:

```text
{"document_id":"doc_python","text":"...","metadata":{"source":"synthetic"}}
{"document_id":"doc_http","text":"...","metadata":{"source":"synthetic"}}
```

---

## 4. Loader responsibilities

The document loader should:

1. read JSONL,
2. ignore blank lines,
3. parse JSON,
4. validate each document,
5. reject blank IDs,
6. reject blank document text,
7. reject duplicate document IDs.

---

## 5. Corpus validation

Eventually we should validate the relationship between:

```text
KnowledgeTask.relevant_document_ids
```

and:

```text
KnowledgeDocument.document_id
```

If a task references a missing document, the benchmark definition is broken.

---

## 6. End-to-end goal

Once tasks and documents both live on disk:

```text
tasks.jsonl
+
documents.jsonl
↓
load + validate
↓
dense retriever
↓
RunResult[]
↓
benchmark evaluator
↓
Recall@K / Precision@K / MRR
```

This will be our first complete KnowledgeBench pipeline.
