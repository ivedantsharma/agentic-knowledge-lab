# EXP-036 Result: Relation-Verified Hybrid Planner

## Outcome

The hybrid planner solved the unseen dead-letter task end-to-end.

```text
AnswerCorrect=1.0000
```

## Trace

### Step 0 — semantic bootstrap

Query:

```text
Which worker platform is maintained by Developer Productivity?
```

Top result:

```text
org_dev_productivity
```

Structured state:

```text
entity=Cirrus
qualifier=production
```

### Step 1 — continuation decision

Candidate:

```text
cirrus
```

Diagnostics:

```text
grounded=True
relation_aligned=False
```

Therefore the planner correctly rejected STOP.

Generated search query:

```text
failed jobs, cirrus worker platform, developer productivity,
cirrus, job queue, retry attempts, production worker platform
```

Top result:

```text
manual_cirrus
```

### Step 2 — verified STOP

Candidate:

```text
CIRRUS-DLQ dead-letter queue
```

Diagnostics:

```text
grounded=True
relation_aligned=True
```

Final answer:

```text
CIRRUS-DLQ dead-letter queue
```

Expected:

```text
CIRRUS-DLQ
```

## Interpretation

The final architecture succeeds because it separates responsibilities:

```text
SemanticPlanner
→ bootstrap

Qwen2.5-0.5B-Instruct
→ continuation query generation
→ candidate extraction

Qwen2.5-1.5B-Instruct
→ relation verification

deterministic code
→ grounding invariant
```

The important success is not only answer correctness.

The system also rejected an early grounded-but-wrong candidate before continuing retrieval.

## Limitation

This remains one synthetic OOD task.

The result validates the mechanism, not broad generalization.

The next step is planner-level evaluation across multiple tasks and metrics.
