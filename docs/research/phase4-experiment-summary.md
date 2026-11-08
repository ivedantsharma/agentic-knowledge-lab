# Phase 4 Experiment Summary

## Objective

Build and evaluate an agentic search planner that decides retrieval actions instead of following benchmark-authored hop plans.

## Experiment progression

| Experiment | Question | Main result |
|---|---|---|
| EXP-022 | Does the new agent loop work with an oracle planner? | Yes; 1.00 answer accuracy |
| EXP-023 | Can a non-oracle rule planner solve original tasks? | Yes on original wording |
| EXP-024 | Does rule planning survive paraphrases? | No; initial-plan rate 0 |
| EXP-025 | Can semantic intent matching recover paraphrases? | Yes; 1.00 on paraphrases |
| EXP-026 | Does semantic planning handle unseen intent? | No; retrieves useful evidence but answers wrong relation |
| EXP-027 | Does few-shot FLAN fix generative planning? | Format improved; planning still failed |
| EXP-028 | Which FLAN capabilities work? | Extraction works; query generation/stopping weak |
| EXP-029 | Does larger FLAN fix planning? | Answerability improves; query generation still weak |
| EXP-030 | Does model family matter? | Qwen improves continuation-query generation |
| EXP-031–033 | Can hybrid stopping be made reliable? | Grounding alone insufficient |
| EXP-034 | Can Qwen 0.5B verify relation alignment? | No; YES to all cases |
| EXP-035 | Does verifier capacity matter? | Qwen 1.5B gets NO, NO, YES, YES |
| EXP-036 | Can relation-verified hybrid solve OOD task? | Yes; end-to-end success |
| EXP-037 | Does hybrid win across multiple tasks? | No; 0.40 initial accuracy |
| EXP-038 | Does structured state improve hybrid trajectories? | Search success 0.40→0.80; premature stops 0.20→0 |

## Final comparison

After the conservative evaluator correction:

```text
Rule-based
AnswerAccuracy=0.8000
PlannerFailureRate=0.2000
SearchSuccessRate=0.8000
StopPrecision=1.0000

Semantic
AnswerAccuracy=0.8000
PlannerFailureRate=0.0000
SearchSuccessRate=1.0000
StopPrecision=0.8000

Hybrid
AnswerAccuracy=0.6000
PlannerFailureRate=0.0000
SearchSuccessRate=0.8000
StopPrecision=1.0000
PrematureStopRate=0.0000
```

## Most important findings

### 1. Closed-world semantic planning is robust but limited

Semantic intent matching handled paraphrases well but failed on a genuinely unseen relation.

### 2. Open-ended generation is capability-dependent

FLAN models were not strong next-query planners.

Qwen2.5-0.5B showed a better continuation-query capability.

### 3. Stopping is harder than it first appears

The project progressed through:

```text
answerability
→ grounding
→ extract-or-abstain
→ relation verification
```

Each stage exposed a new failure class.

### 4. Grounded does not mean correct

A candidate can occur verbatim in evidence and still answer the wrong relation.

### 5. Structured state remains necessary with LLM planners

Explicit entity and qualifier state improved hybrid SearchSuccessRate from 0.40 to 0.80.

### 6. Capability routing is better supported than one-model planning

Different models demonstrated different strengths.

### 7. Negative results were essential

The final architecture came from failures, not only successful runs.

## What Phase 4 does not claim

- the hybrid planner is generally better than deterministic planners,
- five synthetic tasks prove broad robustness,
- the 1.5B verifier generalizes to real enterprise search,
- exact-span grounding is a final groundedness solution,
- query generation is solved.

## Handoff to Phase 5

Phase 4 answers:

> Can the system choose and execute retrieval actions?

Partially, with measurable strengths and failure modes.

Phase 5 changes the retrieval substrate itself:

> Can the planner/search system navigate document hierarchy rather than searching a flat corpus only?
