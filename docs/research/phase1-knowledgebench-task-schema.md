# Phase 1 — KnowledgeBench Task Schema

We now have metrics and aggregate evaluation.

The next problem is representation.

So far, benchmark data has been represented using loose dictionaries such as:

```python
{
    "q1": {"doc_a", "doc_b"}
}
```

That works for small experiments, but it becomes fragile once tasks need:

- question text
- expected answers
- relevant document IDs
- category
- difficulty
- metadata
- evidence annotations

We therefore need a typed task schema.

---

## 1. Why a schema?

A schema defines:

> What fields must every benchmark task contain?

Without a schema, different files may use different names:

```text
query
question
prompt
user_query
```

or:

```text
relevant_docs
gold_docs
evidence
supporting_documents
```

That creates bugs.

A schema gives us one contract.

---

## 2. First KnowledgeBench task

For v0, a task will contain:

- task_id
- question
- relevant_document_ids
- category
- expected_answer
- metadata

Example:

```python
KnowledgeTask(
    task_id="kb-001",
    question="Which company acquired Startup X?",
    relevant_document_ids={"doc-12", "doc-47"},
    category="multi_hop",
    expected_answer="Company Y",
    metadata={"difficulty": "medium"},
)
```

---

## 3. Why relevant documents and expected answer are separate

A system can produce the correct answer for the wrong reason.

Example:

```text
correct final answer
but
wrong retrieved evidence
```

That is why KnowledgeBench stores both:

- retrieval ground truth
- answer ground truth

Later we can separately score:

- retrieval quality
- evidence quality
- answer correctness

---

## 4. Category

Category helps us slice results.

Example categories:

- direct
- semantic_paraphrase
- exact_identifier
- multi_hop
- distractor
- ambiguous_entity
- contradiction
- temporal
- unanswerable
- prompt_injection

Suppose overall accuracy is 80%.

That number alone may hide:

```text
direct = 98%
multi_hop = 61%
temporal = 42%
```

Category-level evaluation reveals failure modes.

---

## 5. Metadata

Metadata is optional extra information.

Examples:

```python
{
    "difficulty": "hard",
    "source": "synthetic",
    "requires_temporal_reasoning": True,
}
```

We should not put core benchmark fields inside metadata.

If something is required for nearly every evaluator, it probably deserves a real schema field.

---

## 6. Why Pydantic?

We will use Pydantic later for many structured inputs.

It provides:

- validation
- clear field definitions
- JSON serialization
- useful errors
- Python type hints

For this first schema, we will introduce it deliberately rather than building a large framework.

---

## 7. Exercise

Open:

`knowledgebench/tasks/schema.py`

Implement the validation TODOs.

The schema should reject:

- blank task IDs
- blank questions
- blank category strings

For now, an empty relevant-document set is allowed because some benchmark tasks may intentionally be unanswerable.

Think carefully about why that is useful.

---

## 8. Design principle

A benchmark task should describe the task itself.

A system run should be stored separately.

Later we will have something like:

```text
KnowledgeTask
↓
Retriever / Agent
↓
RunResult
↓
Evaluator
↓
Metrics
```

Do not mix expected ground truth and model output into the same object.
