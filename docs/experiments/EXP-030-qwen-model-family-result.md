# EXP-030 Result: Qwen Model-Family Ablation

## Goal

Test whether a causal chat/instruction model improves planner capabilities that remained weak across FLAN-T5-small and FLAN-T5-base.

## Model

```text
Qwen/Qwen2.5-0.5B-Instruct
```

## Results

```text
query_generation_no_evidence
→ failed jobs

query_generation_after_intermediate_evidence
→ Where do failed jobs go after they have been exhausted?

answer_extraction_from_final_evidence
→ The failed jobs are sent to the CIRRUS-DLQ dead-letter queue.

answerability_without_evidence
→ NO

answerability_with_final_evidence
→ YES
```

## Capability diagnosis

### Initial query generation

Weak.

The model identified the relevant concept ("failed jobs") but did not produce a sufficiently specific information-seeking query.

### Next-query generation

Pass.

After receiving intermediate evidence, the model produced a genuine missing-information query.

This is the first tested model to do so.

### Grounded answer extraction

Pass.

The answer contains the expected destination:

```text
CIRRUS-DLQ
```

### Answerability / stopping

Pass.

The model correctly distinguishes:

```text
no evidence      → NO
sufficient evidence → YES
```

## Interpretation

The model-family change mattered substantially.

Both FLAN variants failed open-ended query generation.

Qwen succeeds once the planner has an intermediate entity/evidence state.

The remaining weakness is bootstrap planning: generating the first useful search query from the original question alone.

## Architectural implication

A promising hybrid architecture is now visible:

```text
initial anchor / bootstrap planner
→ Qwen query generator
→ retriever
→ Qwen answerability check
→ Qwen grounded extraction
```

Before adopting that architecture, the next experiment should test Qwen inside the full SEARCH/STOP loop.
