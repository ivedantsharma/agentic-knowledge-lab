# Phase 12 High-Level Design — Retrieval Policy Reinforcement Learning

## Goal and boundaries
Study whether trajectory-level reward can train a retrieval-control policy, and whether that behavior transfers to new evidence families. This phase proves an RL *mechanism*, not robust adaptive QA.

## Architecture
```text
Question + frozen/document-ranked corpus
              ↓
RetrievalEpisodeV2 (hidden evaluator support IDs; budget/step state)
              ↓ public RetrievalObservation ONLY
Policy: fixed / epsilon-greedy / tabular softmax REINFORCE
              ↓ SEARCH_K1 / K2 / K3 / K5 / STOP
Action-mask and environment transition
              ↓ reward for new support, document cost, STOP/timeout
Trajectory log → discounted G_t / REINFORCE updates
              ↓
Evaluation: completion, mean discounted reward, retrieval cost,
oracle gap, seed variance, conflict exposure, source-family transfer
```

## Implementation map (verified repository paths)
- `knowledge_engine/rl/retrieval_environment.py`: typed actions, observations, transitions, original/v2 deterministic environment. Search budgets must strictly increase.
- `knowledge_engine/rl/reward_audit.py`: reward, gold-document coverage, cost, conflict and terminal diagnostics; gold remains hidden from policy.
- `knowledge_engine/rl/trajectory_baselines.py`: terminal path enumeration, discounted returns, fixed strategies and evaluator-only gold oracle.
- `knowledge_engine/rl/stochastic_policy.py`: masked uniform/epsilon-greedy policy, seeded Monte Carlo episodes.
- `knowledge_engine/rl/reinforce.py`: tabular softmax policy, return-to-go, score-function gradient, moving-average baseline, multiple-seed evaluation.
- `scripts/run_phase12_*.py`: executable experiments EXP-111–119. See `docs/experiments/` for hypothesis and result records.

## Decision boundary and reward
The policy may see question text and retrieved document IDs in the environment observation, but the **EXP-117/118 learned state** is deliberately restricted to `(requested_k, steps_taken)`. It cannot distinguish which question or evidence family is active. Labels are never direct policy features.

Reward v2: +2 per newly retrieved supporting document; −0.1 per new document; +1 for evidence-complete explicit STOP; −1 for incomplete explicit STOP; −1 for incomplete forced timeout. No extra bonus for a complete timeout. Reward measures gold *retrieval*, not answer correctness, freshness, or resolution of conflicts.

For legal increasing top-K actions there are only four distinct searches; six-step default episodes terminate through STOP and cannot reach a forced timeout. Two-step audits exercise the timeout behavior.

## Dataset and experiment controls
EXP-111–117 use the frozen Cirrus hybrid ranking (manual at rank 2). EXP-118 re-trains using BM25 over 22 real corpus documents and evaluates ten route questions in five non-Cirrus families; BM25 Cirrus manual is rank 1. Those protocols are **not interchangeable**.

Five seeds were used in EXP-117 and EXP-118; hidden-gold oracle returns are diagnostics, not learned-policy performance. Synthetic support-label changes in EXP-114–117 are explicitly stress tests, not heldout real data.

## Results and architecture implications
EXP-117: in-sample mean return +1.5765 → +2.6722 (oracle +2.7000). EXP-118: heldout mean +1.6573 → +1.7540, completion 0.7753 → 0.7416; three of five seeds regressed. Fixed K3 +2.6000 / completion 1.0 and oracle +2.7500 beat learned mean +1.7540.

**Architectural conclusion:** tabular state aliasing prevents true task-conditioned adaptation. Future agents need *policy-visible*, provenance-checked query/evidence signals, fresh evaluation families and a shared model-comparison protocol before any claim of better generalization.

## Known gaps
- The Phase 11 SFT classifier has REFORMULATE but no STOP; Phase 12 RL has STOP but no REFORMULATE.
- Phase 11 measures hybrid-action exact accuracy; Phase 12 measures sequential reward on BM25 in EXP-118. No apples-to-apples SFT-vs-RL conclusion is permitted.
- End-to-end answer quality, unanswerable detection, contradiction resolution and real-world latency were not optimized.
- See `docs/research/phase12-final-review.md`, `docs/architecture/ADR-016-rl-policy-evaluation-guardrails.md`, and `docs/experiments/EXP-119-policy-protocol-compatibility.md`.
