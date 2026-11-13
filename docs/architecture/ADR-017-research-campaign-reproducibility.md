# ADR-017 — Preregister Research Campaigns, Freeze Inputs, and Prevent Evaluator Leakage

## Status
Accepted for Phase 13 campaign design. EXP-120 validates input inventory; later experiments validate performance claims.

## Context
Phases 1–12 produced many retrieval/agent architectures and a richly annotated KnowledgeBench, but dataset sizes and historical retrieval configurations vary. EXP-118 found an unstable learned policy that underperformed fixed K3. Reusing inspected tests or mixing incomparable retrievers would undermine subsequent results.

## Decision
1. Each campaign experiment has an explicit hypothesis, preregistered controlled variable, baseline, dataset manifest/version, task IDs, source families, fixed evaluation protocol, seeds and failure criteria.
2. Record SHA-256 for immutable source files or dataset version identifiers; changing bytes makes a new benchmark version.
3. Keep gold supporting IDs and expected answers out of policy-visible features; evaluator computes metrics separately.
4. Split by **evidence family** and provenance, not randomly by paraphrase. Mark known/inspected families as development-contaminated for future iterative adaptation.
5. Report strong fixed baselines plus oracle upper bounds, multiple independent seeds, per-family metrics and uncertainty with proper sampling units.
6. Compare SFT and RL only once they share retriever, action semantics (including STOP/REFORMULATE), state, train/eval split and reward/quality metrics.
7. Keep negative results, deviations and non-comparability in experiment result files, not only successful summaries.

## Rejected alternatives
- Report a single best seed: susceptible to selection bias.
- Tune on inspected EXP-118 holdouts, then call them pristine: leaks evaluation feedback.
- Use per-query confidence interval as independent evidence when multiple queries share the same family: pseudoreplication.
- Compare Phase 11 action accuracy to Phase 12 discounted reward: different objectives and procedures.
- Scale models before establishing a baseline and valid protocol: poor interpretability.

## Consequences
EXP-120 creates the provenance inventory and campaign matrix. Subsequent experiments must use a defined comparison contract; Phase 14 may only cite results whose provenance and protocol are auditable.
