# Phase 13 High-Level Design — Full Research Campaign

## Goal
Run a controlled, reproducible *research campaign* across retrieval architectures and knowledge-agent behaviors. Build on completed foundations from Phases 0–12 without assuming that the latest learned policy is best.

## Research workflow
```text
 Research question and preregistered hypothesis
              ↓
 Versioned corpus + task registry / provenance checks
              ↓
 Frozen train / dev / unseen-family test and allowed observations
              ↓
 Common retrieval, action, evaluation and resource protocol
              ↓
 Strong fixed baselines + labeled diagnostic oracle
              ↓
 One-variable architecture ablations, multi-seed trials
              ↓
 Independent benchmark evaluator, cost/latency diagnostics
              ↓
 Per-family breakdown, uncertainty and failure review
              ↓
 Experiment result file + ADR / roadmap / HLD update
```

## Two research tracks
1. Agent-native knowledge engine: BM25, dense, RRF hybrid, reranker, hierarchical, graph, claim/evidence, agentic search, adaptive budget, and controlled learned search policies.
2. KnowledgeBench: direct, multi-hop, distractor, temporal/current, contradictory, ambiguous, abstention and prompt-injection tasks with gold provenance and hard split construction.

## Architecture layers
- **Corpus and dataset registry**: `data/processed/` plus source file content hashes and task/family provenance; initial audit in EXP-120.
- **Retriever adapters**: existing `knowledge_engine/retrieval/` implementations; compare only on the same corpus and task set.
- **Policy/agent controllers**: existing `knowledge_engine/rl/`, `knowledge_engine/training/`, and planners; action and retriever protocol must be aligned before head-to-head comparison.
- **Evaluation**: reuse KnowledgeBench evaluators, retrieval metrics and agent graders. Keep gold labels inside evaluators; record answer correctness separately from evidence presence.
- **Experiment runners**: deterministic `scripts/run_phase13_*.py`; seeds, model version, task IDs, environment and metrics recorded.
- **Documentation**: `docs/experiments/EXP-120-*.md` onward with independent results, `docs/research/phase13-*.md`, and ADRs.

## Controlled comparison rules
- Avoid cherry-picked evaluation samples, changes in retrieval budget or prompt, and train/test evidence-family leakage.
- Use fixed K1/K2/K3/K5, BM25, dense, hybrid and other established baselines when the task supports them.
- Report retrieval quality (Recall@K, MRR, grounding), full-answer correctness and unanswerable behavior separately from cost and latency.
- Trial variance comes from actual independent seeds/trials. Do not compute confidence intervals from just multiple paraphrases of the same evidence family as if independent.
- The EXP-118 heldout families were inspected; do not rebrand them as untouched after iteration. New holdouts are needed for future adaptive-policy claims.

## Initial campaign
EXP-120 freezes and audits benchmark sources, overlap, split exposure and reproducibility metadata before new performance optimization. See `docs/research/phase13-campaign-plan.md` and ADR-017.

## Exit requirements
Reproducible experiment protocol and results with baselines, ablations, variance, negative-result documentation, HLD/ADR, a final Phase 13 review, and a credible handoff into Phase 14 integration.
