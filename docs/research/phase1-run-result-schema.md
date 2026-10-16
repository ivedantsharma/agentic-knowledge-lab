# Phase 1 — RunResult Schema

`KnowledgeTask` stores ground truth.

`RunResult` stores what the system actually produced.

Keeping them separate avoids mixing the answer key with the model/retriever output.

## Fields

```text
task_id
generated_answer
retrieved_document_ids
tool_calls
latency_ms
metadata
```

## Validation rules

### task_id
Must not be blank.

### tool_calls
Must be zero or greater.

Negative tool calls are impossible and indicate corrupted data.

### latency_ms
May be omitted when latency was not measured.

If present, it must be zero or greater.

### generated_answer
May be `None`.

This is useful when:
- the system failed,
- the task is unanswerable,
- answer generation was intentionally skipped.

### retrieved_document_ids
May be empty.

An empty list is a valid system outcome and should be evaluated as such.

## Architecture

```text
KnowledgeTask
    ↓ question
System
    ↓
RunResult
    ↓
Evaluator
    ↓
Metrics
```

Ground truth fields such as `expected_answer` and `relevant_document_ids` do not belong in `RunResult`.
