# EXP-113 Result — Incomplete Timeout Reward Repair

## Setup
Preserve Reward v1 and add Reward v2, changing only incomplete forced-timeout handling for identical frozen Cirrus trajectories. No training, new rankings or model inference.

## Verified behavior
- Incomplete forced timeout in v1 has no extra terminal penalty.
- Incomplete forced timeout in v2 incurs −1, matching premature explicit STOP after the same retrieval prefix.
- Explicit STOP, complete retrieval rewards, and complete forced timeout behavior are unchanged.
- Conflicting evidence exposure remains an evaluator diagnostic; no automatic contradiction penalty.

## Verification
Implementation in `knowledge_engine/rl/retrieval_environment.py`, audit in `knowledge_engine/rl/reward_audit.py`, tests in `tests/test_retrieval_reward_v2.py`. EXP-114 expanded the check to 60 timeout/STOP counterfactual pairs.

## Interpretation and limitation
Fixed a precise termination-reward loophole; did not validate actual answer correctness, contradiction resolution, or optimized policies. For the authoritative follow-up, see `EXP-114-reward-v2-trajectory-sweep-result.md`.
