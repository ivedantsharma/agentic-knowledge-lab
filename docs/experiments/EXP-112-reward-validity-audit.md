# EXP-112 — Reward Validity and Termination Audit

## Motivation
EXP-111 proved the environment's arithmetic works, not that the reward measures trustworthy knowledge use. On `route-003` the top ranked document is a pending, non-effective Cirrus revision; the second is the current manual.

## What stays fixed
- The EXP-111 observed top-five ranking, explicitly frozen in the runner (no fresh embedding call).
- The existing reward function and its weights (+2 new support, -0.1 new doc, +1 complete STOP, -1 premature STOP).
- The same original query and gold supporting ID.
- No training, model sampling or optimizer.

## What changes
We audit the same trajectories with **additional evaluator-only diagnostics**:
1. supporting evidence coverage,
2. conflicting/pending-revision evidence exposure,
3. explicit STOP versus forced termination at max_steps.

## Hypotheses
- High reward can coexist with conflicting evidence exposure, because no conflict term is in v1 reward.
- Expiring `max_steps` after an incomplete search currently avoids the -1 premature-STOP penalty; this is a termination loophole.
- Gold and conflict labels must not enter policy-visible observation.

## Measures
Total reward, evidence coverage, retrieved count, conflicting exposure count, explicit stop, termination without STOP.

## Interpretation
`conflicting_exposure_count=1` is not proof of a wrong answer. We are auditing a *risk proxy*, not an answering model.

A missing timeout penalty is an actual objective inconsistency; fixing it requires an explicit reward design decision rather than quietly changing EXP-111 results.

## Next
Design reward v2 with terminal semantics and clarify whether conflict exposure is merely tracked or penalized; assess whether penalties would destroy useful evidence retrieval. Then study returns/credit assignment and a simple policy optimizer. Do not train a generative LLM on this reward yet.
