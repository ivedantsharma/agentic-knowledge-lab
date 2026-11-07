# EXP-028 Result: FLAN-T5-Small Capability Probe

## Goal

Decompose the failed generative planner into separate capabilities.

## Results

```text
query_generation_no_evidence
→ The production worker platform was owned by Developer Productivity.

query_generation_after_intermediate_evidence
→ The Cirrus worker platform is a retry attempt for the production worker platform.

answer_extraction_from_final_evidence
→ CIRRUS-DLQ dead-letter queue

answerability_without_evidence
→ No

answerability_with_final_evidence
→ No
```

## Capability diagnosis

### Query generation

Failed.

The model produced declarative statements rather than useful search queries.

### Answerability / stopping

Failed.

It correctly returned `No` when there was no evidence, but also returned `No` when the supplied evidence explicitly contained the requested destination.

Therefore its stopping judgment is not reliable.

### Grounded answer extraction

Succeeded.

Given sufficient evidence, the model extracted:

```text
CIRRUS-DLQ dead-letter queue
```

which contains the expected answer.

## Architectural implication

FLAN-T5-small should not be used as the planner policy for this benchmark.

Its useful capability is narrower:

```text
question + sufficient evidence
→ grounded answer extraction
```

The next controlled experiment changes only model capacity while preserving the same prompts and probes.
