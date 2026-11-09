# EXP-073 Result: Hard-v0 Integrity Audit

## Report

```text
documents=22
tasks=10
answerable_tasks=6
unanswerable_tasks=4
role_reference_count=23

multi_hop=4
distractor=2
ambiguity=2
contradiction=2
stale_knowledge=3
unanswerable=4

missing_document_references=[]
duplicate_document_ids=[]
duplicate_task_ids=[]
temporal_tasks_without_dated_evidence=[
  "kbv2-hard-001",
  "kbv2-hard-005"
]
ambiguity_tasks_with_too_few_candidates=[]
passed=False
```

## Diagnosis

The benchmark data itself was not missing temporal policy dates.

The audit rule required every document in:

```text
supporting_document_ids ∪ stale_document_ids
```

to have `effective_at`.

That incorrectly rejects legitimate multi-hop bridge evidence such as:

```text
Atlas → Platform Reliability
Helios → Identity Foundations
```

because ownership/relationship records do not need temporal policy-version metadata.

## Failure classification

```text
audit-rule false positive
```

not:

```text
benchmark annotation failure
```

## Scientific response

Do not add artificial dates to bridge documents just to satisfy the audit.

Repair the audit so temporal tasks require:

1. dated stale evidence, and
2. at least one dated supporting document representing the current temporal fact.

Undated non-temporal bridge evidence remains valid.
