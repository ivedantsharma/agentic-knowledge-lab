# Phase 1 — KnowledgeBench Dataset Format and Loader

Until now, benchmark tasks have lived inside Python code.

That is useful for unit tests, but a real benchmark should store tasks as data.

We will use JSONL.

---

## 1. What is JSONL?

JSONL means JSON Lines.

Instead of one giant JSON array:

```json
[
  {"task_id": "kb-001", "question": "..."},
  {"task_id": "kb-002", "question": "..."}
]
```

JSONL stores one JSON object per line:

```text
{"task_id":"kb-001","question":"..."}
{"task_id":"kb-002","question":"..."}
```

---

## 2. Why JSONL?

JSONL is useful for benchmark datasets because:

- each task is independent,
- files can be streamed line by line,
- append/edit operations are simple,
- Git diffs are readable,
- malformed lines can be identified precisely,
- large datasets do not require loading one giant JSON structure first.

---

## 3. Dataset flow

```text
data file
↓
JSON parser
↓
Pydantic KnowledgeTask validation
↓
list[KnowledgeTask]
↓
runner/evaluator
```

This means the loader does not redefine validation.

It reuses our existing schema.

---

## 4. First dataset fields

Each line should match KnowledgeTask:

- task_id
- question
- relevant_document_ids
- category
- expected_answer
- metadata

Example:

```json
{"task_id":"kb-001","question":"How do Python virtual environments help?","relevant_document_ids":["doc_python"],"category":"semantic_paraphrase","expected_answer":"They isolate project dependencies.","metadata":{"difficulty":"easy"}}
```

Pydantic will convert the JSON list of document IDs into the schema's set[str].

---

## 5. Loader responsibilities

The loader should:

1. open the file,
2. read line by line,
3. ignore blank lines,
4. parse JSON,
5. validate using KnowledgeTask,
6. reject duplicate task IDs,
7. report the line number when something is invalid.

---

## 6. Why duplicate task IDs are dangerous

The evaluator joins tasks and results using task_id.

If two benchmark tasks share the same ID, results become ambiguous.

So task IDs must be unique within a dataset.

---

## 7. Why validation belongs at load time

Bad benchmark data should fail immediately.

We do not want:

```text
bad dataset
↓
30 minute experiment
↓
strange metrics
↓
discover malformed task
```

We want:

```text
bad dataset
↓
loader
↓
clear error immediately
```

---

## 8. Starter dataset

We will create a tiny Phase 1 dataset with tasks covering:

- semantic paraphrase,
- exact identifier,
- direct retrieval,
- unanswerable.

This is not yet our real benchmark.

It exists to validate the data architecture.
