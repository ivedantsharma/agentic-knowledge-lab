# Phase 12 — Reinforcement Learning Foundations

## Learning goal
Move from static supervised action imitation to outcome-based optimization of search trajectories.

## Core definitions
- State `s_t`: what the agent is allowed to observe before acting.
- Action `a_t`: next search/continue/stop choice.
- Transition: environment response `s_t, a_t → s_{t+1}`.
- Reward `r_t`: score assigned to consequences of that action.
- Trajectory `τ`: ordered states/actions/rewards for one question.
- Policy `π(a|s)`: distribution over actions given available state.
- Return `G_t = Σ γ^(k-t) r_k`: discounted sum of future rewards.

## Supervised vs RL
SFT learns to predict an oracle target action. RL prefers actions that produce better subsequent outcomes under the reward function. The label may be absent at decision time, but reward calculation in a controlled benchmark can use hidden ground truth.

## Credit assignment
If retrieving one document now enables a later correct answer, how much credit belongs to the earlier search? This is why trajectories, returns and value estimates matter more than an isolated action label.

## Discount factor
`γ ∈ [0,1]`. At γ=1, undiscounted return sums rewards. Smaller gamma prefers nearer rewards. For a short, finite retrieval episode we start at γ=1 and vary it only in a later controlled experiment.

## Policy-gradient intuition
A policy model produces action probabilities. REINFORCE uses sampled trajectories to increase log-probabilities of actions receiving high returns, schematically:
`gradient ∝ Σ ∇ log π(a_t|s_t) (G_t - baseline)`.
A baseline reduces variance. This is an overview, not an implementation yet.

## Crucial safety and scientific distinctions
- Hidden evaluation labels may compute rewards, but must never become policy input.
- Maximize task success under cost constraints, not proxy reward alone.
- Avoid paying repeatedly for the same relevant document.
- Reward design may cause hacking: excessive search, premature stop, evidence-only optimization, or ignoring ambiguity.
- Off-policy evaluation needs care; using rewards from an oracle trajectory as though it were an agent rollout is invalid.
- A successful reward unit test is not evidence that neural RL improved the policy.

## Learning sequence
1. EXP-111: deterministic environment, state/action/reward/trajectory
2. Reward-hacking and termination audit
3. Return and discount, dynamic-programming/oracle baselines
4. Stochastic policy and exploration
5. Policy gradient on small controlled environment
6. Compare to fixed and SFT policies with heldout family splits
7. Only then consider scalable LLM RL (e.g. PPO/GRPO) if evaluation quality and compute justify it
