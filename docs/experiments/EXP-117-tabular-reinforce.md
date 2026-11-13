# EXP-117 — First Tabular REINFORCE Retrieval Policy Update

## Status

Implementation proposed; run the driver and review results before declaring
empirical success. This experiment is **in-sample learning mechanics only**.

## Research question

Can a policy that initially chooses legal retrieval actions uniformly learn
to maximize Reward v2 using only rewards from its *own sampled trajectories*?

Our current environment uses fixed ranking and no visible evidence text. The
experiment is therefore a minimal RL learning proof, **not** an adaptive
retrieval or knowledge-answering generalization test.

## Hypotheses (before running)

1. Training on grounded Cirrus route-003 with REINFORCE will typically increase
   the expected discounted return relative to the initial uniform policy.
2. Different random seeds may converge to different retrieval budgets.
   Report all seed outcomes, not just the best.
3. The best fixed K2 policy and gold-aware oracle remain the relevant ceilings
   under the single grounded Cirrus ranking; matching them is the goal, not
   outperforming the oracle.
4. A zero learning-rate control must reproduce its unchanged evaluation return.
5. Changing hidden supporting labels while keeping policy-visible state fixed
   cannot change an action sampled from **unchanged** logits and RNG; it can
   change the reward and therefore later *training* updates.
6. A policy trained only on Cirrus may perform poorly when synthetic support
   is later in the ranking, demonstrating non-transfer rather than an
   environment failure.

## RL method: REINFORCE

For each policy decision, the tabular agent computes a softmax over only the
legal actions. The state key is the observation's pair:

```
(requested_k, steps_taken)
```

The policy has **no access** to hidden support IDs, rewards, evidence labels,
document texts, or question-derived semantic features during action selection.

The action logit update is

```
logit(s,a_j) += learning_rate * gamma^t * (G_t - b(s))
               * (1[a_j==a_t] - pi(a_j|s))
```

where G_t is the return-to-go from the current step. The gamma^t term
matters for optimizing discounted **G0**, rather than an unweighted sum
of returns-to-go. The per-state moving-average baseline b(s) is computed
from earlier episodes. We compute a whole trajectory with fixed parameters
before updating the model using its own samples.

This is **tabular policy-gradient RL**, not PPO, GRPO, or LLM fine-tuning.
No oracle action labels are used for the parameter updates.

## Protocol

- Verify the original EXP-111 Cirrus ranking and grounded route-003 gold.
- Reward v2; gamma=0.9; max_steps=6 (forced timeouts are not reachable
  under this action space/horizon; EXP-116 covers the two-step timeout case).
- Training: 2500 episodes per seed, five seeds {0,1,2,3,4}.
- Parameters: learning rate 0.08; moving-average baseline rate 0.05.
- Evaluation: 800 fresh on-policy rollouts for each seed, before and after;
  independent evaluation RNG, identical evaluation seeds for the two policies.
- Baselines: fixed-K2, gold-aware finite-horizon oracle and EXP-116
  epsilon-K2 policy; the oracle is evaluator-only.
- Metrics: mean discounted return, across-seed return delta and SD,
  completion rate, premature STOP, retrieval cost, oracle gap,
  initial-action P(K2), and early/late training return.
- Negative control: repeat training with learning rate zero and check that
  evaluation returns remain unchanged.
- Transfer diagnostics: test the seed-0 trained policy against EXP-114's
  three **synthetic** changed-evidence configurations. These are not held-out
  benchmark tasks.

## Interpret carefully

- Multi-seed improvement on the training environment demonstrates learning
  mechanics, not generalization to new questions or knowledge domains.
- Fixed-K2 already attains the grounded Cirrus optimum. We should not claim
  REINFORCE beats a strong fixed baseline unless it actually does.
- The tabular state omits question meaning, source quality, evidence text,
  semantic entailment and contradiction resolution. It is intentionally
  incapable of learning question-dependent retrieval strategies.
- Synthetic cases share much of their observable structure but have changed
  hidden labels; perfect context-dependent transfer may be impossible with
  these features.
- Reward v2 measures retrieved gold-document presence and retrieval cost,
  not final-answer correctness. Conflict exposure remains diagnostic.
- A successful optimization run is not evidence that scaling to PPO, GRPO
  or a large language model will help.

## Run after merging

```bash
git pull
uv run pytest
uv run ruff check .
uv run python scripts/run_phase12_tabular_reinforce.py
```

## Acceptance gates

- All tests and lint pass.
- Finite-difference test validates the softmax log-gradient.
- Multi-seed results are reported even when one seed underperforms.
- Zero-learning-rate control produces no policy change.
- Training and evaluation run on disjoint RNG sequences, with the same
  grounded query (explicitly labeled in-sample).
- No label leak through the policy observation.

## Next milestone

Before concluding Phase 12, build **genuine held-out evidence-family tasks**
with retriever-generated rankings and meaningful policy-visible signals.
Compare fixed policies, trained tabular policy and Phase-11 SFT on a compatible
action/evaluation protocol, with multiple seeds and answer-quality caveats.
Do **not** call synthetic label flips real-world generalization evidence.
