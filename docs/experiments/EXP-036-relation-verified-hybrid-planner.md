# EXP-036: Relation-Verified Hybrid Planner

## Goal

Integrate the successful Qwen2.5-1.5B relation verifier into the end-to-end OOD planner.

## Final STOP policy

A candidate may terminate the trajectory only when all conditions hold:

```text
candidate exists
AND candidate is an exact grounded span
AND 1.5B verifier says relation aligned
```

Otherwise the planner generates another search query.

## Capability routing

```text
SemanticPlanner
→ bootstrap search

Qwen2.5-0.5B-Instruct
→ candidate extraction / abstention
→ continuation query generation

Qwen2.5-1.5B-Instruct
→ relation-alignment verification

deterministic code
→ exact-span grounding
```

## Trace correctness

The experiment previously called the model once for diagnostics and again for the actual action.

The runner now computes one decision and passes that exact decision into `action_from_decision`.

Therefore:

```text
printed decision == decision controlling action
```

This improves reproducibility and avoids duplicate model inference.

## Expected intermediate step

After retrieving the organization document:

```text
candidate_answer='Cirrus'
grounded=True
relation_aligned=False
```

Therefore the planner must SEARCH rather than STOP.

After retrieving the final manual:

```text
candidate contains CIRRUS-DLQ
grounded=True
relation_aligned=True
```

Therefore STOP is allowed.
