# EXP-029 Result: FLAN-T5 Model-Capacity Ablation

## Research question

Does increasing capacity within the FLAN-T5 family recover the planner capabilities that failed with FLAN-T5-small?

## Comparison

### FLAN-T5-small

```text
query generation without evidence       FAIL
query generation after evidence         FAIL
answer extraction                       PASS
answerability without evidence          PASS
answerability with final evidence       FAIL
```

### FLAN-T5-base

```text
query generation without evidence       FAIL
query generation after evidence         FAIL
answer extraction                       PASS
answerability without evidence          PASS
answerability with final evidence       PASS
```

Observed FLAN-T5-base outputs:

```text
query_generation_no_evidence
→ Developer Productivity is the owner of the production worker platform.

query_generation_after_intermediate_evidence
→ Developer Productivity maintains the Cirrus worker platform for production asynchronous workloads.

answer_extraction_from_final_evidence
→ CIRRUS-DLQ dead-letter queue

answerability_without_evidence
→ No

answerability_with_final_evidence
→ YES
```

## Interpretation

Increasing model capacity improved answerability judgment.

The base model can distinguish:

```text
no evidence → NO
sufficient evidence → YES
```

However, query generation remained qualitatively wrong.

Both query-generation probes produced declarative restatements rather than information-seeking queries.

## Conclusion

Model size is an important variable for stopping / answerability, but scaling within the FLAN-T5 family did not repair the main open-ended planning capability.

The next controlled experiment changes model family while keeping the task and capability probes fixed.
