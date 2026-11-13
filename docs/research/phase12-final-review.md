# Phase 12 — Reinforcement Learning Foundations: Research Review

## Scope and status

**Core foundation milestones: complete pending EXP-119 local validation.**
This review covers deterministic retrieval trajectories, reward design,
discounted returns, stochastic exploration, REINFORCE training and
small-corpus family transfer. It does **not** claim robust adaptive
retrieval, superiority to SFT, or LLM-scale RL.

## What we actually established

### EXP-111 to EXP-114: environment and reward invariants

The deterministic environment has legal retrieval actions K1/K2/K3/K5
and STOP, strictly increasing retrieval budgets, hidden supporting
labels, and audited coverage/cost/conflict exposure.

Reward v2 assigns the same terminal penalty to an incomplete forced
timeout as to an explicit premature STOP after an identical prefix.
The default six-step cap does not admit timeout under legal actions
(four increases + STOP); a shorter cap exercises timeout.

### EXP-115: discounted returns and oracle

Exhaustive finite-horizon legal trajectories establish reward upper
bounds. The gold oracle chooses K2 on the grounded Cirrus hybrid
ranking, where its relevant manual is second. At gamma 0.9, the
reward-optimal K2->STOP trajectory returns +2.7.

The oracle uses gold labels to *evaluate*, never to produce policy
inputs. The metric rewards evidence coverage, not final-answer quality.

### EXP-116: stochastic exploration

Seeded epsilon-greedy and uniform random policies demonstrate legal
stochastic rollouts without parameter updates. Exploration itself is
not reinforcement learning. The experiment includes short-horizon
timeouts, uniform sampling and gold-isolation checks.

### EXP-117: first on-policy policy-gradient learning

Five REINFORCE seeds, 2500 training episodes each, on one frozen Cirrus
hybrid query. The mean gamma=0.9 reward changed from **+1.5765** to
**+2.6722** (mean delta **+1.0957**, delta SD **0.0643**).
Oracle/fixed K2 +2.7000. All seeds reached complete evidence retrieval.

Seed 3 converged to a higher-cost solution: approx 3.05 documents vs
roughly 2.04–2.10 for the other seeds. Zero-rate control delta 0.

Synthetic transfer probes with altered hidden support failed badly:
seed-0 completion 0.016 for late and multi-support cases. These are
stress tests, not real held-out evidence-family evaluations.

**Conclusion:** a functioning on-policy REINFORCE optimizer on a
single fixed task, not generalization.

### EXP-118: genuine family-disjoint BM25 transfer

The 22-document corpus has 12 paired questions in six families.
Train a new tabular policy on BM25 Cirrus route-003 only; evaluate
ten questions from five other evidence families. BM25 rankings are
recomputed consistently across train/evaluation, to avoid conflating
the original hybrid Cirrus ranking with BM25.

| Metric | Value |
|---|---:|
| Heldout mean reward before | +1.6573 |
| Heldout mean reward after | +1.7540 |
| Mean delta | +0.0967 |
| Across-seed delta SD | 0.4797 |
| Heldout completion before | 0.7753 |
| Heldout completion after | 0.7416 |
| Fixed K2 mean return / completion | +2.3200 / 0.9000 |
| Fixed K3 mean return / completion | +2.6000 / 1.0000 |
| Gold oracle mean return | +2.7500 |
| Mean posttraining oracle gap | 0.9960 |

Per-seed heldout return differences:
**+0.698, -0.386, +0.661, -0.290, -0.200**.

Three of five seeds regressed. The mean gain is small relative to
seed-to-seed variation; evidence completion declined. The RL policy
did **not** beat the fixed K3 baseline. On the Solstice family,
one paraphrase required BM25 rank 3; training support was rank 1.

**Conclusion:** learning a budget preference is not the same as
learning an adaptive retrieval policy. The state is only
`(requested_k, steps_taken)`, so it cannot distinguish meaningfully
different user questions.

### EXP-119: Phase 11 / Phase 12 protocol audit

Phase 11 was LoRA supervised action imitation on a hybrid-action
space; Phase 12 is reward-based sequential control on BM25 in EXP-118.
The action sets and termination semantics differ, as do the held-out
families and metrics. Supervised classification accuracy cannot
validly be compared with sequential discounted reward by merely
renaming K1/K2/K3/K5. EXP-119 audits exact shared task/question
identities, split metadata and retriever-dependent K budgets.

## Evidence-backed conclusion

We now have:
- a deterministic and reward-audited retrieval RL environment,
- reproducible on-policy exploration with explicit legal-action masks,
- experimentally validated on-policy policy-gradient learning,
- a family-disjoint transfer evaluation with a **negative result**,
- strong fixed policies and gold-only oracle upper bounds,
- a documented barrier to direct SFT-versus-RL claims.

We **do not** have:
- an RL agent that understands evidence quality or source authority,
- a demonstrated improvement over the best fixed retrieval policy,
- a valid apples-to-apples Qwen SFT-versus-RL performance comparison,
- robust generalization across unseen knowledge domains,
- end-to-end answer correctness, contradictory-evidence resolution
  or unanswerable calibration under learned RL,
- justification for PPO/GRPO or high-compute LLM RL.

## Research decision

**Close the foundational Phase 12 milestones, but reject a claim of
successful adaptive retrieval generalization.**

The next research initiative should first develop a richer, strictly
policy-visible observation (retrieval scores, source metadata,
question features and document evidence), using fresh evidence-family
splits beyond the already inspected EXP-118 tasks. Then evaluate
controlled improvements against fixed K3 and the same heldout
end-to-end task reward protocol.

Do not tune on the EXP-118 heldout outcomes and then re-report them
as pristine test evidence.

## Reproduction

```bash
uv run pytest
uv run ruff check .
uv run python scripts/run_phase12_reward_v2_trajectory_sweep.py
uv run python scripts/run_phase12_return_oracle_baselines.py
uv run python scripts/run_phase12_stochastic_policy_exploration.py
uv run python scripts/run_phase12_tabular_reinforce.py
uv run python scripts/run_phase12_family_disjoint_transfer.py
uv run python scripts/run_phase12_policy_protocol_audit.py
```

The EXP-116 Monte Carlo output and final EXP-119 compatibility audit
should be included in the archived experiment results before claiming
comprehensive empirical reproduction of every phase command.
